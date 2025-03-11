class Config:
    BOT_TOKEN = "your-bot-token"
    API_ID = "your-api-id"
    API_HASH = "your-api-hash"
    DATABASE_URL = "your-mongodb-url"
    ADMINS = [123456789, 987654321]  # Replace with Telegram Admin User IDs

    # Shortener API
    SHORTENER_API = "your-shortener-api-key"
    SHORTENER_URL = "https://yourshortener.com/api"

    # Premium System
    PAYMENT_QR = "your-gpay-qr-url"
    PAYMENT_UPI = "your-upi-id"
    PRICING = {
        20: 50,
        35: 100,
        45: 150,
        60: 300
    }
