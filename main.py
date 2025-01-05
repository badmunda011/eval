import asyncio
import os
import subprocess
import re
import sys
import time
import shlex
import traceback
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime
from inspect import getfullargspec
from io import StringIO
from time import time
import openai
import os
import io
import logging
import PIL.Image
from pyrogram.types import Message
import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import os
import requests
from pyrogram import Client, filters

# Set up your API key for Gemini
API_KEY = 'AIzaSyCdj8Mao0nFV7tcRMqwneMStcSEP4HTldU'
BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'


# Define bot credentials (Use your own token and API credentials)
API_ID = "12380656"
API_HASH = "d927c13beaaf5110f25c505b7c071273"
BOT_TOKEN = "7663505148:AAH0ZgYmJkLOpYh5LcJPyEfsLvag_e0tR6s"
MODEL_NAME = "gemini-1.5-flash"

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)

@bot.on_message(filters.command("ping"))
async def ping(client, message):
    # Get the current uptime
    uptime_seconds = time.time() - start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    uptime_message = f"Bot uptime: {hours} hours, {minutes} minutes, {seconds} seconds."
    
    # Respond to the user with the uptime
    await message.reply_text(uptime_message)


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




async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@bot.on_edited_message(
    filters.command("eval")
    & ~filters.forwarded
    & ~filters.via_bot
)
@bot.on_message(
    filters.command("eval")
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: bot, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2-t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ ᴇᴠᴀʟ :</b>\n<code>{cmd[0:980]}</code>\n\n<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached Document",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@bot.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@bot.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ʙᴀʙʏ.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@bot.on_edited_message(
    filters.command("sh")
    & ~filters.forwarded
    & ~filters.via_bot
)
@bot.on_message(
    filters.command("sh")
    & ~filters.forwarded
    & ~filters.via_bot
)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Output</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")
    await message.stop_propagation()





genai.configure(api_key="AIzaSyCdj8Mao0nFV7tcRMqwneMStcSEP4HTldU")

model = genai.GenerativeModel(MODEL_NAME)

@bot.on_message(filters.command("gem"))
async def gemi_handler(client: Client, message: Message):
    loading_message = None
    try:
        loading_message = await message.reply_text("**Generating response, please wait...**")

        if len(message.text.strip()) <= 5:
            await message.reply_text("**Provide a prompt after the command.**")
            return

        prompt = message.text.split(maxsplit=1)[1]
        response = model.generate_content(prompt)

        response_text = response.text
        if len(response_text) > 4000:
            parts = [response_text[i:i + 4000] for i in range(0, len(response_text), 4000)]
            for part in parts:
                await message.reply_text(part)
        else:
            await message.reply_text(response_text)

    except Exception as e:
        await message.reply_text(f"**An error occurred: {str(e)}**")
    finally:
        if loading_message:
            await loading_message.delete()

@bot.on_message(filters.command("imgai"))
async def generate_from_image(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("**Please reply to a photo for a response.**")
        return

    prompt = message.command[1] if len(message.command) > 1 else message.reply_to_message.caption or "Describe this image."

    processing_message = await message.reply_text("**Generating response, please wait...**")

    try:
        img_data = await client.download_media(message.reply_to_message, in_memory=True)
        img = PIL.Image.open(io.BytesIO(img_data.getbuffer()))

        response = model.generate_content([prompt, img])
        response_text = response.text

        await message.reply_text(response_text, parse_mode=None)
    except Exception as e:
        logging.error(f"Error during image analysis: {e}")
        await message.reply_text("**An error occurred. Please try again.**")
    finally:
        await processing_message.delete()



def generate_response(prompt):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'contents': [{'parts': [{'text': prompt}]}]
    }
    response = requests.post(BASE_URL, headers=headers, json=data)
    return response.json()


@bot.on_message(filters.text)
def handle_message(client, message):
    prompt = message.text
    response_data = generate_response(prompt)
    response_text = response_data['contents'][0]['parts'][0]['text']
    message.reply_text(response_text)


# Run the bot
if __name__ == "__main__":
    bot.run()
