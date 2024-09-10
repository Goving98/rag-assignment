import time
from llama_index.core import VectorStoreIndex, QueryBundle, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from index import es_vector_store
import httpx
# Local LLM setup
local_llm = Ollama(model="mistral")
Settings.embed_model = OllamaEmbedding("mistral")

async def run_query(query: str) -> str:

    start_time = time.time()
    index = VectorStoreIndex.from_vector_store(es_vector_store)
    query_engine = index.as_query_engine(llm=local_llm, similarity_top_k=10)
    print(f"Engine setup time: {time.time() - start_time} seconds")
    query_embedding = Settings.embed_model.get_query_embedding(query)

    # Create a QueryBundle
    bundle = QueryBundle(query, embedding=query_embedding)
    print(f"Embedding generation time: {time.time() - start_time} seconds")

    # Query the index (this step might be the bottleneck)
    result = query_engine.query(bundle)

    # Log the total time taken
    url = "http://localhost:3000/query"
    data = {"query": query}

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=data)
        # Process the response if necessary
        # For example, if you need to add data to the result
        additional_data = response.json()
        print("Additional data is:",additional_data)
    print(f"Total query processing time: {time.time() - start_time} seconds")

    return str(result)
