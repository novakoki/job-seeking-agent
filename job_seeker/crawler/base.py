from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any
import asyncio
import time

from loguru import logger

from job_seeker.db.model import Job
from job_seeker.db.dao import JobDAO
from job_seeker.db.rabbitmq import consume
from pydantic import ValidationError


class BaseCrawler(ABC):
    @abstractmethod
    async def extract_jobs(self, link: str) -> AsyncGenerator[Job, None]:
        ...

    async def serve(self):
        queue_name = self.__class__.__name__
        await consume(queue_name, self.execute)

    async def execute(self, link: str):
        start = time.time()
        cnt = 0
        futures = []
        async for job in self.extract_jobs(link):
            futures.append(asyncio.create_task(JobDAO.add_one(job)))
        for future in futures:
            try:
                result = await future
                if result is not None:
                    cnt += 1
            except ValidationError as e:
                logger.error(f"Failed to add job: {e}")

        logger.info(
            f"Added {cnt} jobs in {time.time() - start:.2f} seconds from {link}"
        )


class CrawlerRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, crawler: type[BaseCrawler]):
        if name in cls._registry:
            raise ValueError(f"{name} already exists in the registry")
        cls._registry[name] = crawler

    @classmethod
    def get(cls, name: str) -> type[BaseCrawler]:
        if name not in cls._registry:
            raise ValueError(f"{name} not found in the registry")
        return cls._registry.get(name)

    @classmethod
    def list(cls):
        return cls._registry.keys()
