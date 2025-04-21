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
from bson.objectid import ObjectId  # Import for MongoDB ObjectId handling

# MongoDB client setup
client = MongoClient(MONGO_URL)
db = client['audio_bot']
collection = db['audios']

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an audio to add it and vote for others!")

# Save audio
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    audio = update.message.audio
    if not audio:
        await update.message.reply_text("Please send a valid audio file.")
        return

    # Save to DB with a default title if not provided
    entry = {
        "file_id": audio.file_id,
        "title": audio.title or f"Audio-{str(uuid4())[:8]}",  # Default title with unique ID
        "votes": 0
    }
    inserted = collection.insert_one(entry)

    buttons = [[InlineKeyboardButton("Vote", callback_data=f"vote:{str(inserted.inserted_id)}")]]
    await update.message.reply_audio(
        audio.file_id,
        caption=f"Title: {entry['title']}\nVotes: 0",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Handle vote
async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    audio_id = query.data.split(":")[1]

    try:
        # Find the audio document
        audio = collection.find_one({"_id": ObjectId(audio_id)})
        if not audio:
            await query.edit_message_text("Audio not found or has been removed.")
            return

        # Increment votes
        collection.update_one({"_id": ObjectId(audio_id)}, {"$inc": {"votes": 1}})
        audio = collection.find_one({"_id": ObjectId(audio_id)})  # Fetch updated audio

        await query.edit_message_caption(
            caption=f"Title: {audio['title']}\nVotes: {audio['votes']}",
            reply_markup=query.message.reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"An error occurred: {e}")

# Inline query handler
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()
    results = []

    for audio in collection.find():
        if query in audio['title'].lower():  # Match query with title
            if audio.get("file_id"):  # Ensure file_id exists
                results.append(
                    InlineQueryResultCachedAudio(
                        id=str(uuid4()),
                        audio_file_id=audio["file_id"],
                        caption=f"Title: {audio['title']}\nVotes: {audio['votes']}"  # Show title and votes
                    )
                )

    # If no results match, return an empty response
    if not results:
        await update.inline_query.answer([], cache_time=1)
        return

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

# Fix for already running event loop
if __name__ == "__main__":
    import nest_asyncio
    import asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
