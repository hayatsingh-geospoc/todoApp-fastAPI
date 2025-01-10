from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

# Use certifi for SSL certificate verification
client = MongoClient(os.getenv("MONGODB_URL"), tlsCAFile=certifi.where())
db = client[os.getenv("DATABASE_NAME")]
todo_collection = db["todos"] 