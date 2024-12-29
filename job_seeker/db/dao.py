from typing import Optional, Coroutine

from bson import ObjectId
from loguru import logger

from job_seeker.db.model import Job, Resume
from job_seeker.db.mongo import job_collection, resume_collection


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
            job["id"] = str(job["_id"])
            del job["_id"]
            return Job(**job)

        return None

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
