import os

class Config:
    API_ID = int(os.getenv("API_ID", "15072022"))  # Ensures API_ID is an integer
    API_HASH = os.getenv("API_HASH", "16b9f1767df306b369039fee1202970d")  # Should be a valid hash
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7204165447:AAEgaDNLMSdTkRT2NjxP4NcwFb6jAX07DXQ")  # Bot token from BotFather
    DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://AnimeFireBot: Skesavan7@cluster0.zu5mx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB connection URL
    SHORTENER_API = os.getenv("SHORTENER_API", "5a6b57d3cbd44e9b81cda3a2ec9d93024fcc6838")  # Your shortener API key
    SHORTENER_URL = os.getenv("SHORTENER_URL", "http://modijiurl.com")  # Your shortener site URL
    ADMINS = list(map(int, os.getenv("ADMINS", "1775977570").split()))  # List of admin user IDs
    PAYMENT_UPI = os.getenv("PAYMENT_UPI", "sivakumar089356@oksbi")  # UPI ID for payments
    PAYMENT_QR = os.getenv("PAYMENT_QR", "https://graph.org/file/3c17f2014b6c468b108df-01888ecfbde40c16bf.jpg")  # QR code URL for payments

    # Pricing for Premium Tokens (₹ → Tokens)
    TOKEN_PRICING = {
        20: 50,   # ₹20 → 50 Tokens
        35: 100,  # ₹35 → 100 Tokens
        45: 150,  # ₹45 → 150 Tokens
        60: 300   # ₹60 → 300 Tokens
    }
