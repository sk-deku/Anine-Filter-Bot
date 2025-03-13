import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens, users
import logging

logger = logging.getLogger(__name__)

def is_user_verified(user_id):
    user = users.find_one({"user_id": user_id})
    return user.get("verified", False) if user else False

def generate_short_link(user_id):
    try:
        url = f"https://yourdomain.com/verify?user={user_id}"
        params = {
            "api": Config.SHORTENER_API,
            "url": url
        }
        response = requests.get(
            Config.SHORTENER_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("shortenedUrl")
    except Exception as e:
        logger.error(f"Shortener error: {e}")
        return None

async def send_verification_link(bot, message):
    user_id = message.from_user.id
    short_url = generate_short_link(user_id)
    
    if not short_url:
        await message.reply_text("⚠️ Verification service unavailable. Try later.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Verify Now", url=short_url)],
        [InlineKeyboardButton("✅ Done", callback_data=f"check_verify_{user_id}")]
    ])
    
    await message.reply_text(
        "🔒 Verify to get 15 FREE tokens:",
        reply_markup=keyboard
    )

async def check_verification(bot, query):
    user_id = int(query.data.split("_")[-1])
    if is_user_verified(user_id):
        add_tokens(user_id, 15)
        users.update_one({"user_id": user_id}, {"$set": {"verified": True}})
        await query.message.edit_text("🎉 Verified! 15 tokens added.")
    else:
        await query.answer("❌ Complete verification first!", show_alert=True)
