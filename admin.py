from pyrogram import Client, filters
from database import add_tokens
from config import Config
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("addtokens") & filters.user(Config.ADMINS))
async def add_tokens_admin(client, message):
    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError
            
        user_id = int(args[1])
        amount = int(args[2])
        
        if amount <= 0:
            raise ValueError
            
        add_tokens(user_id, amount)
        await message.reply_text(f"✅ Added {amount} tokens to user {user_id}")
        
    except ValueError:
        await message.reply_text("❌ Invalid format. Use: /addtokens <user_id> <positive_number>")
    except Exception as e:
        logger.error(f"Admin command error: {e}")
        await message.reply_text("❌ Failed to add tokens")
