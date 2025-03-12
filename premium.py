from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens, get_user_tokens  # Ensure these functions are implemented
import os

# Payment Details
PAYMENT_UPI = Config.PAYMENT_UPI
PAYMENT_QR = Config.PAYMENT_QR
TOKEN_PRICING = Config.TOKEN_PRICING  # Pricing dictionary

# 💎 Command: /premium (Shows pricing and payment options)
@Client.on_message(filters.command("premium"))
async def premium_info(client, message):
    pricing_text = "**💎 Premium Token Pricing 💎**\n\n"
    for price, tokens in TOKEN_PRICING.items():
        pricing_text += f"💰 **₹{price}** → {tokens} Tokens\n"
    
    pricing_text += "\n✅ **Send payment screenshot to the admin to get tokens!**"

    # Payment buttons
    buttons = [InlineKeyboardButton("📥 Pay via UPI", url=f"upi://pay?pa={PAYMENT_UPI}")]

    if PAYMENT_QR:
        buttons.insert(0, [InlineKeyboardButton("📸 Scan QR to Pay", url=PAYMENT_QR)])

    await message.reply_text(pricing_text, reply_markup=InlineKeyboardMarkup(buttons))


# 🛠️ Command: /addtokens (Admin only - Adds tokens to a user)
@Client.on_message(filters.command("addtokens") & filters.user(Config.ADMINS))
async def add_tokens_admin(client, message):
    args = message.text.split()
    if len(args) < 3:
        return await message.reply_text("⚠️ Usage: `/addtokens user_id token_amount`")

    user_id = int(args[1])
    token_amount = int(args[2])

    add_tokens(user_id, token_amount)
    await message.reply_text(f"✅ **Added {token_amount} tokens to User ID {user_id}!**")


# 📝 Command: /tokens (User checks remaining tokens)
@Client.on_message(filters.command("tokens"))
async def check_tokens(client, message):
    user_id = message.from_user.id
    tokens = get_user_tokens(user_id)
    await message.reply_text(f"🎟️ **You have {tokens} tokens left.**\n\nEach file download costs **1 token**.")
