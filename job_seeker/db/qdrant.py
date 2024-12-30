import os

from dotenv import load_dotenv
from qdrant_client import AsyncQdrantClient

load_dotenv()

client = AsyncQdrantClient(url=os.environ.get("QDRANT_URL"))

