# 🎵 Telegram Music Bot 🎵
**A Telegram bot that fetches songs from Spotify, downloads them as MP3, and posts them to artist-specific Telegram channels with clickable links to Spotify and YouTube.**

---

## 🚀 Features
- Automatic Song Fetching: Fetches songs for artists from Spotify.
- Multi-Artist Support: Handles multiple artists, each with a dedicated Telegram bot and channel.
- Thumbnails and Links: Posts songs with album thumbnails and clickable links to Spotify and YouTube.
- Smart Posting: Skips songs already posted to avoid duplicates.

---

## 🚀 Implementation
**In this project, we fetch music tracks from Spotify and share them on Telegram channels using a Telegram bot. Here’s how the implementation works:**

### 🎵 Fetching All Songs
Spotify's API limits the number of albums or tracks returned per request to 50. To bypass this, we implemented a pagination system. This means we can make multiple requests to fetch all albums and songs from an artist, regardless of the 50-item limit.

We start by searching for the artist and retrieving their Spotify ID. Then, we fetch the artist's albums in batches, starting from the first album. We continue fetching albums until all albums have been retrieved. Once we have the list of albums, we fetch the tracks for each album and add them to our list.

### 🗓️ Sorting and Processing Tracks
After retrieving all albums and tracks, we sort them by their release date, ensuring that songs are shared in chronological order. This makes the bot share music in the order it was released, giving users a better experience.

### 💬 Posting on Telegram
Once all tracks are fetched, we use a Telegram bot to send these tracks to the appropriate Telegram channel. We use the Spotify link and YouTube link (from YouTube search) to provide listeners with the option to listen to the tracks via these platforms. Each track is posted with a thumbnail and a clickable link to both Spotify and YouTube.

---

## 🛠️ Installation
**Clone the Repository**
```bash
git clone https://github.com/MinoMakh/Telegram-Music-Bot
cd Telegram-Music-Bot
```
**Set Up the Environment**
1. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
2. **Install dependencies:**
```bash
pip install -r requirements.tx
```

---

## ⚙️ Configuration
Add an `config.json` File at the same level of `script.py`
- Add artists, Telegram bot tokens, and channel IDs in the following format:

```json
{
    "ARTISTS": {
        "Artist Name": ["Bot Token", "Channel ID"]
    },
    "SPOTIPY_CLIENT_ID": "your_spotify_client_id",
    "SPOTIPY_CLIENT_SECRET": "your_spotify_client_secret"
}
```
Replace `your_spotify_client_id` and `your_spotify_client_secret` with Spotify API credentials.

### Obtain Spotify API Credentials
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Create a new app and note down the Client ID and Client Secret.

### Bot Token Setup
**To create Telegram bots for each artist, follow these steps using BotFather:**

1. **Start a Chat with BotFather:**
   - Open Telegram and search for [BotFather](https://telegram.me/BotFather).
   - Start a chat by clicking on Start.
2. **Create a New Bot:**
   - Type the command:
```
/newbot
```
   - Follow the prompts to:
     1. Give your bot a unique name.
     2. Assign a username ending with bot.
3. **Receive Your Bot Token:**
   - After completing the steps, BotFather will provide you with a bot token:
```
Use this token to access the HTTP API:
123456789:ABCDefghIJKLMNOqrstUVwxyz12345
```
4. **Repeat for Each Artist:**
   - Use the /newbot command again to create bots for all artists in your project.
   - Save each token securely.

### Channel ID Setup
**To fetch the Telegram Channel IDs:**

1. **Create Telegram Channels:**
   - Open Telegram and create a channels for each artist.
   - Assign each one appropriate names.
2. **Add Your Bot as an Admin:**
   - Go to the channel settings.
   - Add the bot as an admin with full permissions.
3. **Send a Message:**
   - After adding the bot, send a message in the channel (it can be anything, e.g., "Hello").
   - This step is crucial because the get_channel_id.py script fetches updates and cannot retrieve the channel ID without a message in the channel.
4. **Modify the get_channel_id.py Script:**
   - Open the get_channel_id.py file and replace TOKEN with the bot token for the specific artist:
```python
TOKEN = "123456789:ABCDefghIJKLMNOqrstUVwxyz12345"  # Replace with your bot token
```
5. **Run the Script:**
   - Use the following command to execute the script:
```bash
python get_channel_id.py
```
The script will output the channel ID in the console (If not repeat step 3).
6. **Update the Config File:**
   - Add the bot token and channel ID for each artist to the config.json file in this format:
```json
{
    "ARTISTS": {
        "Taylor Swift": ["123456789:ABCDefghIJKLMNOqrstUVwxyz12345", "-1001122334455"],
        "Ariana Grande": ["987654321:ZYXWVUTSRQPONMLKJIHGFEDCBA54321", "-1005566778899"]
    }
}
```
7. **Run the main script:**
   - Run the main script:
```bash
python script.py
```
8. **Automate with Cron (Optional)**
   - To run the bot automatically every 24 hours, schedule it using cron:
     1. Open the crontab editor:
```bash
crontab -e
```
  2. Add the following line to schedule the script at 2:10 AM (for example):

```ruby
10 2 * * * /path/to/venv/bin/python3 /path/to/Telegram-Music-Bot/script.py
```

---

## 📂 File Structure
```bash
Telegram-Music-Bot/
├── config.json          # Configuration file for artists and API keys
├── script.py            # Main bot script
├── get_channel_id.py    # Script to fetch Telegram channel IDs
├── requirements.txt     # Python dependencies
├── songs/               # Directory for downloaded songs
```

---

## Screenshots:
<img src="https://github.com/user-attachments/assets/56678036-4bee-4830-9a93-30bce063401b" width="500"/>
<img src="https://github.com/user-attachments/assets/491b030f-c3f7-4862-a72d-bc5094528e07" width="500"/>
<img src="https://github.com/user-attachments/assets/51fa0cd4-6563-4017-9d13-511ea5dfc2ec" width="500"/>
<img src="https://github.com/user-attachments/assets/cee5ed10-04f5-479d-a431-b0d365d8f5bc" width="500"/>
