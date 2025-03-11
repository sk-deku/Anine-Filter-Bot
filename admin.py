from pyrogram import Client, filters
from config import Config
from database import add_tokens

@bot.on_message(filters.command("addtokens") & filters.user(Config.ADMINS))
async def add_tokens_admin(client, message):
    args = message.text.split()
    if len(args) < 3:
        await message.reply_text("Usage: `/addtokens <user_id> <amount>`")
        return

    user_id, amount = int(args[1]), int(args[2])
    add_tokens(user_id, amount)
    await message.reply_text(f"✅ Added {amount} tokens to {user_id}.")
