# Request Model
from typing import List

from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    texts: object

# Response Model
class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]