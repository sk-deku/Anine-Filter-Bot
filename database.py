import pymongo
from config import Config
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)

try:
    client = pymongo.MongoClient(Config.DATABASE_URL, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["AutoFilterBot"]
    users = db["users"]
    files = db["files"]
    files.create_index([("file_name", "text")])
except ConnectionFailure as e:
    logger.error(f"Database connection failed: {e}")
    raise

def get_files(query):
    try:
        return [{"file_name": doc["file_name"], "file_id": doc["file_id"]} for doc in files.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})])]
    except Exception as e:
        logger.error(f"Search error: {e}")
        return []

# Rest of the code remains the same...

def get_tokens(user_id):
    try:
        user = users.find_one({"user_id": user_id})
        return user.get("tokens", 0) if user else 0
    except Exception as e:
        logger.error(f"Token check error: {e}")
        return 0

def deduct_token(user_id):
    try:
        users.update_one(
            {"user_id": user_id, "tokens": {"$gt": 0}},
            {"$inc": {"tokens": -1}}
        )
    except Exception as e:
        logger.error(f"Token deduction error: {e}")

def add_tokens(user_id, amount):
    try:
        if amount <= 0:
            raise ValueError("Token amount must be positive")
        users.update_one(
            {"user_id": user_id},
            {"$inc": {"tokens": amount}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Add tokens error: {e}")

def get_user_tokens(user_id):
    return get_tokens(user_id)  # Alias for consistency
