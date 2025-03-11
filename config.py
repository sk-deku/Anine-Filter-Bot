import os

class Config:
    # ✅ REQUIRED SETTINGS (Replace with your actual values)
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")  
    API_ID = int(os.getenv("API_ID", ""))  # Must be an integer
    API_HASH = os.getenv("API_HASH", "")

    # ✅ DATABASE (If using MongoDB)
    DATABASE_URL = os.getenv("DATABASE_URL", "")

    # ✅ FORCE SUBSCRIBE CHANNELS (Multiple channels supported)
    FSUB_CHANNELS = os.getenv("FSUB_CHANNELS", "").split(",")

    # ✅ PREMIUM SYSTEM SETTINGS
    PAYMENT_UPI = os.getenv("PAYMENT_UPI", "")  # Your UPI ID
    PAYMENT_QR = os.getenv("PAYMENT_QR", "")  # QR Image Link
    TOKEN_PRICING = {20: 50, 35: 100, 45: 150, 60: 300}  # ₹ → Tokens

    # ✅ SHORTENER API (For verification links)
    SHORTENER_API = os.getenv("SHORTENER_API", "")
    VERIFICATION_LINK = os.getenv("VERIFICATION_LINK", "")

    # ✅ ADMIN CONFIG
    ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))  # Admin IDs
