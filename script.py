import asyncio
import spotipy
import yt_dlp
from telegram import Bot
from telegram.error import TelegramError
import os
import re
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# Load the configuration file
with open("config.json") as config_file:
    config = json.load(config_file)


# Load the artists and Spotify API credentials from the configuration file
# Artists should be in the format: "Artist Name": ["Telegram Bot Token", "Telegram Channel ID"]
ARTISTS = config["ARTISTS"]
SPOTIPY_CLIENT_ID = config["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = config["SPOTIPY_CLIENT_SECRET"]


# Set up Spotify API client (for searching songs)
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

# Function to sanitize song names (Remove everything but alphanumeric characters and spaces)
def sanitize_song_name(song_name):
    return re.sub(r"[^\w\s]", "", song_name)


# Set up Telegram Bot
def get_bot(token):
    return Bot(token=token)


# Function to download thumbnail image (only once)
def download_thumbnail(image_url):
    image_filename = "thumbnail.jpg"
    if not os.path.exists(image_filename):  # Check if the image already exists
        try:
            image_response = requests.get(image_url)
            with open(image_filename, "wb") as f:
                f.write(image_response.content)
            print("Thumbnail downloaded successfully.")
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")
    else:
        print("Thumbnail already exists, skipping download.")
    return image_filename


# Function to get albums and tracks by artist, sorted by release date
def get_songs_by_artist(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist")
    if not results["artists"]["items"]:
        print(f"Artist {artist_name} not found.")
        return []

    artist_id = results["artists"]["items"][0]["id"]
    albums = []
    offset = 0

    while True:
        artist_albums = sp.artist_albums(
            artist_id, include_groups="album,single", limit=50, offset=offset
        )
        albums.extend(artist_albums["items"])
        if len(artist_albums["items"]) < 50:
            break
        offset += 50

    albums.sort(key=lambda album: album["release_date"])
    song_list = []
    for album in albums:
        album_id = album["id"]
        album_name = album["name"]
        album_release_date = album["release_date"]
        album_image_url = album["images"][0]["url"] if album["images"] else ""

        album_tracks = sp.album_tracks(album_id, limit=50)
        for track in album_tracks["items"]:
            song_list.append(
                {
                    "name": track["name"],
                    "url": track["external_urls"]["spotify"],
                    "album_image_url": album_image_url,
                    "artist": artist_name,
                    "album_name": album_name,
                    "release_date": album_release_date,
                    "duration": track["duration_ms"] / 1000,
                }
            )

    return sorted(song_list, key=lambda song: song["release_date"])


# Function to download song as MP3
def download_song(song_name, artist_name):
    query = f"{artist_name} {song_name} mp3"
    sanitized_song_name = sanitize_filename(song_name)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{sanitized_song_name}.mp3",
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            youtube_video_url = result["entries"][0]["webpage_url"]
            ydl.download([f"ytsearch:{query}"])
        return f"{sanitized_song_name}.mp3", youtube_video_url
    except Exception as e:
        print(f"Error downloading song {song_name}: {e}")
        return None, None


# Function to send MP3 to Telegram channel
async def send_song(
    bot,
    file_path,
    artist,
    album_image_url,
    duration,
    spotify_url,
    youtube_url,
    song_name,
    channel_id,
):
    try:
        thumbnail_file = download_thumbnail(album_image_url)

        if thumbnail_file:
            sanitized_title = sanitize_filename(song_name)

            with open(thumbnail_file, "rb") as thumb_file:
                with open(file_path, "rb") as audio_file:
                    message = f'<b>Listen on: <a href="{spotify_url}">Spotify</a> | <a href="{youtube_url}">YouTube</a></b>'

                    await bot.send_audio(
                        chat_id=channel_id,
                        audio=audio_file,
                        caption=message,
                        thumbnail=thumb_file,
                        performer=artist,
                        title=sanitized_title,
                        duration=duration,
                        parse_mode="HTML",
                    )

            os.remove(thumbnail_file)
    except TelegramError as e:
        print(f"Error sending audio: {e}")


# Function to update posted songs in the file for a given artist
# Using 'latin1' encoding to handle potential Western European characters in the file.
# It ensures correct reading of files with non-ASCII characters without errors, especially in legacy systems.
def update_posted_songs_file(artist_name, song_name):
    sanitized_song_name = sanitize_song_name(song_name)
    artist_folder = f"./songs/{sanitize_filename(artist_name)}"
    os.makedirs(artist_folder, exist_ok=True)
    file_path = os.path.join(artist_folder, "posted_songs.txt")

    posted_songs = set()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="latin1") as f:
            posted_songs = set(f.read().splitlines())

    if sanitized_song_name not in posted_songs:
        with open(file_path, "a") as f:
            f.write(f"{sanitized_song_name}\n")


# Function to check and post new songs
# Using 'latin1' encoding to handle potential Western European characters in the file.
# It ensures correct reading of files with non-ASCII characters without errors, especially in legacy systems.
async def check_and_post_new_songs(bot, artist_name, channel_id):
    artist_songs = get_songs_by_artist(artist_name)

    artist_folder = f"./songs/{sanitize_filename(artist_name)}"
    os.makedirs(artist_folder, exist_ok=True)
    file_path = os.path.join(artist_folder, "posted_songs.txt")

    file_posted_songs = set()
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="latin1") as f:
            file_posted_songs = set(f.read().splitlines())
            
    for song in artist_songs:
        if sanitize_song_name(song["name"]) not in file_posted_songs:
            mp3_file, youtube_url = download_song(song["name"], song["artist"])

            if mp3_file:
                await send_song(
                    bot,
                    mp3_file,
                    song["artist"],
                    song["album_image_url"],
                    song["duration"],
                    song["url"],
                    youtube_url,
                    song["name"],
                    channel_id,
                )
                update_posted_songs_file(artist_name, song["name"])
                os.remove(mp3_file)

            await asyncio.sleep(5)
        else:
            print(f"Song {song['name']} already posted.")


# Main function to start checking songs for an artist
async def main():
    for artist, data in ARTISTS.items():
        token, channel_id = data
        bot = get_bot(token)
        await check_and_post_new_songs(bot, artist, channel_id)


if __name__ == "__main__":
    asyncio.run(main())
