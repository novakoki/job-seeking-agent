import motor.motor_asyncio

mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://192.168.1.74:27017")
mongo_db = mongo_client["job_seeker"]
job_collection = mongo_db["jobs"]
