import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

from job_seeker.core.db.dao import JobDAO

app = FastAPI()

@app.get("/jobs")
async def get_jobs(skip: int = 0, limit: int = 1000):
    return await JobDAO.pagination(skip, limit)
