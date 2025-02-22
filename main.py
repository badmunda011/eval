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

arguments = [
    "smallcap",
    "monospace",
    "outline",
    "script",
    "blackbubbles",
    "bubbles",
    "bold",
    "bolditalic"
]

fonts = [
    "smallcap",
    "monospace",
    "outline",
    "script",
    "blackbubbles",
    "bubbles",
    "bold",
    "bolditalic"
]

_default = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_smallcap = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘϙʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
_monospace = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶ℍ𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
_outline = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
_script = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪ℙ𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
_blackbubbles = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
_bubbles = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
_bold = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝘝𝘞𝘟𝘠𝘡"
_bolditalic = "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"

def gen_font(text, new_font):
    new_font = " ".join(new_font).split()
    for q in text:
        if q in _default:
            new = new_font[_default.index(q)]
            text = text.replace(q, new)
    return text

@app.on_message(filters.text & ~filters.forwarded & ~filters.via_bot)
async def font_ubot(client: Client, message: Message):
    buttons = []
    for i in range(0, len(fonts), 4):
        buttons.append([InlineKeyboardButton(font, callback_data=f"{font}|{message.text}") for font in fonts[i:i+4]])
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply("Choose a font:", reply_markup=reply_markup)

@app.on_callback_query()
async def on_callback_query(client: Client, callback_query):
    data = callback_query.data
    font, text = data.split('|')
    if font == "smallcap":
        nan = gen_font(text, _smallcap)
    elif font == "monospace":
        nan = gen_font(text, _monospace)
    elif font == "outline":
        nan = gen_font(text, _outline)
    elif font == "script":
        nan = gen_font(text, _script)
    elif font == "blackbubbles":
        nan = gen_font(text, _blackbubbles)
    elif font == "bubbles":
        nan = gen_font(text, _bubbles)
    elif font == "bold":
        nan = gen_font(text, _bold)
    elif font == "bolditalic":
        nan = gen_font(text, _bolditalic)
    await callback_query.message.reply(nan)

@app.on_message(filters.command("listfont") & ~filters.forwarded & ~filters.via_bot)
async def list_fonts(client: Client, message: Message):  # Renamed function
    await message.reply(
        "<b>ᴅᴀғᴛᴀʀ ғᴏɴᴛs</b>\n\n"
        "<b>• smallcap</b>\n"
        "<b>• monospace</b>\n"
        "<b>• outline</b>\n"
        "<b>• script</b>\n"
        "<b>• blackbubbles</b>\n"
        "<b>• bubbles</b>\n"
        "<b>• bold</b>\n"
        "<b>• bolditalic</b>\n\n"
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
