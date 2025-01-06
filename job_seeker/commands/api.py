import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from job_seeker.core.db.dao import JobDAO
from job_seeker.embedding.worker import SentenceTransformerGPUWorker
from job_seeker.commands.worker import main

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
    asyncio.ensure_future(main())

@app.get("/jobs")
async def get_jobs(skip: int = 0, limit: int = 1000):
    return await JobDAO.pagination(skip, limit)

@app.post("/embedding/")
async def embedding(body: EmbeddingQuery):
    return EmbeddingResponse(embedding=worker.execute(body.query))
