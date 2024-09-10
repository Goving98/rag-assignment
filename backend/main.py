from fastapi import FastAPI, File, UploadFile, Request , HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import shutil
import uvicorn
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elasticsearch import Elasticsearch
from index import ElasticsearchStore

from docparse import parse_document

from index import run_ingestion_pipeline , es_vector_store
from query import run_query

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file temporarily

    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Re-open the file to read it as bytes
    with open(temp_file_path, "rb") as f:
        content = f.read()
    
    await es_vector_store.clear()
    parsed_text = parse_document(content, filename=temp_file_path)
    
    # Run the ingestion pipeline with the parsed text
    run_ingestion_pipeline(parsed_text)
    os.remove(temp_file_path)
    
    return JSONResponse(content={"message": "File processed and indexed."})

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def query_model(request: Request):
    data = await request.json()
    query = data.get("query", "")
    response = await run_query(query)
    
    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
