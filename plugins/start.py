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

import asyncio
import os
import random
import sys
import re
import string 
import string as rohit
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.db_premium import *


BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}7"
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, prem_link)

        buttons = [
            [
                InlineKeyboardButton(text="ᴅᴏᴡɴʟᴏᴀᴅ", url=short_link),
                InlineKeyboardButton(text="ᴛᴜᴛᴏʀɪᴀʟ", url=TUT_VID)
            ],
            [
                InlineKeyboardButton(text="ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")
            ]
        ]

        await message.reply_photo(
            photo=SHORTENER_PIC,
            caption=SHORT_MSG.format(
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except IndexError:
        pass



@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    id = message.from_user.id
    is_premium = db.is_premium_user(id)

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]]
            )
        )

    # ✅ Check Force Subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    # File auto-delete time in seconds
    FILE_AUTO_DELETE = await db.get_del_timer()

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Handle normal message flow
    text = message.text
    if len(text) <= 7:
        await message.reply_text("Welcome to the bot!")
        return

    try:
        base64_string = text.split(" ", 1)[1]
        # Handle WEBSITE_URL_MODE HACKHEIST parameter
        if base64_string.startswith("HACKHEIST="):
            base64_string = base64_string.split("HACKHEIST=", 1)[1]
    except IndexError:
        await message.reply_text("Welcome to the bot!")
        return

    # Try decoding the string
    try:
        string = await decode(base64_string)
        if string.startswith("get-HACKHEIST-"):
            # Handle new HACKHEIST format
            is_premium, remaining_time = await db.is_premium_user(id)
            current_time = int(time.time())
            if not is_premium:
                user_doc = await db.premium_users.find_one({'_id': id})
                if user_doc and 'expiration_time' in user_doc and user_doc['expiration_time'] <= current_time:
                    await message.reply_text(
                        f"ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴇxᴘɪʀᴇᴅ 🥲\n"
                        f"𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐟𝐨𝐫 𝐛𝐮𝐲 𝐚𝐠𝐚𝐢𝐧 - ",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")]]
                        )
                    )
                else:
                    await message.reply_text(
                        f"<blockquote><b>𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚 𝐩𝐫ᴇᴍ𝐢ᴜᴍ 𝐮𝐬𝐞𝐫 🥺</b></blockquote>\n"
                        f"Contact for buy",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")]]
                        )
                    )
                return
            try:
                channel_id, f_msg_id, s_msg_id = await decode_link(base64_string)
                if f_msg_id <= s_msg_id:
                    ids = range(f_msg_id, s_msg_id + 1)
                else:
                    ids = []
                    i = f_msg_id
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < s_msg_id:
                            break
            except ValueError as e:
                await message.reply_text(f"Error parsing HACKHEIST format: {str(e)}")
                return
        else:
            # Process new format: get-{channel_id}-{f_msg_id}-{s_msg_id}
            argument = string.split("-")
            if len(argument) == 4 and argument[0] == "get":
                try:
                    channel_id = int(argument[1])
                    f_msg_id = int(argument[2])
                    s_msg_id = int(argument[3])
                    if f_msg_id <= s_msg_id:
                        ids = range(f_msg_id, s_msg_id + 1)
                    else:
                        ids = []
                        i = f_msg_id
                        while True:
                            ids.append(i)
                            i -= 1
                            if i < s_msg_id:
                                break
                except (ValueError, IndexError) as e:
                    await message.reply_text(f"Error parsing format: {str(e)}")
                    return
            elif len(argument) == 3 and argument[0] == "get":
                try:
                    channel_id = int(argument[1])
                    f_msg_id = int(argument[2])
                    ids = [f_msg_id]  # Single message ID
                except (ValueError, IndexError) as e:
                    await message.reply_text(f"Error parsing single ID format: {str(e)}")
                    return
            else:
                await message.reply_text("Invalid format structure")
                return

        # Fetch messages using get_messages from helper_funcn.py
        try:
            messages = await get_messages(client, channel_id, ids)
            # Process messages (e.g., send to user, apply auto-delete, etc.)
            for msg in messages:
                if msg:
                    # Example: Forward or send the message content
                    await msg.copy(chat_id=user_id, disable_notification=True)
                else:
                    await message.reply_text("Failed to fetch one or more messages.")
        except Exception as e:
            await message.reply_text(f"Error fetching messages: {str(e)}")
            return

    except ValueError as e:
        await message.reply_text(f"Failed to decode string: {str(e)}")
        return

        temp_msg = await message.reply(
            f"<b> 𝗪𝗮𝗶𝘁 𝗕𝗵𝗮𝗶 🥺.. </b>"
            )
        
        try:
            messages = await get_messages(client, ids)
            
        except Exception as e:
            await temp_msg.edit(f"Something went wrong: {str(e)}")
            return
        await temp_msg.delete()

        codeflix_msgs = []
        
        for msg in messages:
            # Initialize filename and media_type with safe defaults
            filename = "Unknown"
            media_type = "Unknown"

            # Determine the media type and filename
            if msg.video:
                media_type = "Video"
                filename = msg.video.file_name if msg.video.file_name else "Unnamed Video"
            elif msg.document:
                filename = msg.document.file_name if msg.document.file_name else "Unnamed Document"
                media_type = "PDF" if filename.endswith(".pdf") else "Document"
            elif msg.photo:
                media_type = "Image"
                filename = "Image"
            elif msg.text:
                media_type = "Text"
                filename = "Text Content"

    # Generate caption
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=(msg.caption.html if msg.caption else "𝗛𝗔𝗖𝗞𝗛𝗘𝗜𝗦𝗧 🔥"),
                    filename=filename,
                    mediatype=media_type,
                )
                if bool(CUSTOM_CAPTION)
                else (msg.caption.html if msg.caption else "")
            )

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None


            try:
                # Use protect_content=True for new format, PROTECT_CONTENT for old format
                protect_content = True if is_new_format else PROTECT_CONTENT
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
                await asyncio.sleep(0.5)
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=protect_content
                )
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                await message.reply_text(f"Error copying message: {str(e)}")
        
            await asyncio.sleep(2)

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}"
                f"<blockquote><b>ʙᴜᴛ ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ 😁 ᴀғᴛᴇʀ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴀɢᴀɪɴ ᴀᴄᴄᴇss ᴛʜʀᴏᴜɢʜ ᴏᴜʀ ᴡᴇʙsɪᴛᴇs 😘</b></blockquote>"
                f"<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:    
                if snt_msg:
                    try:    
                        await snt_msg.delete()  
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"{WEBSITE_URL}{message.command[1]}"
                    if message.command and len(message.command) > 1
                    else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<blockquote><b>ʏᴏᴜʀ ʟᴇᴄᴛᴜʀᴇs / ᴘᴅғ ɪs  ᴅᴇʟᴇᴛᴇᴅ !!\n</b></blockquote>"
                    "<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴅᴇʟᴇᴛᴇᴅ ʟᴇᴄᴛᴜʀᴇs / ᴘᴅғ 👇</b>\n\n"
                    "<b> <a href=https://yashyasag.github.io/hiddens_officials>🌟 𝗢𝗧𝗛𝗘𝗥 𝗪𝗘𝗕𝗦𝗜𝗧𝗘𝗦 🌟</a></b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                    [InlineKeyboardButton("• 𝗠𝗔𝗜𝗡 𝗪𝗘𝗕𝗦𝗜𝗧𝗘 •", url="https://yashyasag.github.io/hiddens_officials")],

    [
                    InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data = "about"),
                    InlineKeyboardButton('ʜᴇʟᴘ •', callback_data = "help")

    ]
            ]
        )
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586)  # 🔥
        
        return



