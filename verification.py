import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens, is_verified_user  # Ensure `is_verified_user` checks verification status

def generate_short_link(user_id):
    """Generate a shortened verification link for the user."""
    url = f"https://yourdomain.com/verify?user={user_id}"
    try:
        response = requests.get(f"{Config.SHORTENER_URL}?api={Config.SHORTENER_API}&url={url}")
        if response.status_code == 200:
            return response.json().get("shortenedUrl")
        else:
            print(f"Error generating short link: {response.text}")
            return None
    except Exception as e:
        print(f"Short link generation failed: {e}")
        return None

async def send_verification_link(bot, message):
    """Send a verification link to the user."""
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
    
    await message.reply_text("🔹 Complete verification to get **15 tokens**.", reply_markup=keyboard)

async def check_verification(bot, query):
    """Check if the user has completed verification."""
    user_id = int(query.data.split("_")[-1])

    if is_verified_user(user_id):  # Check verification from the database
        add_tokens(user_id, 15)
        await query.message.edit_text("✅ **Verification successful!** You received **15 tokens**.")
    else:
        await query.answer("❌ Not verified yet. Complete the verification and try again.", show_alert=True)
