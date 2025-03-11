import os

class Config:
    API_ID = int(os.getenv("API_ID", "0"))  # Ensures API_ID is an integer
    API_HASH = os.getenv("API_HASH", "")  # Should be a valid hash
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # Bot token from BotFather
    DATABASE_URL = os.getenv("DATABASE_URL", "")  # MongoDB connection URL
    SHORTENER_API = os.getenv("SHORTENER_API", "")  # Your shortener API key
    SHORTENER_URL = os.getenv("SHORTENER_URL", "")  # Your shortener site URL
    ADMINS = list(map(int, os.getenv("ADMINS", "").split()))  # List of admin user IDs
    PAYMENT_UPI = os.getenv("PAYMENT_UPI", "")  # UPI ID for payments
    PAYMENT_QR = os.getenv("PAYMENT_QR", "")  # QR code URL for payments

    # Pricing for Premium Tokens (₹ → Tokens)
    TOKEN_PRICING = {
        20: 50,   # ₹20 → 50 Tokens
        35: 100,  # ₹35 → 100 Tokens
        45: 150,  # ₹45 → 150 Tokens
        60: 300   # ₹60 → 300 Tokens
    }
