import logging
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_files, save_file, get_tokens, deduct_token
from verification import send_verification_link, check_verification
from config import Config
from premium import premium_info
from admin import add_tokens_admin

# ===== Flask Server for Health Checks =====
app = Flask(__name__)

@app.route("/")
def health_check():
    return "🤖 Bot Server Running", 200

# ===== Pyrogram Bot Setup =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = Client(
    "AnimeFilterBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# ===== Handlers =====

# ... (previous imports and setup code)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    try:
        buttons = [
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("📢 Support", url="https://t.me/yourgroup")],
            [InlineKeyboardButton("✅ Verify", callback_data="verify"),
             InlineKeyboardButton("💰 Premium", callback_data="premium")]
        ]
        await message.reply_text(  # Fixed parenthesis
            "👋 Welcome! Use me to search and share files.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )  # Added this closing parenthesis
    except Exception as e:
        logging.error(f"Start handler error: {e}")

@bot.on_message(filters.text & filters.group)
async def search_handler(client, message):
    try:
        query = message.text.strip()
        results = get_files(query)
        
        if not results:
            await message.reply_text("❌ No files found matching your query.")
            return

        buttons = [
            [InlineKeyboardButton(
                doc["file_name"], 
                callback_data=f"file_{doc['file_id']}"
            ) for doc in results[:10]
        ]
        
        if len(results) > 10:
            buttons.append(
                [InlineKeyboardButton("Next ➡️", callback_data=f"next_{query}_1")]
            )

        await message.reply_text(  # Fixed parenthesis
            f"🔍 Found {len(results)} results:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )  # Added this closing parenthesis
    except Exception as e:
        logging.error(f"Search error: {e}")

# ... (rest of the code remains the same)

@bot.on_callback_query(filters.regex(r"^file_(.+)"))
async def file_handler(client, query):
    try:
        user_id = query.from_user.id
        file_id = query.matches[0].group(1)
        
        if get_tokens(user_id) > 0:
            deduct_token(user_id)
            await bot.send_document(user_id, file_id)
            await query.answer("📁 File sent to your PM!", show_alert=True)
        else:
            await send_verification_link(bot, query.message)
    except Exception as e:
        logging.error(f"File handler error: {e}")
        await query.answer("❌ Failed to send file", show_alert=True)

@bot.on_callback_query(filters.regex("help"))
async def help_handler(client, query):
    help_text = (
        "🆘 **Help Guide**\n\n"
        "• Search files in groups using keywords\n"
        "• Each download costs 1 token\n"
        "• Get free tokens via verification\n"
        "• Buy more tokens with /premium"
    )
    await query.message.edit_text(help_text)

@bot.on_callback_query(filters.regex("verify"))
async def verify_handler(client, query):
    await send_verification_link(bot, query.message)

@bot.on_callback_query(filters.regex("premium"))
async def premium_handler(client, query):
    await premium_info(bot, query.message)

@bot.on_message(filters.document & filters.private)
async def store_file_handler(client, message):
    try:
        file_id = message.document.file_id
        file_name = message.document.file_name
        save_file(file_id, file_name)
        await message.reply("✅ File successfully added to database!")
    except Exception as e:
        logging.error(f"File storage error: {e}")
        await message.reply("❌ Failed to store file")

# ===== Startup =====
if __name__ == "__main__":
    # Start Flask server
    threading.Thread(
        target=app.run,
        kwargs={"host": "0.0.0.0", "port": 8000},
        daemon=True
    ).start()
    
    # Start Pyrogram bot
    bot.run()
