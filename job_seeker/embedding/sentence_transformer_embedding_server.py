from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List
import torch


bi_encoder = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True, model_kwargs={"torch_dtype": "float16"})
cross_encoder = CrossEncoder("mixedbread-ai/mxbai-rerank-large-v1", automodel_args={"torch_dtype":'float16'})
class EmbeddingQuery(BaseModel):
    query: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]

class CrossEmbeddingQuery(BaseModel):
    query: str
    context: str

class CrossEmbeddingResponse(BaseModel):
    similarity: float

app = FastAPI()


@app.post("/embedding/")
async def embedding(body: EmbeddingQuery):
    torch.cuda.empty_cache()
    return EmbeddingResponse(embedding=bi_encoder.encode(body.query, batch_size=1))

@app.post("/cross_embedding/")
async def cross_embedding(body: CrossEmbeddingQuery):
    torch.cuda.empty_cache()
    return CrossEmbeddingResponse(similarity=cross_encoder.predict((body.query, body.context), batch_size=1))
