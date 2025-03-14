import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

bot = Client(
    "FileIndexBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# ================== Indexing Handler ================== #
@bot.on_message(filters.chat(Config.INDEX_CHANNEL) & 
               (filters.document | filters.video | filters.audio))
async def index_file(client, message):
    try:
        file_type = None
        if message.document:
            file_type = "document"
            file_id = message.document.file_id
            file_name = message.document.file_name
        elif message.video:
            file_type = "video"
            file_id = message.video.file_id
            file_name = message.video.file_name
        elif message.audio:
            file_type = "audio"
            file_id = message.audio.file_id
            file_name = message.audio.file_name

        file_data = {
            'file_id': file_id,
            'file_name': file_name,
            'caption': message.caption.html if message.caption else "",
            'file_type': file_type,
            'date': message.date,
            'channel_id': Config.MAIN_CHANNEL
        }

        if db.save_file(file_data):
            await message.reply_text("✅ File indexed successfully!")
        else:
            await message.reply_text("❌ Failed to index file!")

    except Exception as e:
        logging.error(f"Indexing error: {e}")

# ================== Search Handler ================== #
@bot.on_message(filters.command("search") & filters.group)
async def search_files(client, message):
    try:
        query = message.text.split(" ", 1)[1]
        page = 1
        
        results = db.search_files(query, page)
        total = db.get_total_results(query)
        
        if not results:
            return await message.reply_text("❌ No results found!")

        buttons = []
        for file in results:
            btn = [InlineKeyboardButton(
                f"📁 {file['file_name']}",
                callback_data=f"file_{file['file_id']}"
            )]
            buttons.append(btn)

        # Add pagination if needed
        if total > Config.RESULTS_PER_PAGE:
            buttons.append([
                InlineKeyboardButton("⬅️ Previous", callback_data=f"prev_{query}_{page}"),
                InlineKeyboardButton(f"Page {page}", callback_data="ignore"),
                InlineKeyboardButton("Next ➡️", callback_data=f"next_{query}_{page}")
            ])

        await message.reply_text(
            f"🔍 Found {total} results for '{query}':\n\n"
            f"📄 Showing page {page} ({len(results)} results)",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except IndexError:
        await message.reply_text("❗ Please provide a search query\nUsage: `/search query`")
    except Exception as e:
        logging.error(f"Search error: {e}")
        await message.reply_text("❌ An error occurred during search!")
# ... (previous imports and setup code)

# ================== File Request Handler ================== #
@bot.on_callback_query(filters.regex(r"^(file|prev|next)_"))
async def handle_callbacks(client, callback_query):
    try:
        data = callback_query.data.split("_")
        if len(data) < 3 and data[0] != "file":
            return await callback_query.answer("Invalid request!")

        action = data[0]

        if action == "file":
            file_id = data[1]
            try:
                await client.send_cached_media(
                    chat_id=callback_query.message.chat.id,
                    file_id=file_id
                )
                await callback_query.answer()
            except Exception as e:
                await callback_query.answer("❌ File not available!", show_alert=True)
                logging.error(f"File send error: {e}")

        elif action in ["prev", "next"]:
            query = data[1]
            page = int(data[2])
            new_page = page - 1 if action == "prev" else page + 1

            results = db.search_files(query, new_page)
            total = db.get_total_results(query)

            if not results:
                return await callback_query.answer("No more results!", show_alert=True)

            buttons = []
            for file in results:
                btn = [InlineKeyboardButton(
                    f"📁 {file['file_name']}",
                    callback_data=f"file_{file['file_id']}"
                )]
                buttons.append(btn)

            if total > Config.RESULTS_PER_PAGE:
                pagination = []
                if new_page > 1:
                    pagination.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"prev_{query}_{new_page}"))
                
                pagination.append(InlineKeyboardButton(f"Page {new_page}", callback_data="ignore"))
                
                if (new_page * Config.RESULTS_PER_PAGE) < total:
                    pagination.append(InlineKeyboardButton("Next ➡️", callback_data=f"next_{query}_{new_page}"))
                
                buttons.append(pagination)

            await callback_query.message.edit_reply_markup(
                InlineKeyboardMarkup(buttons)
            await callback_query.answer()

    except IndexError:
        await callback_query.answer("Invalid request!", show_alert=True)
    except Exception as e:
        logging.error(f"Callback error: {e}")
        await callback_query.answer("❌ Error processing request!", show_alert=True)

# ... (rest of the code)
if __name__ == "__main__":
    bot.run()
