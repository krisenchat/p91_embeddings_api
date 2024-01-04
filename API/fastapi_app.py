import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import List
import numpy as np
from InstructorEmbedding import INSTRUCTOR

# Initialize the FastAPI app
app = FastAPI(redirect_slashes=True)

# Initialize the model
model = INSTRUCTOR('hkunlp/instructor-large')

# Endpoint for the root path
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "API for generating embeddings from text using a HuggingFace model."}

# Health Check Endpoint
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}

# Request Model
class EmbeddingRequest(BaseModel):
    texts: List[str]

# Response Model
class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

# Doc Embedding Endpoint
@app.post("/get_doc_embeddings", response_model=EmbeddingResponse, tags=["Embedding"])
async def get_doc_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    """Compute document embeddings using a HuggingFace transformer model.

    Args:
        request: A list of texts to embed.

    Returns:
        A list of embeddings, one for each text.
    """
    try:
        instruction_pairs = [["Represent the document for retrieval: ", text] for text in request.texts]
        embeddings = model.encode(instruction_pairs)
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        return EmbeddingResponse(embeddings=embeddings_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Query Embedding Endpoint
@app.post("/get_query_embeddings", response_model=EmbeddingResponse, tags=["Embedding"])
async def get_query_embeddings(request: EmbeddingRequest) -> EmbeddingResponse:
    """Compute document embeddings using a HuggingFace transformer model.

    Args:
        request: A list of texts to embed.

    Returns:
        A list of embeddings, one for each text.
    """
    try:
        instruction_pairs = [["Represent the question for retrieving supporting documents: ", text] for text in request.texts]
        embeddings = model.encode(instruction_pairs)
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        return EmbeddingResponse(embeddings=embeddings_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Main Function
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
