import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from job_seeker.embedding.worker import SentenceTransformerGPUWorker

worker = SentenceTransformerGPUWorker()
background_task = None

class EmbeddingQuery(BaseModel):
    query: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    background_task = asyncio.create_task(worker.serve())

@app.on_event("shutdown")
async def shutdown_event():
    background_task.cancel()

@app.post("/embedding/")
async def embedding(body: EmbeddingQuery):
    return EmbeddingResponse(embedding=worker.execute(body.query))
