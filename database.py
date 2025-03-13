import pymongo
from config import Config
from pymongo.errors import ConnectionFailure

# Connect to MongoDB with error handling
try:
    client = pymongo.MongoClient(Config.DATABASE_URL, serverSelectionTimeoutMS=5000)
    client.server_info()  # Test connection
    db = client["AutoFilterBot"]
    users = db["users"]
    files = db["files"]
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

def get_files(query):
    try:
        return [doc["file_name"] for doc in files.find({"file_name": {"$regex": query, "$options": "i"}})]
    except Exception as e:
        print(f"Error fetching files: {e}")
        return []

def get_tokens(user_id):
    try:
        user = users.find_one({"user_id": user_id})
        return user.get("tokens", 0) if user else 0
    except Exception as e:
        print(f"Error fetching tokens: {e}")
        return 0

def deduct_token(user_id):
    try:
        users.update_one({"user_id": user_id, "tokens": {"$gt": 0}}, {"$inc": {"tokens": -1}})
    except Exception as e:
        print(f"Error deducting tokens: {e}")

def add_tokens(user_id, amount):
    try:
        if amount <= 0:
            raise ValueError("Token amount must be positive.")
        users.update_one({"user_id": user_id}, {"$inc": {"tokens": amount}}, upsert=True)
    except Exception as e:
        print(f"Error adding tokens: {e}")
