import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_files, get_tokens, deduct_token
from verification import send_verification_link
from config import Config
from premium import premium_info
from admin import add_tokens_admin
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Client(
    "AutoFilterBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# ================== HANDLERS ================== #
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
            res["file_name"], 
            callback_data=f"file_{res['file_id']}"
        )] for res in results[:10]
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
            logger.error(f"File send error: {e}")
            await query.answer("❌ Failed to send file.", show_alert=True)
    else:
        await send_verification_link(bot, query.message)

@bot.on_callback_query(filters.regex("help"))
async def show_help(client, query):
    text = (
        "🆘 **Help**\n\n"
        "• Search files in groups\n"
        "• Use /tokens to check balance\n"
        "• Verify to get free tokens\n"
        "• Buy tokens via /premium"
    )
    await query.message.edit_text(text)

@bot.on_callback_query(filters.regex("verify"))
async def trigger_verify(client, query):
    await send_verification_link(bot, query.message)

@bot.on_callback_query(filters.regex("premium"))
async def show_premium(client, query):
    await premium_info(bot, query.message)

if __name__ == "__main__":
    bot.run()
