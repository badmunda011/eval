import os
import shutil
import asyncio
import re
import subprocess
import sys
import traceback
import logging
from inspect import getfullargspec
from io import StringIO
from time import time
from pyrogram.types import BotCommand
from pyrogram import filters, Client as PyroClient, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telethon import TelegramClient, events, Button
from telethon.tl.custom import Button

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pyrogram Bot API
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7280541678:AAE7Or_mN10MPV2gjEi_JjK3gaFx3XmoRnk"
OWNER_ID = 7009601543

# Telethon Bot API
TELETHON_API_ID = "16457832"
TELETHON_API_HASH = "3030874d0befdb5d05597deacc3e83ab"
TELETHON_BOT_TOKEN = "7280541678:AAE7Or_mN10MPV2gjEi_JjK3gaFx3XmoRnk"

app = PyroClient(
           name="EVAL", 
           api_id=API_ID, 
           api_hash=API_HASH, 
           bot_token=BOT_TOKEN
)

            

if __name__ == "__main__":
    try:
        logger.info("Starting Pyrogram client...")
        app.run()
        logger.info("Pyrogram client started successfully.")
    except Exception as e:
        logger.error(f"Failed to start Pyrogram client: {str(e)}")
    else:
        app.send_message(OWNER_ID, "Bot started successfully.")
    
    try:
        logger.info("Starting Telethon client...")
        Bad.start()
        Bad.run_until_disconnected()
        logger.info("Telethon client started successfully.")
    except Exception as e:
        logger.error(f"Failed to start Telethon client: {str(e)}")
    else:
        Bad.send_message(OWNER_ID, "Bot started successfully.")

    idle()
