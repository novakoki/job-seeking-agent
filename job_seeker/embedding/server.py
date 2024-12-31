import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from job_seeker.embedding.worker import SentenceTransformerGPUWorker

worker = SentenceTransformerGPUWorker()

class EmbeddingQuery(BaseModel):
    query: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]

app = FastAPI()

@app.on_event("startup")
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(worker.serve(loop))

@app.post("/embedding/")
async def embedding(body: EmbeddingQuery):
    return EmbeddingResponse(embedding=worker.execute(body.query))

