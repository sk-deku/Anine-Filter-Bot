from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import users, add_tokens
import requests
import logging

logger = logging.getLogger(__name__)

def is_user_verified(user_id):
    try:
        user = users.find_one({"user_id": user_id})
        return user.get("verified", False) if user else False
    except Exception as e:
        logger.error(f"Verification check error: {e}")
        return False

async def send_verification_link(bot, message):
    user_id = message.from_user.id
    try:
        verify_url = f"https://your-domain.com/verify?user={user_id}"
        params = {"api": Config.SHORTENER_API, "url": verify_url}
        response = requests.get(Config.SHORTENER_URL, params=params, timeout=10)
        short_url = response.json().get("shortenedUrl")
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Verify Now", url=short_url)],
            [InlineKeyboardButton("✅ Done", callback_data=f"check_verify_{user_id}")]
        ])
        await message.reply("🔒 Complete verification to get 15 tokens:", reply_markup=keyboard)
        
    except Exception as e:
        logger.error(f"Verification error: {e}")
        await message.reply("❌ Verification service unavailable. Try later.")

@Client.on_callback_query(filters.regex(r"^check_verify_(\d+)"))
async def verify_callback(client, query):
    try:
        user_id = int(query.matches[0].group(1))
        if is_user_verified(user_id):
            add_tokens(user_id, 15)
            users.update_one({"user_id": user_id}, {"$set": {"verified": True}})
            await query.message.edit_text("🎉 Verification successful! 15 tokens added.")
        else:
            await query.answer("❌ Complete verification steps first!", show_alert=True)
    except Exception as e:
        logger.error(f"Verification callback error: {e}")
