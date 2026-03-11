from pymongo import MongoClient

client = MongoClient("mongodb+srv://samratd2005_db_user:samrat_dbatlas@recipe-ai.5gqvssd.mongodb.net/")

db = client["recipe-ai"]

users_collection = db["users"]