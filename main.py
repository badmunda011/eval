import time
import os
import subprocess
import sys
import shlex
import traceback
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

# Define bot credentials (Use your own token and API credentials)
API_ID = "12380656"
API_HASH = "d927c13beaaf5110f25c505b7c071273"
BOT_TOKEN = "7663505148:AAH0ZgYmJkLOpYh5LcJPyEfsLvag_e0tR6s"

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Store bot's startup time for uptime calculation
start_time = time.time()

# Helper function to calculate uptime
def get_uptime():
    uptime_seconds = time.time() - start_time
    uptime = str(datetime.timedelta(seconds=uptime_seconds))
    return uptime

# Command: /start
@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Hello! I am a bot with various administrative features.\nUse /help to see all available commands.")

# Command: /help
@bot.on_message(filters.command("help"))
async def help_command(client, message: Message):
    help_text = """
    Available commands:
    /start - Greet the user.
    /help - Show this help message.
    /restart - Restart the bot.
    /reboot - Reboot the system.
    /sh <command> - Execute shell commands for installing/updating packages.
    /eval <code> - Execute Python code.
    /update - Pull the latest changes from the repository.
    /ping - Check the bot's uptime.
    """
    await message.reply(help_text)

# Command: /restart
@bot.on_message(filters.command("restart"))
async def restart(client, message: Message):
    await message.reply("Restarting the bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Command: /reboot
@bot.on_message(filters.command("reboot"))
async def reboot(client, message: Message):
    await message.reply("Rebooting the system...")
    subprocess.run(["sudo", "reboot"])

# Command: /sh
@bot.on_message(filters.command("sh"))
async def execute_shell(client, message: Message):
    if len(message.text.split()) > 1:
        cmd = " ".join(message.text.split()[1:])
        try:
            output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT, timeout=60)
            await message.reply(f"Command executed successfully:\n``` {output.decode()} ```")
        except subprocess.CalledProcessError as e:
            await message.reply(f"Error occurred while executing the command:\n``` {e.output.decode()} ```")
    else:
        await message.reply("Please provide a shell command to execute.")

# Command: /eval
@bot.on_message(filters.command("eval"))
async def eval_code(client, message: Message):
    if len(message.text.split()) > 1:
        code = " ".join(message.text.split()[1:])
        try:
            exec_locals = {}
            exec(code, {}, exec_locals)
            output = exec_locals.get("Success")
            await message.reply(f"Result:\n\n ``` {output} ``` ")
        except Exception as e:
            await message.reply(f"Error during execution:\n ``` {traceback.format_exc()} ```")
    else:
        await message.reply("Please provide Python code to execute.")

# Command: /update
@bot.on_message(filters.command("update"))
async def update_repo(client, message: Message):
    await message.reply("Updating the bot from the repository...")
    try:
        # Pull the latest changes from the git repository
        subprocess.check_call(["git", "pull"])
        await message.reply("Bot updated successfully.")
    except subprocess.CalledProcessError:
        await message.reply("Failed to update the bot from the repository.")

# Command: /ping
@bot.on_message(filters.command("ping"))
async def ping(client, message: Message):
    uptime = get_uptime()
    await message.reply(f"Pong! Uptime: {uptime}")

# Start the bot
print("Bot Started") 
bot.run()
