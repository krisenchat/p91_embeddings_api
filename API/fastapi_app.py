import os
import uvicorn
from fastapi import FastAPI, HTTPException
import numpy as np

from API.base_models import EmbeddingResponse, EmbeddingRequest
from API.resource_manager import ResourceManager

# Initialize the FastAPI app
app = FastAPI(redirect_slashes=True)

resource_manager = ResourceManager()
resource_manager.load_model("hkunlp/instructor-xl")

embeddings_model = resource_manager.model

# Endpoint for the root path
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "API for generating embeddings from text using a HuggingFace model."}

# Health Check Endpoint
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok"}

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
        embeddings = embeddings_model.encode(instruction_pairs)
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
        embeddings = embeddings_model.encode(instruction_pairs)
        embeddings_list = embeddings.tolist() if isinstance(embeddings, np.ndarray) else embeddings
        return EmbeddingResponse(embeddings=embeddings_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/reload_embeddings_model", tags=["Reloading"])
async def reload_embeddings_model():
    """For extreme cases where the periodic reloading of the model is not enough, this endpoint provides a last solution
    for manual reloading (garbage collecting) of the embeddings model """
    try:
        resource_manager.reload_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return JSONResponse(content={"message": "Successfully reloaded model"}, status_code=200)

# Main Function
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
