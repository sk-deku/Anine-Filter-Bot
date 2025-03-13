import pymongo
import logging
from config import Config
from pymongo.errors import ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)

try:
    client = pymongo.MongoClient(Config.DATABASE_URL, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["AutoFilterBot"]
    users = db["users"]
    files = db["files"]
    
    # Create index with error handling
    try:
        files.create_index([("file_name", "text")], name="search_index")
    except OperationFailure as e:
        logger.error(f"Index creation failed: {e}")

except ConnectionFailure as e:
    logger.critical(f"MongoDB connection failed: {e}")
    raise

def save_file(file_id, file_name):
    try:
        files.update_one(
            {"file_id": file_id},
            {"$set": {"file_id": file_id, "file_name": file_name}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"File save error: {e}")

# Other functions (get_files, get_tokens, etc) remain same as previous version

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
