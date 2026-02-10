from pymongo import MongoClient
import time

def get_database():
    for i in range(15):
        try:
            client = MongoClient("mongodb://db:27017/", serverSelectionTimeoutMS=2000)
            client.server_info()
            print("MongoDB connected (theatres)")
            return client["theatre_booking"]
        except:
            print("Waiting for MongoDB...")
            time.sleep(2)

    raise Exception("Database not ready")

db = get_database()
theatres_collection = db["theatres"]