#=====================================================================================##
# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport



# Create a global dictionary to store chat data
chat_data_cache = {}

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i>Checking Subscription...</i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  # Should return list of (chat_id, mode) tuples
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  # fetch mode 

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link

                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @HACKHEISTBOT</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        # Retry Button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @HACKHEISTBOT</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

#=====================================================================================##

@Bot.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id  # Get user ID from the message

    # Get the premium status of the user
    status_message = await check_user_plan(user_id)

    # Send the response message to the user
    await message.reply(status_message)

#=====================================================================================##
@Bot.on_message(filters.command('addpremium') & filters.private & admin)
async def add_premium_command(client: Client, message: Message):
    try:
        args = message.text.split(" ", 2)[1:]
        if len(args) < 2:
            await message.reply_text("Usage: /addpremium {user_id} {time_in_seconds} or /addpremium All {time_in_seconds}")
            return
        
        time_seconds = int(args[1])
        if time_seconds <= 0:
            await message.reply_text("Time must be a positive number of seconds")
            return

        if args[0].lower() == "all":
            await db.add_all_premium(time_seconds)
            await message.reply_text(f"All users set as premium for {time_seconds} seconds")
        else:
            user_id = int(args[0])
            if not await db.present_user(user_id):
                await message.reply_text(f"User {user_id} not found in database")
                return
            await db.add_premium_user(user_id, time_seconds)
            await message.reply_text(f"User {user_id} set as premium for {time_seconds} seconds")
    except (IndexError, ValueError) as e:
        await message.reply_text(f"Error: {str(e)}. Usage: /addpremium {user_id} {time_in_seconds} or /addpremium All {time_in_seconds}")

