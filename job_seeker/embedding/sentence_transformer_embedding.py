from sentence_transformers import SentenceTransformer
import torch
import numpy as np


class SentenceTransformerEmbedding:
    def __init__(self, model_name: str, model_kwargs: dict = None):
        if model_kwargs is None:
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": "float16"
            }
        self.model = SentenceTransformer(model_name, model_kwargs=model_kwargs)

    def encode(self, query: str) -> np.ndarray:
        torch.cuda.empty_cache()
        return self.model.encode(query, batch_size=1)
