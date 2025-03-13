from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("premium"))
async def show_pricing(client, message):
    text = "💎 **Premium Plans**\n\n"
    for price, tokens in Config.TOKEN_PRICING.items():
        text += f"• ₹{price} → {tokens} tokens\n"
    
    text += "\n💳 Payment methods:"
    
    buttons = [
        [InlineKeyboardButton("📲 UPI Payment", url=f"upi://pay?pa={Config.PAYMENT_UPI}")],
        [InlineKeyboardButton("📸 QR Code", url=Config.PAYMENT_QR)]
    ]
    
    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
