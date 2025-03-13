import pymongo
import logging
from pymongo.errors import ConnectionFailure, OperationFailure
from config import Config

logger = logging.getLogger(__name__)

try:
    client = pymongo.MongoClient(Config.DATABASE_URL, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client["AutoFilterBot"]
    users = db["users"]
    files = db["files"]
    
    # Smart index creation
    existing_indexes = files.index_information()
    text_index_exists = any(
        idx["key"][0][0] == "file_name" and idx["key"][0][1] == "text"
        for idx in existing_indexes.values()
    )
    
    if not text_index_exists:
        files.create_index([("file_name", "text")], name="search_index")
        logger.info("Created text search index")
    else:
        logger.info("Using existing text index")

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

def get_files(query):
    try:
        return [doc for doc in files.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})])]
    except Exception as e:
        logger.error(f"Search error: {e}")
        return []

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
        logger.error(f"Deduction error: {e}")

def add_tokens(user_id, amount):
    try:
        users.update_one(
            {"user_id": user_id},
            {"$inc": {"tokens": amount}},
            upsert=True
        )
    except Exception as e:
        logger.error(f"Add tokens error: {e}")
