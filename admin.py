from pyrogram import Client, filters  # Added "Client" here
from database import add_tokens
from config import Config
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("addtokens") & filters.user(Config.ADMINS))
async def add_tokens_admin(client, message):
    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except:
        await message.reply_text("❌ Usage: /addtokens <user_id> <positive_number>")
        return
    
    try:
        add_tokens(user_id, amount)
        await message.reply_text(f"✅ Added {amount} tokens to {user_id}")
    except Exception as e:
        logger.error(f"Admin token error: {e}")
        await message.reply_text("❌ Failed to add tokens")
