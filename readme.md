# External Embeddings Model API

## Overview
This API is designed to generate embeddings from text using the HuggingFace model. It is deployed on a compute engine instance and is optimized for performance with GPU support. The API computes embeddings on demand for various text inputs.

## Features
- **Document Embeddings**: Generate embeddings for documents.
- **Query Embeddings**: Generate embeddings specifically tailored for queries in information retrieval contexts.

## Installation and Running the API
1. Clone the repository to your local machine.
2. Ensure you have the necessary dependencies installed, including FastAPI and HuggingFace transformers.
3. install packages if needed   
    ```bash 
    make install`
4. Run the server using Uvicorn:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080

## Encryption Module
The embeddings machine has an encryption module installed. By design, it is not possible to activate/deactivate encryption from the embeddings. In order to toggle this encryption module, please turn it on or off with ```ConfigManager.set_encryption_status(True)``` on the project you're calling the embeddings machine on.

