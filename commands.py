from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from verification import send_verification_link

async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("📚 Help", callback_data="help"),
         InlineKeyboardButton("📢 Support", url="https://t.me/your-support-group")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify"),
         InlineKeyboardButton("💰 Buy Tokens", callback_data="premium")]
    ]
    await message.reply_text("👋 Welcome! Use me to find files easily.", reply_markup=InlineKeyboardMarkup(buttons))

async def help_command(client, message):
    help_text = (
        "📚 **Help Menu**\n"
        "🔍 Search for files by sending a message in groups.\n"
        "✅ Use /verify to get tokens for downloads.\n"
        "💰 Buy premium tokens using /premium.\n"
        "📢 Contact support if you need help."
    )
    await message.reply_text(help_text)

async def verify_command(client, message):
    """ Sends a verification link to the user. """
    await message.reply_text("🔗 Generating your verification link... Please wait.")
    
    # Call verification function
    success = await send_verification_link(client, message)
    
    if not success:
        await message.reply_text("⚠️ Failed to generate a verification link. Please try again later.")
