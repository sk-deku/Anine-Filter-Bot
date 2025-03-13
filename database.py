import pymongo
from config import Config

client = pymongo.MongoClient(Config.DATABASE_URL)
db = client["AutoFilterBot"]
users = db["users"]
files = db["files"]

def get_files(query):
    return [doc["file_name"] for doc in files.find({"file_name": {"$regex": query, "$options": "i"}})]

def get_tokens(user_id):
    user = users.find_one({"user_id": user_id})
    return user["tokens"] if user else 0

def deduct_token(user_id):
    users.update_one({"user_id": user_id}, {"$inc": {"tokens": -1}}, upsert=True)

def add_tokens(user_id, amount):
    users.update_one({"user_id": user_id}, {"$inc": {"tokens": amount}}, upsert=True)

def is_verified_user(user_id):
    """Check if a user is verified."""
    user = users.find_one({"user_id": user_id})
    return user and user.get("verified", False)

def set_verified(user_id):
    """Mark a user as verified."""
    users.update_one({"user_id": user_id}, {"$set": {"verified": True}}, upsert=True)
