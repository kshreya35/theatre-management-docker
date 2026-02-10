from pymongo import MongoClient
import time

def get_database():
    for i in range(15):  # try for 30 seconds
        try:
            client = MongoClient("mongodb://db:27017/", serverSelectionTimeoutMS=2000)
            client.server_info()  # force connection
            print("✅ MongoDB Connected")
            return client["theatre_booking"]
        except Exception:
            print("⏳ Waiting for MongoDB to start...")
            time.sleep(2)

    raise Exception("❌ MongoDB connection failed")

db = get_database()
bookings_collection = db["bookings"]
