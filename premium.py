from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import add_tokens

@bot.on_message(filters.command("premium") & filters.private)
async def premium_info(client, message):
    buttons = [[InlineKeyboardButton(f"💰 ₹{price} → {tokens} Tokens", callback_data=f"buy_{price}")]
               for price, tokens in Config.PRICING.items()]
    buttons.append([InlineKeyboardButton("📤 Send Payment Screenshot", callback_data="send_payment")])
    await message.reply_text("💎 Buy Tokens:", reply_markup=InlineKeyboardMarkup(buttons))

@bot.on_callback_query(filters.regex(r"buy_(\d+)"))
async def buy_tokens(client, query):
    price = int(query.matches[0].group(1))
    tokens = Config.PRICING.get(price)
    
    if tokens:
        await query.message.reply_text(f"💳 Pay **₹{price}** and send screenshot.\n\n"
                                       f"📌 UPI ID: `{Config.PAYMENT_UPI}`\n"
                                       f"📌 QR Code: {Config.PAYMENT_QR}")
    else:
        await query.answer("❌ Invalid option!", show_alert=True)

@bot.on_callback_query(filters.regex("send_payment"))
async def receive_payment(client, query):
    await query.message.reply_text("📤 Send your payment screenshot to an admin for verification.")
