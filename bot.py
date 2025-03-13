import threading
import http.server
import socketserver
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_files, get_tokens, deduct_token
from verification import send_verification_link
from config import Config

# Initialize Pyrogram Bot
bot = Client("AutoFilterBot", bot_token=Config.BOT_TOKEN, api_id=int(Config.API_ID), api_hash=Config.API_HASH)

# Define HTTP Server Port
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

# Function to Start HTTP Server
def run_http_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP Server Running on Port {PORT}")
        httpd.serve_forever()

# ✅ START Command
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("📚 Help", callback_data="help"),
         InlineKeyboardButton("📢 Support", url="https://t.me/your-support-group")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify"),
         InlineKeyboardButton("💰 Buy Tokens", callback_data="premium")]
    ]
    await message.reply_text("👋 Welcome! Use me to find files easily.", reply_markup=InlineKeyboardMarkup(buttons))

# ✅ HELP Command
@bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    help_text = "🛠 **Bot Commands:**\n\n" \
                "/start - Start the bot\n" \
                "/help - Show this help message\n" \
                "/verify - Get verification link\n" \
                "/premium - Buy premium tokens\n"
    
    await message.reply_text(help_text)

# ✅ VERIFY Command (Now working!)
@bot.on_message(filters.command("verify") & filters.private)
async def verify_command(client, message):
    await send_verification_link(client, message)

# ✅ PREMIUM Command
@bot.on_message(filters.command("premium") & filters.private)
async def premium_command(client, message):
    payment_info = "💰 **Premium Token Prices:**\n\n" \
                   "₹20 → 50 tokens\n" \
                   "₹35 → 100 tokens\n" \
                   "₹45 → 150 tokens\n" \
                   "₹60 → 300 tokens\n\n" \
                   "**Send Payment Screenshot to Admin**"

    await message.reply_text(payment_info)

# ✅ FILE SEARCH in Groups
@bot.on_message(filters.text & filters.group)
async def search_files(client, message):
    query = message.text
    files = get_files(query)
    
    if not files:
        await message.reply_text("❌ No files found.")
        return

    buttons = [[InlineKeyboardButton(file, callback_data=f"get_{file}")] for file in files[:10]]

    if len(files) > 10:
        buttons.append([InlineKeyboardButton("➡️ Next", callback_data=f"next_{query}_1")])

    await message.reply_text("📂 **Matching Files:**", reply_markup=InlineKeyboardMarkup(buttons))

# ✅ SEND FILE Callback
@bot.on_callback_query(filters.regex(r"get_(.+)"))
async def send_file(client, query):
    user_id = query.from_user.id
    file_name = query.matches[0].group(1)
    
    if get_tokens(user_id) > 0:
        deduct_token(user_id)
        await bot.send_document(user_id, file_name)
        await query.answer("📂 File sent in DM!", show_alert=True)
    else:
        await send_verification_link(bot, query.message)

# ✅ CHECK VERIFICATION Callback
@bot.on_callback_query(filters.regex(r"check_verification_(\d+)"))
async def check_verification(client, query):
    from verification import check_verification  # Import dynamically
    await check_verification(client, query)

# Start the bot and HTTP server
if __name__ == "__main__":
    threading.Thread(target=run_http_server, daemon=True).start()
    bot.run()
