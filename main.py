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

Bad = TelegramClient(
    "eval_telethon",
    TELETHON_API_ID,
    TELETHON_API_HASH
).start(bot_token=TELETHON_BOT_TOKEN)

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

# Load installed plugins from file
def load_installed_plugins():
    if os.path.exists("installed_plugins.txt"):
        with open("installed_plugins.txt", "r") as file:
            return set(file.read().splitlines())
    return set()

# Save installed plugins to file
def save_installed_plugins(plugins):
    with open("installed_plugins.txt", "w") as file:
        file.write("\n".join(plugins))

installed_plugins = load_installed_plugins()

# Load installed plugins at startup
for plugin in installed_plugins:
    try:
        __import__(plugin)
        logger.info(f"Loaded plugin: {plugin}")
    except ImportError as e:
        logger.error(f"Failed to load plugin {plugin}: {str(e)}")

# Pyrogram eval command
@app.on_edited_message(
    filters.command("eval")
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
    filters.command("eval")
    & ~filters.forwarded
    & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_name.endswith(".py"):
            file_path = await client.download_media(document)
            with open(file_path, "r") as file:
                cmd = file.read()
        else:
            return await edit_or_reply(message, text="<b>Only .py files are supported.</b>")
    elif len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ [ᴘʏ] ?</b>")
    else:
        cmd = message.text.split(" ", maxsplit=1)[1]

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
               
@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)

@app.on_callback_query(filters.regex("forceclose"))
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

