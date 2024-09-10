# index.py
import os
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch
import asyncio

load_dotenv('.env')

class CustomElasticsearchStore(ElasticsearchStore):
    def __init__(self, index_name, vector_field, text_field, es_cloud_id, es_api_key):
        super().__init__(index_name=index_name,
                         vector_field=vector_field,
                         text_field=text_field,
                         es_cloud_id=es_cloud_id,
                         es_api_key=es_api_key)

    async def clear(self):
        await self.es_client.delete_by_query(index=self.index_name, body={"query": {"match_all": {}}})

# Create an instance of the custom store
es_vector_store = CustomElasticsearchStore(
    index_name="calls",
    vector_field='conversation_vector',
    text_field='conversation',
    es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    es_api_key=os.getenv("ELASTIC_API_KEY")
)

def run_ingestion_pipeline(parsed_text: str):
    import asyncio
    asyncio.run(es_vector_store.clear())
    
    documents = [Document(text=parsed_text, metadata={"source": "uploaded_file"})]
    
    # Ingestion Pipeline setup
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=350, chunk_overlap=50),
            OllamaEmbedding("mistral"),
        ],
        vector_store=es_vector_store
    )
    
    pipeline.run(documents=documents)
    print(".....Done running pipeline.....\n")

def run_pipeline(parsed_text: str):
    asyncio.run(run_ingestion_pipeline(parsed_text))