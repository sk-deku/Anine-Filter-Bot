from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens, get_user_tokens
import os

@Client.on_message(filters.command("premium"))
async def premium_info(client, message):
    pricing_text = "**💎 Premium Token Pricing 💎**\n\n"
    for price, tokens in Config.TOKEN_PRICING.items():
        pricing_text += f"💰 **₹{price}** → {tokens} Tokens\n"
    
    pricing_text += "\n✅ **Send payment screenshot to the admin to get tokens!**"

    buttons = [InlineKeyboardButton("📥 Pay via UPI", url=f"upi://pay?pa={Config.PAYMENT_UPI}")]

    if Config.PAYMENT_QR:
        buttons.insert(0, [InlineKeyboardButton("📸 Scan QR to Pay", url=Config.PAYMENT_QR)])

    await message.reply_text(pricing_text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.command("addtokens") & filters.user(Config.ADMINS))
async def add_tokens_admin(client, message):
    args = message.text.split()
    if len(args) < 3:
        return await message.reply_text("⚠️ Usage: `/addtokens user_id token_amount`")

    try:
        user_id = int(args[1])
        token_amount = int(args[2])
        if token_amount <= 0:
            return await message.reply_text("⚠️ Token amount must be positive.")
    except ValueError:
        return await message.reply_text("⚠️ Invalid user_id or token_amount.")

    add_tokens(user_id, token_amount)
    await message.reply_text(f"✅ **Added {token_amount} tokens to User ID {user_id}!**")

@Client.on_message(filters.command("tokens"))
async def check_tokens(client, message):
    user_id = message.from_user.id
    tokens = get_user_tokens(user_id)
    await message.reply_text(f"🎟️ **You have {tokens} tokens left.**\n\nEach file download costs **1 token**.")
