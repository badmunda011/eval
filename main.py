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

fonts = {
    "smallcap": "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "monospace": "𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏𝚊𝚋𝚌𝚍𝚎𝚏",
    "outline": "𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗𝕒𝕓𝕔𝕕𝕖𝕗",
    "script": "𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻𝒶𝒷𝒸𝒹𝑒𝒻",
    "bold": "𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳𝗮𝗯𝗰𝗱𝗲𝗳",
    "bolditalic": "𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛𝙖𝙗𝙘𝙙𝙚𝙛"
}

names_list = [
    "❛ .𝁘ໍ.𓆪ִֶָ ֺ⎯꯭‌ 𓆩💗𓆪𓈒",
    "➺ ‌⃪⃜ .✦ 𝆺𝅥⎯ꨄ",
    "ᯓ𓆰𝅃🔥.⃪⍣꯭꯭𓆪꯭🝐",
    "🤍 ⍣⃪͜ ᶦ ͢ᵃᵐ⛦⃕‌.❛𝆺𝅥⤹࿗𓆪ꪾ™",
    "⋆⎯፝֟፝֟⎯᪵ 𝆺꯭𝅥. ᭄꯭🦋꯭᪳᪳᪻⎯̽⎯🐣",
    "𓆰⎯꯭꯭֯‌⌯ .𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ",
    "𓆰𝅃꯭᳚𓄂️𝆺𝅥⃝🔥 ⃪ͥ͢ ᷟ𓆩 ! 乛|⁪⁬⁮⁮⁮⁮⁮ ‌⁪⁬𓆪🐼™",
]

def apply_font(text, font):
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(font) != len(normal):
        raise ValueError("Font length must be equal to the length of the normal alphabet")
    translation = str.maketrans(normal, font)
    return text.translate(translation)

def create_styled_text(user_text):
    words = user_text.split()
    if not words:
        return user_text

    styled_words = []
    for word in words:
        random_font = random.choice(list(fonts.values()))
        styled_word = apply_font(word, random_font)
        styled_words.append(styled_word)

    return " ".join(styled_words)

def create_random_designs(user_text):
    words = user_text.split()
    if not words:
        return user_text

    styled_variations = []
    for _ in range(3):  # 3 Different Styled Variants
        random_name = random.choice(names_list)
        modified_name = random_name.replace(".", random.choice(words), 1)
        styled_variations.append(modified_name)

    return "\n".join(styled_variations)

@app.on_message(filters.text)
async def font_ubot(client: Client, message: Message):
    styled_text = create_styled_text(message.text)
    design_variations = create_random_designs(message.text)

    buttons = [
        [InlineKeyboardButton("Fonts", callback_data=f"fonts|{message.text}")],
        [InlineKeyboardButton("Names", callback_data=f"names|{message.text}")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    reply_msg = f"**Styled Text:**\n{styled_text}\n\n**Design Variations:**\n{design_variations}"
    await message.reply(reply_msg, reply_markup=reply_markup)

@app.on_callback_query()
async def on_callback_query(client: Client, callback_query):
    data = callback_query.data
    option, text = data.split('|')

    if option == "fonts":
        styled_text = create_styled_text(text)
        await callback_query.message.reply(f"**Styled Text:**\n{styled_text}")

    elif option == "names":
        design_variations = create_random_designs(text)
        await callback_query.message.reply(f"**Design Variations:**\n{design_variations}")

if __name__ == "__main__":
    try:
        logger.info("Starting Pyrogram client...")
        app.run()
    except Exception as e:
        logger.error(f"Failed to start Pyrogram client: {str(e)}")
