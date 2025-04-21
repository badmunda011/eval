from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedAudio
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    InlineQueryHandler, ContextTypes, filters
)
from pymongo import MongoClient
from uuid import uuid4
from Config import BOT_TOKEN, MONGO_URL
import asyncio
from bson.objectid import ObjectId
import nest_asyncio

# MongoDB client setup
client = MongoClient(MONGO_URL)
db = client['audio_bot']
collection = db['audios']

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an audio file to save and vote on others!")

# Save audio
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    if not audio:
        await update.message.reply_text("Please send a valid audio file.")
        return

    if not audio.mime_type or not audio.mime_type.startswith("audio/"):
        await update.message.reply_text("Only audio files (like MP3) are supported.")
        return

    entry = {
        "file_id": audio.file_id,
        "title": audio.title or f"Audio-{str(uuid4())[:8]}",
        "votes": 0,
        "mime_type": audio.mime_type
    }
    inserted = collection.insert_one(entry)

    buttons = [[InlineKeyboardButton("Vote", callback_data=f"vote:{str(inserted.inserted_id)}")]]
    await update.message.reply_audio(
        audio.file_id,
        caption=f"Title: {entry['title']}\nVotes: 0",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Vote button handler
async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    audio_id = query.data.split(":")[1]

    audio = collection.find_one({"_id": ObjectId(audio_id)})
    if not audio:
        await query.edit_message_text("Audio not found or has been removed.")
        return

    collection.update_one({"_id": ObjectId(audio_id)}, {"$inc": {"votes": 1}})
    updated = collection.find_one({"_id": ObjectId(audio_id)})

    await query.edit_message_caption(
        caption=f"Title: {updated['title']}\nVotes: {updated['votes']}",
        reply_markup=query.message.reply_markup
    )

# Inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []

    for audio in collection.find():
        if query in audio['title'].lower():
            if audio.get("file_id") and audio.get("mime_type", "").startswith("audio/"):
                results.append(
                    InlineQueryResultCachedAudio(
                        id=str(uuid4()),
                        audio_file_id=audio["file_id"],
                        caption=f"Title: {audio['title']}\nVotes: {audio['votes']}"
                    )
                )

    await update.inline_query.answer(results, cache_time=1)

# Main bot runner
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(CallbackQueryHandler(handle_vote))
    app.add_handler(InlineQueryHandler(inline_query))
    print("Bot running...")
    await app.run_polling()

# Async fix
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
