from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedAudio
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    InlineQueryHandler, ContextTypes, filters
)
from pymongo import MongoClient
from uuid import uuid4
from Config import BOT_TOKEN, MONGO_URL
import asyncio

# MongoDB client setup
client = MongoClient(MONGO_URL)
db = client['audio_bot']
collection = db['audios']

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an audio to add it and vote others!")

# Save audio
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    if not audio:
        return

    # Save to DB
    entry = {
        "file_id": audio.file_id,
        "title": audio.title or "Untitled Audio",
        "votes": 0
    }
    inserted = collection.insert_one(entry)

    buttons = [[InlineKeyboardButton("Vote", callback_data=f"vote:{str(inserted.inserted_id)}")]]
    await update.message.reply_audio(audio.file_id, caption="Votes: 0", reply_markup=InlineKeyboardMarkup(buttons))

# Handle vote
async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    audio_id = query.data.split(":")[1]

    collection.update_one({"_id": audio_id}, {"$inc": {"votes": 1}})
    audio = collection.find_one({"_id": audio_id})

    await query.edit_message_caption(
        caption=f"Votes: {audio['votes']}",
        reply_markup=query.message.reply_markup
    )

# Inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []

    for audio in collection.find():
        if query in audio['title'].lower():
            results.append(
                InlineQueryResultCachedAudio(
                    id=str(uuid4()),
                    audio_file_id=audio["file_id"],
                    title=audio["title"]
                )
            )
    await update.inline_query.answer(results, cache_time=1)

# Run bot
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(CallbackQueryHandler(handle_vote))
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot running...")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            # If the event loop is already running, run the coroutine directly
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
