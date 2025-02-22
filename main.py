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
_monospace = "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚝𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶ℍ𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉"
_outline = "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐𝕑"
_script = "𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪ℙ𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
_blackbubbles = "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"
_bubbles = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"
_bold = "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗓"
_bolditalic = "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"

names_list = [
    "⏤‌͢✶❥‌𝄟⃟͢👑꯭ꯨ🆅꯭ꯨ𝝸𝝼꯭͠ꯨ𝝰꯭𝝰͠ꯨ𝝶᭄ 𝆺𝅥⃝♥️𝄟❥↲꧍",
    "ᯓ𓆰𝅃꯭᳚🦁𝛥꯭ɴ꯭ɴ꯭ᴏ꯭ɴ꯭˶꯭꯭꯭꯭꯭꯭֟፝͟͝ ⚡꯭꯭꯭꯭꯭",
    "➺꯭ ꯭𝅥‌꯭𝆬‌🦋⃪꯭ ─⃛͢┼ 𝞄⃕𝖋𝖋 𝛥꯭ɴ꯭ɴ꯭ᴏ꯭ɴ꯭🥵⃝⃝ᬽ꯭ ⃪꯭ ꯭𝅥‌꯭𝆬‌➺꯭⎯⎯᪵᪳",
    "🤍 ⍣⃪͜ ᶦ ͢ᵃᵐ⛦⃕‌!❛𝆺𝅥⤹࿗𓆪ꪾ™",
    "𓆰𓏲𝛥꯭ɴ꯭ɴ꯭ᴏ꯭ɴ꯭𓂃ֶꪳ 𓆩〭〬🦋𓆪ꪾ",
    "◄❥‌‌❥ ⃝⃪⃕🦚⟵᷽᷍𝛥꯭ɴ꯭ɴ꯭ᴏ꯭ɴ꯭˚‌‌‌‌◡‌⃝🐬᪳ ‌⃪𔘓❁‌‌❍•:➛"
]

def gen_font(text, new_font):
    if len(text.split()) > 10:
        return text
    new_font = " ".join(new_font).split()
    for q in text:
        if q in _default:
            new = new_font[_default.index(q)]
            text = text.replace(q, new)
    return text

@app.on_message(filters.text & ~filters.forwarded & ~filters.via_bot)
async def font_ubot(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("Fonts", callback_data="fonts|{}".format(message.text))],
        [InlineKeyboardButton("Names", callback_data="names|{}".format(message.text))]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply("Choose an option:", reply_markup=reply_markup)

@app.on_callback_query()
async def on_callback_query(client: Client, callback_query):
    data = callback_query.data
    option, text = data.split('|')
    if option == "fonts":
        buttons = []
        for i in range(0, len(fonts), 4):
            buttons.append([InlineKeyboardButton(font, callback_data=f"{font}|{text}") for font in fonts[i:i+4]])
        reply_markup = InlineKeyboardMarkup(buttons)
        await callback_query.message.reply("Choose a font:", reply_markup=reply_markup)
    elif option in fonts:
        if option == "smallcap":
            nan = gen_font(text, _smallcap)
        elif option == "monospace":
            nan = gen_font(text, _monospace)
        elif option == "outline":
            nan = gen_font(text, _outline)
        elif option == "script":
            nan = gen_font(text, _script)
        elif option == "blackbubbles":
            nan = gen_font(text, _blackbubbles)
        elif option == "bubbles":
            nan = gen_font(text, _bubbles)
        elif option == "bold":
            nan = gen_font(text, _bold)
        elif option == "bolditalic":
            nan = gen_font(text, _bolditalic)
        await callback_query.message.reply(nan)
    elif option == "names":
        for name in names_list:
            await callback_query.message.reply(name)

@app.on_message(filters.command("listfont") & ~filters.forwarded & ~filters.via_bot)
async def list_fonts(client: Client, message: Message):  
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
