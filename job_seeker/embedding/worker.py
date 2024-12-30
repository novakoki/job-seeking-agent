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
                "trust_remote_code": True,
                "model_kwargs": {"torch_dtype": "float16"},
            },
        )

    async def serve(self):
        await self.encoder.serve()

    def execute(self, query):
        return self.encoder.encode(query)


if __name__ == "__main__":
    worker = SentenceTransformerGPUWorker()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(worker.serve())
    loop.close()
