import asyncio
from telegram import Bot

# Replace with your bot's token
TOKEN = "XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


async def get_channel_id():
    bot = Bot(token=TOKEN)

    # Get the list of the bot's updates
    updates = await bot.get_updates()

    for update in updates:
        # Check if the update has a message or channel_post
        if update.message and update.message.chat:
            chat = update.message.chat
        elif update.channel_post and update.channel_post.chat:
            chat = update.channel_post.chat
        else:
            continue

        # If the chat is a channel
        if chat.type == "channel":
            print(f"Channel Name: {chat.title}")
            print(f"Channel ID: {chat.id}")


async def main():
    await get_channel_id()


if __name__ == "__main__":
    asyncio.run(main())
