import os
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file

class Config:
    # Mandatory variables - Throw error if missing
    API_ID = int(os.environ["API_ID"])  # Use [] instead of getenv to enforce existence
    API_HASH = os.environ["API_HASH"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    DATABASE_URL = os.environ["DATABASE_URL"]

    # Optional variables with defaults
    SHORTENER_API = os.getenv("SHORTENER_API", "")
    SHORTENER_URL = os.getenv("SHORTENER_URL", "")
    ADMINS = list(map(int, os.getenv("ADMINS", "").split())) if os.getenv("ADMINS") else []
    PAYMENT_UPI = os.getenv("PAYMENT_UPI", "")
    PAYMENT_QR = os.getenv("PAYMENT_QR", "")

    TOKEN_PRICING = {
        20: 50,
        35: 100,
        45: 150,
        60: 300
    }
