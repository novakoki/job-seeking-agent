from job_seeker.embedding.sentence_transformer_embedding import request_embedding
from job_seeker.db.dao import ChunkEmbeddingDAO, JobDAO

async def test_request_embedding():
    text = "Languages: Python, C++, TypeScript/JavaScript, Java"
    embedding = request_embedding(text)

    print(len(embedding))

    response = await ChunkEmbeddingDAO.search(embedding)
    
    for point in response.points:
        job = await JobDAO.find_one(point.payload["job_id"])
        print(job.link)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_request_embedding())
    loop.close()
