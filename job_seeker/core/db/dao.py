from typing import Optional, List

from bson import ObjectId
from loguru import logger
import numpy as np

from job_seeker.core.db.model import Job, Resume
from job_seeker.core.db.mongo import job_collection, resume_collection


class JobDAO:
    @classmethod
    async def add_one_dict(cls, job: dict) -> Optional[str]:
        Job.model_validate(job)
        try:
            insert_result = await job_collection.insert_one(job)
            return str(insert_result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to add job: {e}")
            return None

    @classmethod
    async def add_one(cls, job: Job) -> Optional[str]:
        try:
            insert_result = await job_collection.insert_one(
                job.model_dump(exclude={"id"})
            )
            return str(insert_result.inserted_id)
        except:
            return None

    @classmethod
    async def update_desc(cls, job_id: str, description: str) -> bool:
        update_result = await job_collection.update_one(
            filter={"_id": ObjectId(job_id)},
            update={"$set": {"description": description}},
        )

        return update_result.modified_count > 0

    @classmethod
    async def find_one(cls, job_id: str):
        job = await job_collection.find_one({"_id": ObjectId(job_id)})

        if job is not None:
            return Job(**job, id=str(job["_id"]))

        return None
    
    @classmethod
    async def pagination(cls, skip=0, limit=10):
        cursor = job_collection.find({}).sort({"date": -1}).skip(skip).limit(limit)
        jobs = [Job(**job, id=str(job["_id"])) async for job in cursor]
        return jobs

    @classmethod
    async def remove_one(cls, job_id: str):
        delete_result = await job_collection.delete_one({"_id": ObjectId(job_id)})

        return delete_result.deleted_count

    @classmethod
    async def watch(cls):
        async with job_collection.watch() as change_stream:
            async for change in change_stream:
                yield change


class ResumeDAO:
    @classmethod
    async def add_one(cls, resume: dict) -> Optional[str]:
        # would raise ValidationError if the resume is invalid
        Resume.model_validate(resume)
        insert_result = await resume_collection.insert_one(resume)

        return insert_result.inserted_id

    @classmethod
    async def update_one(cls, resume_id: str, description: str):
        update_result = await resume_collection.update_one(
            filter={"_id": ObjectId(resume_id)},
            update={"$set": {"description": description}},
        )

        return update_result.upserted_id

class ChunkEmbeddingDAO:
    @classmethod
    async def add_one(cls, job_id: str, embedding: np.ndarray):
        from job_seeker.core.db.qdrant import client
        from qdrant_client import models
        from uuid import uuid4

        exists = await client.collection_exists(collection_name="chunk_embedding")

        if not exists:
            await client.create_collection(
                collection_name="chunk_embedding",
                vectors_config=models.VectorParams(
                    size=embedding.shape[0],
                    distance=models.Distance.COSINE,
                    datatype=models.Datatype.FLOAT32,
                ),
            )

        result = await client.upsert(
            collection_name="chunk_embedding",
            wait=True,
            points=[
                models.PointStruct(
                    id=str(uuid4()),
                    payload={
                        "job_id": job_id,
                    },
                    vector=embedding,
                ),
            ],
        )

    @classmethod
    async def search(cls, query: List[float], top_k: int = 10):
        from job_seeker.core.db.qdrant import client
        from qdrant_client import models

        search_result = await client.query_points(
            collection_name="chunk_embedding",
            query=query,
            limit=top_k,
        )

        return search_result
