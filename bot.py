import threading
import http.server
import socketserver
from pyrogram import Client, filters
from database import get_files, get_tokens, deduct_token
from config import Config
from commands import start_command, help_command, verify_command  # Import commands

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

# Register Commands
bot.add_handler(filters.command("start") & filters.private, start_command)
bot.add_handler(filters.command("help") & filters.private, help_command)
bot.add_handler(filters.command("verify") & filters.private, verify_command)

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

# Start the bot and HTTP server
if __name__ == "__main__":
    # Start HTTP server in a separate thread
    threading.Thread(target=run_http_server, daemon=True).start()
    
    # Start Pyrogram Bot
    bot.run()
