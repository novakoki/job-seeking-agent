import multiprocessing
import asyncio

from loguru import logger


class MultiprocessingChunkingWorker:
    def __init__(self, n_workers=4):
        self.n_workers = n_workers
        self.pool = []

    async def serve(self):
        logger.info("Start dispatching")
        context = multiprocessing.get_context("spawn")
        self.pool = [
            context.Process(target=MultiprocessingChunkingWorker.work_process)
            for _ in range(self.n_workers)
        ]
        for p in self.pool:
            p.start()

        while True:
            await asyncio.sleep(1)
        
        for p in self.pool:
            p.terminate()

    @staticmethod
    def work_process():
        from job_seeker.chunking.base import UnstructuredChunker
        chunker = UnstructuredChunker()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(chunker.serve())
        loop.close()


if __name__ == "__main__":
    worker = MultiprocessingChunkingWorker(4)
    worker.serve()