@app.on_edited_message(
    filters.command("sh")
    & ~filters.forwarded
    & ~filters.via_bot
)
@app.on_message(
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

# Telethon eval command
@Bad.on(events.NewMessage(pattern='/eval2'))
async def eval_handler(event):
    if event.reply_to and event.reply_to.file and event.reply_to.file.name.endswith('.py'):
        file_path = await event.client.download_media(event.reply_to)
        with open(file_path, "r") as file:
            cmd = file.read()
    elif len(event.raw_text.split()) < 2:
        await event.reply("ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ [ᴛᴇʟᴇ] ?")
        return
    else:
        cmd = event.raw_text.split(" ", maxsplit=1)[1]

    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        exec(
            "async def __aexec(event): "
            + "".join(f"\n {a}" for a in cmd.split("\n"))
        )
        await locals()["__aexec"](event)
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
        keyboard = [
            [Button.inline(f"⏳ {round(t2-t1, 3)} Seconds")],
        ]
        await event.respond(file=filename, buttons=keyboard)
        os.remove(filename)
    else:
        t2 = time()
        keyboard = [
            [Button.inline(f"⏳ {round(t2-t1, 3)} Seconds"), Button.inline("🗑", data=f"forceclose|{event.sender_id}")],
        ]
        await event.respond(final_output, buttons=keyboard)

@Bad.on(events.CallbackQuery(data="forceclose"))
async def forceclose_callback(event):
    if event.sender_id != int(event.data.decode().split("|")[1]):
        await event.answer("» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪғ ʏᴏᴜ sᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛs ʙᴀʙʏ.", alert=True)
        return
    await event.delete()

@Bad.on(events.CallbackQuery(data=re.compile(b"runtime")))
async def runtime_callback(event):
    runtime = event.data.decode().split(None, 1)[1]
    await event.answer(runtime, alert=True)


# Function to check if a plugin is already installed
def is_plugin_installed(plugin_name):
    return plugin_name in installed_plugins

# Modified install command
@app.on_message(filters.command("install") & ~filters.forwarded & ~filters.via_bot)
async def install_plugin(client, message):
    if message.reply_to_message and message.reply_to_message.document:
        # Handle installation from a .py file reply
        try:
            document = message.reply_to_message.document
            plugin_name = os.path.splitext(document.file_name)[0]
            if is_plugin_installed(plugin_name):
                return await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' is already installed.</b>")

            file_path = await client.download_media(document)
            with open(file_path, "r") as file:
                code = file.read()
            
            # Save the code to new .py files for both Pyrogram and Telethon
            with open(f"pyrogram_{plugin_name}.py", "w") as plugin_file_pyrogram, open(f"telethon_{plugin_name}.py", "w") as plugin_file_telethon:
                plugin_file_pyrogram.write(code)
                plugin_file_telethon.write(code)
            
            # Verify the plugin import
            try:
                __import__(f"pyrogram_{plugin_name}")
                __import__(f"telethon_{plugin_name}")
                installed_plugins.add(plugin_name)
                save_installed_plugins(installed_plugins)
                await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' installed successfully for both Pyrogram and Telethon from file.</b>")
                logger.info(f"Plugin '{plugin_name}' installed successfully for both Pyrogram and Telethon from file.")
            except ImportError as e:
                await edit_or_reply(message, text=f"<b>Failed to import plugin '{plugin_name}':</b>\n<pre>{str(e)}</pre>")
                logger.error(f"Failed to import plugin '{plugin_name}': {str(e)}")
        except Exception as e:
            await edit_or_reply(message, text=f"<b>Failed to install plugin from file:</b>\n<pre>{str(e)}</pre>")
            logger.error(f"Failed to install plugin from file: {str(e)}")
    else:
        # Handle installation from command text
        if len(message.command) < 2:
            return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/install <plugin_code>")
        try:
            plugin_code = message.text.split(" ", maxsplit=1)[1].strip()
            plugin_name = "custom_plugin"
            if is_plugin_installed(plugin_name):
                return await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' is already installed.</b>")

            with open(f"pyrogram_{plugin_name}.py", "w") as plugin_file_pyrogram, open(f"telethon_{plugin_name}.py", "w") as plugin_file_telethon:
                plugin_file_pyrogram.write(plugin_code)
                plugin_file_telethon.write(plugin_code)
            
            # Verify the plugin import
            try:
                __import__(f"pyrogram_{plugin_name}")
                __import__(f"telethon_{plugin_name}")
                installed_plugins.add(plugin_name)
                save_installed_plugins(installed_plugins)
                await edit_or_reply(message, text=f"<b>Plugin installed successfully for both Pyrogram and Telethon from command.</b>")
                logger.info("Plugin installed successfully for both Pyrogram and Telethon from command.")
            except ImportError as e:
                await edit_or_reply(message, text=f"<b>Failed to import plugin:</b>\n<pre>{str(e)}</pre>")
                logger.error(f"Failed to import plugin: {str(e)}")
        except Exception as e:
            await edit_or_reply(message, text=f"<b>Failed to install plugin from command:</b>\n<pre>{str(e)}</pre>")
            logger.error(f"Failed to install plugin from command: {str(e)}")


# Modified uninstall command
@app.on_message(filters.command("uninstall") & ~filters.forwarded & ~filters.via_bot)
async def uninstall_plugin(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/uninstall <plugin_name>")
    plugin_name = message.text.split(" ", maxsplit=1)[1].strip()
    try:
        os.remove(f"pyrogram_{plugin_name}.py")
        os.remove(f"telethon_{plugin_name}.py")
        await edit_or_reply(message, text=f"<b>Plugin '{plugin_name}' uninstalled successfully for both Pyrogram and Telethon.</b>")
        logger.info(f"Plugin '{plugin_name}' uninstalled successfully for both Pyrogram and Telethon.")
    except Exception as e:
        await edit_or_reply(message, text=f"<b>Failed to uninstall plugin '{plugin_name}':</b>\n<pre>{str(e)}</pre>")
        logger.error(f"Failed to uninstall plugin '{plugin_name}': {str(e)}")

# Restart command to ensure commands persist across restarts
@app.on_message(filters.command("rs") & ~filters.forwarded & ~filters.via_bot)
async def restart(client: PyroClient, message: Message):
    reply = await message.reply_text("**🔁 Restarting...**")
    await message.delete()
    await reply.edit_text("Successfully Restarted\nPlease wait 1-2 min for loading user plugins...")
    logger.info("Bot is restarting...")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")
        
            

