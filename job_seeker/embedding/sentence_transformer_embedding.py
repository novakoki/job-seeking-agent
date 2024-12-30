from sentence_transformers import SentenceTransformer
import torch
import numpy as np

from job_seeker.embedding.base import BaseEncoder

import requests

def request_embedding(text: str):
    with requests.post("http://192.168.1.74:8000/embedding/", json={"query": text}) as response:
        body = response.json()
    return body["embedding"]

def request_cross_embedding(query: str, context: str):
    with requests.post("http://192.168.1.74:8000/cross_embedding/", json={"query": query, "context": context}) as response:
        body = response.json()
    return body["similarity"]


class SentenceTransformerEncoder(BaseEncoder):
    def __init__(self, model_name: str, model_kwargs: dict = None):
        self.model = SentenceTransformer(model_name, **model_kwargs)

    def encode(self, query: str) -> np.ndarray:
        torch.cuda.empty_cache()
        return self.model.encode(query, batch_size=1)
