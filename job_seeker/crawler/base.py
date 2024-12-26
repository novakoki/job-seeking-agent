from abc import ABC, abstractmethod
from typing import AsyncGenerator

from job_seeker.db.model import Job

class BaseCrawler(ABC):
    @abstractmethod
    async def extract_jobs(self, link: str, **kwargs) -> AsyncGenerator[Job, None]: ...


class CrawlerRegistry:
    _registry = {}

    @classmethod
    def register(cls, name: str, crawler: BaseCrawler):
        if name in cls._registry:
            raise ValueError(f"{name} already exists in the registry")
        cls._registry[name] = crawler

    @classmethod
    def get(cls, name: str) -> BaseCrawler:
        if name not in cls._registry:
            raise ValueError(f"{name} not found in the registry")
        return cls._registry.get(name)
