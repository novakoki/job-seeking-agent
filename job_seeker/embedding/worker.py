import asyncio
import json

from loguru import logger

from job_seeker.embedding.sentence_transformer_embedding import (
    SentenceTransformerEncoder,
)


class SentenceTransformerGPUWorker:
    def __init__(self):
        self.encoder = SentenceTransformerEncoder(
            "dunzhang/stella_en_400M_v5",
            model_kwargs={
                "revision": "eb1ce34a33908596b61c83a88903b5f5f30beaa9",
                "trust_remote_code": True,
                "model_kwargs": {"torch_dtype": "float16"},
            },
        )

    async def serve(self, loop=None):
        await self.encoder.serve(loop)

    def execute(self, query):
        return self.encoder.encode(query)


if __name__ == "__main__":
    worker = SentenceTransformerGPUWorker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.serve())
    loop.close()
