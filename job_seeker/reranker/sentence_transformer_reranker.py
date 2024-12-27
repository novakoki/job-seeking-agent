import torch
from sentence_transformers import CrossEncoder

class SentenceTransformerReRanker:
    def __init__(self, model_name: str, automodel_args: dict = None):
        if automodel_args is None:
            automodel_args = {
                "torch_dtype": "float16"
            }
        self.model = CrossEncoder(model_name, automodel_args=automodel_args)

    def predict(self, query: str, context: str) -> float:
        torch.cuda.empty_cache()
        return self.model.predict((query, context), batch_size=1)
