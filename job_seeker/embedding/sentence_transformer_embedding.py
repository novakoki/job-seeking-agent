from sentence_transformers import SentenceTransformer
import torch
import numpy as np

from job_seeker.embedding.base import BaseEncoder


class SentenceTransformerEncoder(BaseEncoder):
    def __init__(self, model_name: str, model_kwargs: dict = None):
        self.model = SentenceTransformer(model_name, **model_kwargs)

    def encode(self, query: str) -> np.ndarray:
        torch.cuda.empty_cache()
        return self.model.encode(query, batch_size=1)
