import os

from dotenv import load_dotenv

import motor.motor_asyncio

load_dotenv()
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI"))
mongo_db = mongo_client[os.environ.get("MONGO_DB")]
job_collection = mongo_db["jobs"]
resume_collection = mongo_db["resumes"]
query_collection = mongo_db["queries"]
