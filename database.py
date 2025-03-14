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
    
    # Index management
    target_index = [("file_name", "text")]
    index_name = "search_index"
    existing_indexes = files.index_information()

    # Remove conflicting indexes
    for name, index in existing_indexes.items():
        if index['key'] == target_index and name != index_name:
            logger.info(f"Removing old index: {name}")
            files.drop_index(name)

    # Create new index if needed
    if index_name not in existing_indexes:
        try:
            files.create_index(target_index, name=index_name)
            logger.info("Created text search index")
        except OperationFailure as e:
            logger.error(f"Index error: {e}")

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

# Other functions (get_files, get_tokens, etc.) remain same as previous versions

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
