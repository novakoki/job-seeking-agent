from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, List
import time
import json

import numpy as np
from loguru import logger

from job_seeker.db.dao import JobDAO
from job_seeker.db.rabbitmq import consume, publish
from job_seeker.db.dao import ChunkEmbeddingDAO


class BaseEncoder(ABC):
    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        ...

    async def serve(self):
        queue_name = "embedding"
        await consume(queue_name, self.execute)

    async def execute(self, msg: str):
        msg = json.loads(msg)
        job_id = msg["job_id"]
        chunk = msg["chunk"]
        job = await JobDAO.find_one(job_id)
        if job is None:
            logger.error(f"job_id does not exist: {job_id}")
            return
        start = time.time()
        embedding = self.encode(chunk)
        logger.info(
            f"Embedding job_id {job_id} with chunk length {len(chunk)} to vector {embedding.shape} in {time.time() - start:.2f} seconds"
        )
        # TODO: save to vector db
        await ChunkEmbeddingDAO.add_one(job_id, embedding)