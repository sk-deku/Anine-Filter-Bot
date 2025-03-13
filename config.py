import os

class Config:
    # Mandatory environment variables (no defaults)
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Optional variables with defaults
    SHORTENER_API = os.getenv("SHORTENER_API", "5a6b57d3cbd44e9b81cda3a2ec9d93024fcc6838")
    SHORTENER_URL = os.getenv("SHORTENER_URL", "http://modijiurl.com")
    ADMINS = list(map(int, os.getenv("ADMINS", "1775977570").split())) if os.getenv("ADMINS") else []
    PAYMENT_UPI = os.getenv("PAYMENT_UPI", "sivakumar089356@oksbi")
    PAYMENT_QR = os.getenv("PAYMENT_QR", "https://graph.org/file/3c17f2014b6c468b108df-01888ecfbde40c16bf.jpg")

    TOKEN_PRICING = {
        20: 50,
        35: 100, 
        45: 150,
        60: 300
    }
