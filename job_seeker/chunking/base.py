from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any, List
import time
import json

from loguru import logger

from job_seeker.db.dao import JobDAO
from job_seeker.db.rabbitmq import consume, publish
from job_seeker.chunking.clean_html import clean_html


class BaseChunker(ABC):
    @abstractmethod
    async def extract(self, desc: str) -> AsyncGenerator[List[str], None]:
        ...

    async def serve(self):
        queue_name = "chunking"
        await consume(queue_name, self.execute)

    async def execute(self, msg: str):
        msg = json.loads(msg)
        job_id = msg["job_id"]
        desc = msg["desc"]
        job = await JobDAO.find_one(job_id)
        if job is None:
            logger.error(f"job_id does not exist: {job_id}")
            return
        cleaned_html, cleaned_text = clean_html(desc)
        await JobDAO.update_desc(job_id, cleaned_text)
        start = time.time()
        chunk_lens = []
        async for chunk in self.extract(cleaned_html):
            chunk_lens.append(len(chunk))
            await publish("embedding", json.dumps({"job_id": job_id, "chunk": chunk}))
        logger.info(
            f"Chunk job_id {job_id} with chunk length {chunk_lens} in {time.time() - start:.2f} seconds"
        )


class UnstructuredChunker(BaseChunker):
    async def extract(self, text: str) -> AsyncGenerator[List[str], None]:
        from unstructured.partition.html import partition_html
        from unstructured.chunking.title import chunk_by_title

        for chunk in chunk_by_title(
            partition_html(text=text),
            multipage_sections=False,
            max_characters=500
        ):
            yield str(chunk)
