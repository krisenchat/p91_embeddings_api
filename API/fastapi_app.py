import os

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
#from components.logger import Logger
from InstructorEmbedding import INSTRUCTOR
from typing import List
import numpy as np




#logger = Logger()



# Initialize the FastAPI app
app = FastAPI(redirect_slashes=True)

model = INSTRUCTOR('hkunlp/instructor-xl')



@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Hey, I am an API that holds an embeddingsmodel. You can send me text and I will send you embeddings."
    }
@app.get("/health", include_in_schema=False)
def health_check():
    return {"status": "ok"}

def create_dict_from_texts(texts: list):
    return [{"text": text, "instruction": "Represent the text for retrieval"} for text in texts]

# Example usage

@app.post("/get_embeddings",
          summary="Gives you embeddings!",
          description="In this endpoint you can send some text to model and it will return a list of embeddings",
          tags=["Embedding"]
          )
async def get_embeddings(input_texts: List[str]):
    try:
        # prepare texts with instructions
        text_instruction_pairs = create_dict_from_texts(input_texts)

        # postprocess
        texts_with_instructions = []
        for pair in text_instruction_pairs:
            texts_with_instructions.append([pair["instruction"], pair["text"]])

        # calculate embeddings
        customized_embeddings = model.encode(texts_with_instructions)
        embeddings_list = customized_embeddings.tolist() if isinstance(customized_embeddings,
                                                                       np.ndarray) else customized_embeddings

        # Combine text-instruction pairs with their corresponding embeddings
        output = [
            {**pair, "embedding": embedding}
            for pair, embedding in zip(text_instruction_pairs, embeddings_list)
        ]

        return JSONResponse(content={"message": output}, status_code=200)
    except Exception as e:
        print(e) #logger.error(msg=f"Failed with {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)