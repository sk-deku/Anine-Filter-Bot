from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
import logging

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("premium"))
async def premium_info(client, message):  # Renamed from "show_pricing" to "premium_info"
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
    )
