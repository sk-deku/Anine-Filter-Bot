import os

class Config:
    # Required configuration
    API_ID = int(os.environ["API_ID"])
    API_HASH = os.environ["API_HASH"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    DATABASE_URL = os.environ["DATABASE_URL"]
    
    # Channel configuration
    INDEX_CHANNEL = int(os.environ["INDEX_CHANNEL"])  # Channel where files are added
    MAIN_CHANNEL = int(os.environ["MAIN_CHANNEL"])    # Your public channel
    
    # Optional configuration
    ADMINS = list(map(int, os.getenv("ADMINS", "1775977570").split()))
    CACHE_TIME = int(os.getenv("CACHE_TIME", 300))
    RESULTS_PER_PAGE = int(os.getenv("RESULTS_PER_PAGE", 10))
