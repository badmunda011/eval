import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Pyrogram Bot API
API_ID = "16457832"
API_HASH = "3030874d0befdb5d05597deacc3e83ab"
BOT_TOKEN = "7502185711:AAHVIGXxrRLb0WUyR606njxpRS2vz-jOduM"
OWNER_ID = 7009601543

app = Client(
    name="EVAL",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

fonts = {
    "smallcap": "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "monospace": "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚝𝚕𝚖𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶ℍ𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉",
    "outline": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐𝕑",
    "script": "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪ℙ𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
    "bold": "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗓",
    "bolditalic": "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"
}

names_list = [
    "ᯓ𓆰 𝅃.™ ٭ - 𓆪ꪾ⌯ 🜲 ˹ 𝐎ᴘ ˼",
    "❛ .𝁘ໍ.𓆪ִֶָ ֺ⎯꯭‌ 𓆩💗𓆪𓈒",
    "➺ ‌⃪⃜ .✦ 𝆺𝅥⎯ꨄ",
    "ᯓ𓆰𝅃🔥.⃪⍣꯭꯭𓆪꯭🝐",
    "🤍 ⍣⃪͜ ᶦ ͢ᵃᵐ⛦⃕‌.❛𝆺𝅥⤹࿗𓆪ꪾ™",
    "⋆⎯፝֟፝֟⎯᪵ 𝆺꯭𝅥. ᭄꯭🦋꯭᪳᪳᪻⎯̽⎯🐣",
    "🍹𝆺𝅥⃝🤍 ⃪ͥ͢ ᷟ●.🤍᪳𝆺꯭𝅥⎯꯭̽⎯꯭",
    "𓆰⎯꯭꯭֯‌⌯ .𓂃ֶꪳ 𓆩〭〬🔥𓆪ꪾ",
    "𓆰𓏲.𓂃ֶꪳ 𓆩〭〬🦋𓆪ꪾ",
    "𓆰𝅃꯭᳚𓄂️𝆺𝅥⃝🔥 ⃪ͥ͢ ᷟ𓆩 ! 乛|⁪⁬⁮⁮⁮⁮ ‌⁪⁬𓆪🐼™",
    "❛ .𝁘ໍ!𓆪ִֶָ ֺ⎯꯭‌ 𓆩💗𓆪𓈒",
    "ᯓ𓆰𝅃🔥!⃪⍣꯭꯭𓆪꯭🝐",
    "❛ .𝁘ໍ.ꨄ 🦋𓂃•",
    "⟶̽ꭙ⋆🔥𓆩〬 !🤍᪳𝆺꯭𝅥⎯᳝֟፝֟⎯‌",
    "⋆─፝─᪵།‌꯭! ا۬͢𝆺𝅥⃝🌸𝄄꯭꯭𝄄꯭꯭ ̶꯭𝅥ͦ𝆬👑",
    "🍹𝆺𝅥⃝🤍 ⃪ͥ͢ ᷟ●!🤍᪳𝆺꯭𝅥⎯꯭̽⎯꯭",
    "❛ .𝁘ໍ!ꨄ 🦋𓂃•"
]

@app.on_message(filters.text)
async def font_ubot(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("Fonts", callback_data=f"fonts|{message.text}")],
        [InlineKeyboardButton("Names", callback_data=f"names|{message.text}")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply("Choose an option:", reply_markup=reply_markup)

@app.on_callback_query()
async def on_callback_query(client: Client, callback_query):
    data = callback_query.data
    option, text = data.split('|')

    if option == "names":
        for name in names_list:
            await callback_query.message.reply(f"{name} {text}")

if __name__ == "__main__":
    try:
        logger.info("Starting Pyrogram client...")
        app.run()
    except Exception as e:
        logger.error(f"Failed to start Pyrogram client: {str(e)}")
