import logging
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Pyrogram Bot API
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7502185711:AAHVIGXxrRLb0WUyR606njxpRS2vz-jOduM"

app = Client(
    name="EVAL",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# Define your fonts as a list
fonts = [
    "🤍 ⍣⃪‌ ᶦ ‌ᵃᵐ⛦⃕‌!❛𝆺𝅥⤹࿗𓆪ꪾ™",
    "ᯓ𓆰𝅃🔥!⃪⍣꯭꯭𓆪꯭🝐",
    "➺ ‌⃪⃜ !✦ 𝆺𝅥⎯ꨄ",
    "❛ .𝁘ໍ!𓆪ִֶָ ֺ⎯꯭‌ 𓆩💗𓆪𓈒",
    "𓆰𝅃꯭᳚𓄂️𝆺𝅥⃝🔥 ‌⃪‌ ᷟ𓆩 ! 乛|⁪⁬⁮⁮⁮⁮ ‌⁪⁬𓆪🐼™",
    "ᯓ𓆰𝅃꯭᳚🦁!˶‌‌꯭꯭꯭꯭꯭꯭֟፝ ⚡꯭꯭꯭꯭꯭",
    "◄❥‌‌❥ ⃝⃪⃕🦚⟵᷽᷍!˚‌‌‌‌◡‌⃝🐬᪳ ‌⃪𔘓❁‌‌❍•:➛",
    "➺꯭ ꯭𝅥‌꯭𝆬‌🦋⃪꯭ ─‌⃛┼ 𝞄⃕𝖋𝖋 !🥵⃝⃝ᬽ꯭ ⃪꯭ ꯭𝅥‌꯭𝆬‌➺꯭⎯⎯᪵᪳",
    "ᯓ𓆰 𝅃!™ ٭ - 𓆪ꪾ⌯ 🜲 ˹ 𝐎ᴘ ˼",
    "—‌‌ 𝐈тᷟʑ‌꯭𓄂︪︫︠𓆩〭〬!⍣⃪‌ ꭗ‌‌𝆺꯭𝅥𔘓༌🪽⎯꯭‌⎯꯭ ꯭",
    "𓆰𓏲!𓂃ֶꪳ 𓆩〭〬🦋𓆪ꪾ",
    "𓆰⎯꯭꯭֯‌⌯ !𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ",
    "🍹𝆺𝅥⃝🤍 ‌⃪‌ ᷟ●!🤍᪳𝆺꯭𝅥⎯꯭‌⎯꯭",
    "⋆⎯፝֟፝֟⎯᪵ 𝆺꯭𝅥! ᭄꯭🦋꯭᪳᪳᪻⎯‌⎯🐣",
    "⟶‌ꭙ⋆\"🔥𓆩〬 !⎯᳝֟፝֟⎯‌ꭙ⋆\"🔥",
    "⟶‌ꭙ⋆\"🔥𓆩〬 !🤍᪳𝆺꯭𝅥⎯᳝֟፝֟⎯‌",
    "⋆─፝─᪵།‌꯭! ا۬‌𝆺𝅥⃝🌸𝄄꯭꯭𝄄꯭꯭ 𝅥‌꯭𝆬‌👑",
    "❛ .𝁘ໍ!ꨄ 🦋𓂃•",
    "⟶‌𓆩〬𝁘ໍ!𓂃˖ॐ🪼⎯᳝֟፝⎯‌ꭙ⋆\"",
    "⏤‌‌ !𓂃 🔥𝆺𝅥 🜲 ⌯",
    "𓆰⎯꯭꯭֯‌!𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ",
    ".𝁘ໍ⎯꯭‌- !⌯ 𝘅𝗗 𓂃⎯꯭‌ ִֶָ ֺ🎀",
    "𓂃❛ ⟶‌! ❜ 🌙⤹🌸",
    "❍⏤‌‌●!●───♫▷"
]

@app.on_message(filters.text)
async def insert_name(client, message):
    name = message.text.strip()
    if not name:
        await message.reply("Please send a name.")
        return

    # Pick a random font from the list
    font = fonts[0]  # You can randomize this if you prefer

    # Insert the name in the middle of the font
    mid_point = len(font) // 2
    new_text = font[:mid_point] + name + font[mid_point:]

    # Send the modified text back
    await message.reply(new_text)


if __name__ == "__main__":
    try:
        logger.info("Starting Pyrogram client...")
        app.run()
    except Exception as e:
        logger.error(f"Failed to start Pyrogram client: {str(e)}")
