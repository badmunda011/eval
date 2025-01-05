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


# Define bot credentials (Use your own token and API credentials)
API_ID = "12380656"
API_HASH = "d927c13beaaf5110f25c505b7c071273"
BOT_TOKEN = "7663505148:AAH0ZgYmJkLOpYh5LcJPyEfsLvag_e0tR6s"

bot = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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






from pyrogram import Client, filters, types as t
from lexica import Client as ApiClient, AsyncClient
from pyrogram.types import InlineKeyboardButton
from math import ceil
import asyncio

# Global database to store user data
Database = {}

# API client for lexica
api = ApiClient()
Models = api.getModels()['models']['image']

async def ImageGeneration(model, prompt):
    try:
        client = AsyncClient()
        output = await client.generate(model, prompt, "")
        if output['code'] != 1:
            return 2
        elif output['code'] == 69:
            return output['code']
        task_id, request_id = output['task_id'], output['request_id']
        await asyncio.sleep(20)
        
        tries = 0
        image_url = None
        resp = await client.getImages(task_id, request_id)
        
        while True:
            if resp['code'] == 2:
                image_url = resp['img_urls']
                break
            if tries > 15:
                break
            await asyncio.sleep(5)
            resp = await client.getImages(task_id, request_id)
            tries += 1
            continue
        return image_url
    except Exception as e:
        raise Exception(f"Failed to generate the image: {e}")
    finally:
        await client.close()

def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_models(page_n: int, models: list, user_id) -> list:
    modules = sorted(
        [
            EqInlineKeyboardButton(
                x['name'],
                callback_data=f"d.{x['id']}.{user_id}"
            )
            for x in models
        ]
    )

    pairs = list(zip(modules[::3], modules[1::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 3
    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE: COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "◁", callback_data=f"d.left.{modulo_page}.{user_id}"
                ),
                EqInlineKeyboardButton(
                    "⌯ ᴄᴀɴᴄᴇʟ ⌯", callback_data=f"close_data"
                ),
                EqInlineKeyboardButton(
                    "▷", callback_data=f"d.right.{modulo_page}.{user_id}"
                ),
            )
        ]
    else:
        pairs += [[EqInlineKeyboardButton("⌯ ʙᴀᴄᴋ ⌯", callback_data=f"d.-1.{user_id}")]]
    return pairs

@bot.on_message(filters.command(["draw", "create", "imagine", "dream"]))
async def draw(bot, m: t.Message):
    global Database
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("<code>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ. ᴜsᴀɢᴇ: /draw <prompt></code>")
    
    user = m.from_user
    data = {'prompt': prompt, 'reply_to_id': m.id}
    Database[user.id] = data
    btns = paginate_models(0, Models, user.id)
    
    await m.reply_text(
        text=f"**ʜᴇʟʟᴏ {m.from_user.mention}**\n\n**sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ ᴍᴏᴅᴇʟ**",
        reply_markup=t.InlineKeyboardMarkup(btns)
    )

@bot.on_callback_query(filters.regex(pattern=r"^d.(.*)"))
async def selectModel(bot, query: t.CallbackQuery):
    global Database
    data = query.data.split('.')
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    
    if len(data) > 3:
        if data[1] == "right":
            next_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(next_page + 1, Models, auth_user)
                )
            )
        elif data[1] == "left":
            curr_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(curr_page - 1, Models, auth_user)
                )
            )
        return
    
    modelId = int(data[1])
    await query.edit_message_text("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ, ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ ɪᴍᴀɢᴇ.**")
    promptData = Database.get(auth_user, None)
    if promptData is None:
        return await query.edit_message_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.")
    
    img_url = await ImageGeneration(modelId, promptData['prompt'])
    if img_url is None or img_url == 2 or img_url == 1:
        return await query.edit_message_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.")
    elif img_url == 69:
        return await query.edit_message_text("ɴsғᴡ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ !")
    
    images = []
    modelName = [i['name'] for i in Models if i['id'] == modelId]
    for i in img_url:
        images.append(t.InputMediaPhoto(i))
    images[-1] = t.InputMediaPhoto(img_url[-1], caption=f"Your Prompt:\n`{promptData['prompt']}`")
    
    await query.message.delete()
    try:
        del Database[auth_user]
    except KeyError:
        pass
    
    await bot.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptData['reply_to_id']
    )



# Replace with your own OpenAI API Key
openai.api_key = "sk-svcacct-ODSR6PDrMrri2FKqOcF3fllzsO_ozGpicR3c-ktg0XhFYv-k82m_zCtCxXVfDH_eLT3BlbkFJ_8cFz58nC4DNG0cjjEU_UchG7Z0UdPim7nrsnW6NbiqxJaGopkYa8IgvVyhOTM_AA"

# Function to get the AI response using OpenAI's GPT-3
def get_ai_response(user_input):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # You can use other models like text-ada, text-babbage, etc.
            prompt=user_input,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

@bot.on_message(filters.text)
async def ai_reply(client, message):
    # Get the user's message
    user_message = message.text.strip()

    # Send typing action
    await message.reply("Thinking...", quote=True)

    # Get AI's response
    ai_response = get_ai_response(user_message)

    # Send the AI's response to the user
    await message.reply(ai_response, quote=True)



# Run the bot
if __name__ == "__main__":
    bot.run()
