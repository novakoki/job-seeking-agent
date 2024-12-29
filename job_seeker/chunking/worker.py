from multiprocessing import Process
import asyncio

from job_seeker.chunking.base import UnstructuredChunker


class MultiprocessingChunkingWorker:
    def __init__(self, n_workers):
        self.n_workers = n_workers
        self.pool = []

    def serve(self):
        self.pool = [
            Process(target=MultiprocessingChunkingWorker.work_process)
            for _ in range(self.n_workers)
        ]
        for p in self.pool:
            p.start()
        for p in self.pool:
            p.join()

    @staticmethod
    def work_process():
        chunker = UnstructuredChunker()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(chunker.serve())
        loop.close()


if __name__ == "__main__":
    worker = MultiprocessingChunkingWorker(4)
    worker.serve()
