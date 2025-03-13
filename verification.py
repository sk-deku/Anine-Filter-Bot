import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens

def generate_short_link(user_id):
    url = f"https://yourdomain.com/verify?user={user_id}"
    try:
        response = requests.get(f"{Config.SHORTENER_URL}?api={Config.SHORTENER_API}&url={url}")
        response.raise_for_status()
        return response.json().get("shortenedUrl")
    except Exception as e:
        print(f"Shortener API error: {e}")
        return None

async def send_verification_link(bot, message):
    user_id = message.from_user.id
    short_link = generate_short_link(user_id)
    
    if not short_link:
        await message.reply_text("❌ Failed to generate verification link. Please try again later.")
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Verify Now", url=short_link)],
        [InlineKeyboardButton("✅ I've Completed", callback_data=f"check_verification_{user_id}")],
        [InlineKeyboardButton("📖 How to Verify?", url="https://your-tutorial-link.com")]
    ])
    
    await message.reply_text("🔹 Complete verification to get 15 tokens.", reply_markup=keyboard)

async def check_verification(bot, query):
    user_id = int(query.matches[0].group(1))
    if is_user_verified(user_id):  # Implement this function
        add_tokens(user_id, 15)
        await query.message.edit_text("✅ Verification successful! You got 15 tokens.")
    else:
        await query.answer("❌ Not verified yet.", show_alert=True)
