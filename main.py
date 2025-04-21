from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultCachedAudio, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from uuid import uuid4
from Config import API_ID, API_HASH, BOT_TOKEN, MONGO_URL

# MongoDB client setup
client = MongoClient(MONGO_URL)
db = client['audio_bot']
collection = db['audios']

# Pyrogram bot client
app = Client(
    "audio_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("Send me an audio file to save and vote on others!")

# Save audio
@app.on_message(filters.audio & filters.private)
async def handle_audio(client, message):
    audio = message.audio
    if not audio:
        await message.reply_text("Please send a valid audio file.")
        return

    if not audio.mime_type or not audio.mime_type.startswith("audio/"):
        await message.reply_text("Only audio files (like MP3) are supported.")
        return

    entry = {
        "file_id": audio.file_id,
        "title": audio.title or f"Audio-{str(uuid4())[:8]}",
        "votes": 0,
        "mime_type": audio.mime_type
    }
    inserted = collection.insert_one(entry)

    buttons = [[InlineKeyboardButton("Vote", callback_data=f"vote:{str(inserted.inserted_id)}")]]
    await message.reply_audio(
        audio.file_id,
        caption=f"Title: {entry['title']}\nVotes: 0",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Vote button handler
@app.on_callback_query()
async def handle_vote(client, callback_query):
    data = callback_query.data
    if data and data.startswith("vote:"):
        audio_id = data.split(":")[1]
        audio = collection.find_one({"_id": ObjectId(audio_id)})

        if not audio:
            await callback_query.message.edit("Audio not found or has been removed.")
            return

        collection.update_one({"_id": ObjectId(audio_id)}, {"$inc": {"votes": 1}})
        updated = collection.find_one({"_id": ObjectId(audio_id)})

        await callback_query.message.edit_caption(
            caption=f"Title: {updated['title']}\nVotes: {updated['votes']}",
            reply_markup=callback_query.message.reply_markup
        )

# Inline query handler
from bson import ObjectId  # Ensure to import ObjectId for MongoDB operations

@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    query = inline_query.query.lower()
    results = []

    for audio in collection.find():
        # Validate audio file_id and MIME type
        if audio.get("file_id") and audio.get("mime_type", "").startswith("audio/"):
            try:
                # Test sending the file to ensure validity (optional, for debugging)
                await client.get_messages(chat_id=inline_query.from_user.id, message_ids=audio["file_id"])
                # Append valid results
                results.append(
                    InlineQueryResultCachedAudio(
                        id=str(uuid4()),
                        audio_file_id=audio["file_id"],
                        caption=f"Title: {audio['title']}\nVotes: {audio['votes']}"
                    )
                )
            except Exception as e:
                # Log invalid file_ids for debugging
                print(f"Invalid audio file_id: {audio['file_id']} - Error: {e}")

    await inline_query.answer(results, cache_time=1)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
