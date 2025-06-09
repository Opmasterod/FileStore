#(©)CodeFlix_Bots
#rohit_1888 on Tg #Dont remove this line

import base64
import re
import asyncio
import time
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from shortzy import Shortzy
from pyrogram.errors import FloodWait
from database.database import *



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

#used for cheking if a user is admin ~Owner also treated as admin level
async def check_admin(filter, client, update):
    try:
        user_id = update.from_user.id       
        return any([user_id == OWNER_ID, await db.admin_exist(user_id)])
    except Exception as e:
        print(f"! Exception in check_admin: {e}")
        return False


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

async def is_subscribed(client, user_id):
    channel_ids = await db.show_channels()

    if not channel_ids:
        return True

    if user_id == OWNER_ID:
        return True

    for cid in channel_ids:
        if not await is_sub(client, user_id, cid):
            # Retry once if join request might be processing
            mode = await db.get_channel_mode(cid)
            if mode == "on":
                await asyncio.sleep(2)  # give time for @on_chat_join_request to process
                if await is_sub(client, user_id, cid):
                    continue
            return False

    return True


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

async def is_sub(client, user_id, channel_id):
    try:
        member = await client.get_chat_member(channel_id, user_id)
        status = member.status
        #print(f"[SUB] User {user_id} in {channel_id} with status {status}")
        return status in {
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        }

    except UserNotParticipant:
        mode = await db.get_channel_mode(channel_id)
        if mode == "on":
            exists = await db.req_user_exist(channel_id, user_id)
            #print(f"[REQ] User {user_id} join request for {channel_id}: {exists}")
            return exists
        #print(f"[NOT SUB] User {user_id} not in {channel_id} and mode != on")
        return False

    except Exception as e:
        print(f"[!] Error in is_sub(): {e}")
        return False

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


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string

async def decode(base64_string):
    base64_string = base64_string.strip("=") # links generated before this commit will be having = sign, hence striping them to handle padding errors.
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def encode_link(f_msg_id: int, s_msg_id: int, channel_id: int) -> str:
    """
    Encode Telegram message IDs and return a Telegram bot deep link.
    
    Args:
        f_msg_id: First message ID
        s_msg_id: Second message ID
        channel_id: Channel ID (client.db_channel.id), included for context
        
    Returns:
        Telegram bot deep link in format: https://t.me/AK_LECTURES_BOT?start={encoded_string}
    """
    # Calculate multiplied values
    f_encoded = f_msg_id * 10
    s_encoded = s_msg_id * 10
    
    # Create the string to encode
    raw_string = f"get-HACKHEIST-{f_encoded}-{s_encoded}"
    
    # Encode to base64
    string_bytes = raw_string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii").rstrip("=")
    
    # Return Telegram bot deep link
    return f"https://t.me/AK_LECTURES_BOT?start={base64_string}"

async def decode_link(encoded_string: str) -> Tuple[int, int]:
    """
    Decode a base64 string from a Telegram bot deep link back to original message IDs.
    
    Args:
        encoded_string: The base64 encoded string (without the Telegram URL prefix)
        
    Returns:
        Tuple of (f_msg_id, s_msg_id)
    """
    # Handle padding
    encoded_string = encoded_string.rstrip("=")
    base64_bytes = (encoded_string + "=" * (-len(encoded_string) % 4)).encode("ascii")
    
    # Decode base64
    try:
        string_bytes = base64.urlsafe_b64decode(base64_bytes)
        decoded_string = string_bytes.decode("ascii")
    except (base64.binascii.Error, UnicodeDecodeError):
        raise ValueError("Invalid base64 encoded string")
    
    # Parse the decoded string
    if not decoded_string.startswith("get-HACKHEIST-"):
        raise ValueError("Invalid encoded string format")
    
    # Remove the prefix and split the remaining string
    try:
        # Remove 'get-HACKHEIST_' prefix
        number_part = decoded_string[len("get-HACKHEIST-"):]
        # Split by '-' to get f_encoded and s_encoded
        parts = number_part.split("-")
        if len(parts) != 2:
            raise ValueError("Invalid encoded string structure")
        
        f_encoded = int(parts[0])
        s_encoded = int(parts[1])
    except (ValueError, IndexError):
        raise ValueError("Invalid number format in encoded string")
    
    # Convert back to original message IDs
    f_msg_id = f_encoded // 10
    s_msg_id = s_encoded // 10
    
    return f_msg_id, s_msg_id


async def get_messages(client, channel_id, message_ids):
    messages = []
    total_messages = 0
    while total_messages < len(message_ids):
        temb_ids = message_ids[total_messages:total_messages+200]
        try:
            msgs = await client.get_messages(
                chat_id=channel_id,
                message_ids=temb_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)  # Use e.value for FloodWait duration
            try:
                msgs = await client.get_messages(
                    chat_id=channel_id,
                    message_ids=temb_ids
                )
            except Exception as e2:
                print(f"Error after FloodWait: {str(e2)}")
                msgs = []  # Assign empty list on failure
        except Exception as e:
            print(f"Error fetching messages: {str(e)}")
            msgs = []  # Assign empty list on failure
        total_messages += len(temb_ids)
        messages.extend(msgs if isinstance(msgs, list) else [msgs] if msgs else [])
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        # Return channel ID and message ID from forwarded message
        return message.forward_from_chat.id, message.forward_from_message_id
    elif message.forward_sender_name:
        return None, 0  # Forwarded from a hidden user, invalid
    elif message.text:
        # Handle both private (https://t.me/c/2493255368/45956) and public (https://t.me/username/45956) links
        pattern = r"https://t.me/(?:c/)?([^/]+)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return None, 0
        channel_identifier = matches.group(1)  # Either channel ID (digits) or username
        msg_id = int(matches.group(2))
        # Resolve channel_identifier to chat ID
        try:
            if channel_identifier.isdigit():
                # Private channel (e.g., 2493255368)
                channel_id = int(f"-100{channel_identifier}")
            else:
                # Public channel (e.g., username)
                chat = await client.get_chat(channel_identifier)
                channel_id = chat.id
            return channel_id, msg_id
        except:
            return None, 0
    else:
        return None, 0

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


def get_exp_time(seconds):
    periods = [('days', 86400), ('hours', 3600), ('mins', 60), ('secs', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)} {period_name}'
    return result

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


async def get_shortlink(url, api, link):
    shortzy = Shortzy(api_key=api, base_site=url)
    link = await shortzy.convert(link)
    return link


subscribed = filters.create(is_subscribed)
admin = filters.create(check_admin)

#rohit_1888 on Tg :

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