@Bot.on_message(filters.command('removepremium') & filters.private & admin)
async def remove_premium_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(" ", 1)[1])
        await db.remove_premium_user(user_id)
        await message.reply_text(f"Premium status removed for user {user_id}")
    except (IndexError, ValueError) as e:
        await message.reply_text(f"Error: {str(e)}. Usage: /removepremium {user_id}")

@Bot.on_message(filters.command('listpremiumusers') & filters.private & admin)
async def list_premium_users_command(client: Client, message: Message):
    premium_list = db.list_premium_users()
    if not premium_list:
        await message.reply_text("No premium users found")
        return
    
    response = "Premium Users:\n"
    for user_id, remaining_time in premium_list:
        if user_id == "All":
            response += f"All users: {remaining_time} seconds remaining\n"
        else:
            response += f"User {user_id}: {remaining_time} seconds remaining\n"
    await message.reply_text(response)
# Command to add premium user
@Bot.on_message(filters.command('addpremiumopp') & filters.private & admin)
async def add_premium_user_command(client, msg):
    if len(msg.command) != 4:
        await msg.reply_text(
            "Usage: /addpremium <user_id> <time_value> <time_unit>\n\n"
            "Time Units:\n"
            "s - seconds\n"
            "m - minutes\n"
            "h - hours\n"
            "d - days\n"
            "y - years\n\n"
            "Examples:\n"
            "/addpremium 123456789 30 m → 30 minutes\n"
            "/addpremium 123456789 2 h → 2 hours\n"
            "/addpremium 123456789 1 d → 1 day\n"
            "/addpremium 123456789 1 y → 1 year"
        )
        return

    try:
        user_id = int(msg.command[1])
        time_value = int(msg.command[2])
        time_unit = msg.command[3].lower()  # supports: s, m, h, d, y

        # Call add_premium function
        expiration_time = await add_premium(user_id, time_value, time_unit)

        # Notify the admin
        await msg.reply_text(
            f"✅ User `{user_id}` added as a premium user for {time_value} {time_unit}.\n"
            f"Expiration Time: `{expiration_time}`"
        )

        # Notify the user
        await client.send_message(
            chat_id=user_id,
            text=(
                f"🎉 Premium Activated!\n\n"
                f"You have received premium access for `{time_value} {time_unit}`.\n"
                f"Expires on: `{expiration_time}`"
            ),
        )

    except ValueError:
        await msg.reply_text("❌ Invalid input. Please ensure user ID and time value are numbers.")
    except Exception as e:
        await msg.reply_text(f"⚠️ An error occurred: `{str(e)}`")


# Command to remove premium user
@Bot.on_message(filters.command('remove_premiums') & filters.private & admin)
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("useage: /remove_premium user_id ")
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"User {user_id} has been removed.")
    except ValueError:
        await msg.reply_text("user_id must be an integer or not available in database.")


# Command to list active premium users
@Bot.on_message(filters.command('premium_usersss') & filters.private & admin)
async def list_premium_users_command(client, message):
    # Define IST timezone
    ist = timezone("Asia/Kolkata")

    # Retrieve all users from the collection
    premium_users_cursor = collection.find({})
    premium_user_list = ['Active Premium Users in database:']
    current_time = datetime.now(ist)  # Get current time in IST

    # Use async for to iterate over the async cursor
    async for user in premium_users_cursor:
        user_id = user["user_id"]
        expiration_timestamp = user["expiration_timestamp"]

        try:
            # Convert expiration_timestamp to a timezone-aware datetime object in IST
            expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(ist)

            # Calculate remaining time
            remaining_time = expiration_time - current_time

            if remaining_time.total_seconds() <= 0:
                # Remove expired users from the database
                await collection.delete_one({"user_id": user_id})
                continue  # Skip to the next user if this one is expired

            # If not expired, retrieve user info
            user_info = await client.get_users(user_id)
            username = user_info.username if user_info.username else "No Username"
            first_name = user_info.first_name
            mention=user_info.mention

            # Calculate days, hours, minutes, seconds left
            days, hours, minutes, seconds = (
                remaining_time.days,
                remaining_time.seconds // 3600,
                (remaining_time.seconds // 60) % 60,
                remaining_time.seconds % 60,
            )
            expiry_info = f"{days}d {hours}h {minutes}m {seconds}s left"

            # Add user details to the list
            premium_user_list.append(
                f"UserID: <code>{user_id}</code>\n"
                f"User: @{username}\n"
                f"Name: {mention}\n"
                f"Expiry: {expiry_info}"
            )
        except Exception as e:
            premium_user_list.append(
                f"UserID: <code>{user_id}</code>\n"
                f"Error: Unable to fetch user details ({str(e)})"
            )

    if len(premium_user_list) == 1:  # No active users found
        await message.reply_text("I found 0 active premium users in my DB")
    else:
        await message.reply_text("\n\n".join(premium_user_list), parse_mode=None)


#=====================================================================================##

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")


#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
