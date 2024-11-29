from bot import Bot
import pyrogram.utils

# Optional: You can set the MIN_CHANNEL_ID manually if needed (otherwise, remove this line).
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Run the bot
if __name__ == "__main__":
    Bot().run()
