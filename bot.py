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
    return "Bot Server Running", 200

# ===== Pyrogram Bot =====
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
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("📚 Help", callback_data="help"),
         InlineKeyboardButton("📢 Support", url="https://t.me/yourgroup")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify"),
         InlineKeyboardButton("💰 Premium", callback_data="premium")]
    ]
    await message.reply_text(
        "👋 Hi! I'm your file search bot.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_message(filters.text & filters.group)
async def handle_search(client, message):
    query = message.text.strip()
    results = get_files(query)
    
    if not results:
        await message.reply_text("❌ No files found.")
        return

    buttons = [
        [InlineKeyboardButton(
            doc["file_name"], 
            callback_data=f"file_{doc['file_id']}"
        )] for doc in results[:10]
    ]
    
    if len(results) > 10:
        buttons.append([InlineKeyboardButton("Next ➡️", callback_data=f"next_{query}_1")])

    await message.reply_text(
        f"🔍 Found {len(results)} files:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_callback_query(filters.regex(r"^file_(.+)"))
async def send_file(client, query):
    user_id = query.from_user.id
    file_id = query.matches[0].group(1)
    
    if get_tokens(user_id) > 0:
        try:
            deduct_token(user_id)
            await bot.send_document(user_id, file_id)
            await query.answer("📄 File sent to your DM!", show_alert=True)
        except Exception as e:
            logging.error(f"File send error: {e}")
            await query.answer("❌ Failed to send file.", show_alert=True)
    else:
        await send_verification_link(bot, query.message)

@bot.on_callback_query(filters.regex("help"))
async def show_help(client, query):
    text = (
        "🆘 **Help Menu**\n\n"
        "• Use me in groups to search files\n"
        "• Each download costs 1 token\n"
        "• Get tokens via /premium or verification"
    )
    await query.message.edit_text(text)

@bot.on_callback_query(filters.regex("verify"))
async def trigger_verify(client, query):
    await send_verification_link(bot, query.message)

@bot.on_callback_query(filters.regex("premium"))
async def show_premium(client, query):
    await premium_info(bot, query.message)

@bot.on_message(filters.document & filters.private)
async def store_file(client, message):
    try:
        file_id = message.document.file_id
        file_name = message.document.file_name
        save_file(file_id, file_name)
        await message.reply("✅ File added to database!")
    except Exception as e:
        logging.error(f"File storage error: {e}")

# ===== Start Services =====
if __name__ == "__main__":
    # Start Flask server
    threading.Thread(
        target=app.run,
        kwargs={"host": "0.0.0.0", "port": 8000}
    ).start()
    
    # Start bot
    bot.run()
