# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

#rohit_1888 on Tg
#--------------------------------------------
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7931405874:AAGodglFGX3zOG49z5dxMff_GpaNLgxZ9OE")
APP_ID = int(os.environ.get("APP_ID", "23713783")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "2daa157943cb2d76d149c4de0b036a99") #Your API Hash from my.telegram.org
#--------------------------------------------
WEBSITE_URL_MODE = os.environ.get("WEBSITE_URL_MODE", "True")
WEBSITE_URL = os.environ.get("WEBSITE_URL", "https://alien-unac.github.io/gettings/?token=")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002493255368")) #Your db channel Id
OWNER = os.environ.get("OWNER", "ll_HACKHEIST_ll") # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "5487643307")) # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://namanjain123eudhc:opmaster@cluster0.5iokvxo.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")
#--------------------------------------------
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "0"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/CodeflixSupport")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
#--------------------------------------------
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/PV7wZVd/x.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/PV7wZVd/x.jpg")

#--------------------------------------------
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkshortify.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
TUT_VID = os.environ.get("TUT_VID","https://t.me/hwdownload/3")
SHORT_MSG = "<b>⌯ Here is Your Download Link, Must Watch Tutorial Before Clicking On Download...</b>"

SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
#--------------------------------------------

#--------------------------------------------
HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ʟᴇᴄᴛᴜʀᴇ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ ʜᴀᴄᴋʜᴇɪsᴛ\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/TEAM_OPTECH>𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧</a></blockquote></b>"
ABOUT_TXT = "<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/HACKHEISTBOT>HACKHEIST</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://yashyasag.github.io/hiddens_officials>𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 𝗪𝗘𝗕</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/HACKHEISTBOT>HACKHEIST</a></blockquote></b>"
#--------------------------------------------
#--------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote> ɪ ᴀᴍ ʟᴇᴄᴛᴜʀᴇ ᴘʀᴏᴠɪᴅᴇʀ ʙᴏᴛ, ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴀʟʟ ʟᴇᴄᴛᴜʀᴇs 😈 ᴀɴᴅ ᴘᴅғs 😁</blockquote></b>")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ʟᴇᴄᴛᴜʀᴇs/ᴘᴅғs</b>")

CMD_TXT = "<blockquote><b>HACKHEIST</b></blockquote>"
#--------------------------------------------
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", """<b>{previouscaption}</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>⛧ 🄱🅈 :-) </b><b><a href="https://yashyasag.github.io/hiddens">ℍ𝔸ℂ𝕂ℍ𝔼𝕀𝕊𝕋 😈</a></b> <b>♛</b>\n<b>━━━━━━━━━━━━━━━━━◇</b>\n<b>🙏 sʜᴀʀᴇ ᴀɴᴅ sᴜᴘᴘᴏʀᴛ ᴜs 👇</b>\n<b>—————————————————</b>\n<b><a href="https://yashyasag.github.io/hiddens">🚀 𝗠𝗢𝗥𝗘 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>\n<b>—————————————————</b>""")
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False #set True if you want to prevent users from forwarding files from bot
#--------------------------------------------
#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'
#--------------------------------------------
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

#==========================(BUY PREMIUM)====================#

OWNER_TAG = os.environ.get("OWNER_TAG", "HACKHEISTBOT")
UPI_ID = os.environ.get("UPI_ID", "rukosaar")
QR_PIC = os.environ.get("QR_PIC", "https://i.ibb.co/PV7wZVd/x.jpg")
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"t.me/HACKHEISTBOT")
#--------------------------------------------
#Time and its price
#7 Days
PRICE1 = os.environ.get("PRICE1", "0 rs")
#1 Month
PRICE2 = os.environ.get("PRICE2", "60 rs")
#3 Month
PRICE3 = os.environ.get("PRICE3", "150 rs")
#6 Month
PRICE4 = os.environ.get("PRICE4", "280 rs")
#1 Year
PRICE5 = os.environ.get("PRICE5", "550 rs")
#===================(END)========================#

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
