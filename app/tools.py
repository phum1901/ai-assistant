import os
from typing import List

from fastmcp import FastMCP

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

mcp = FastMCP('')

embedding = FastEmbedEmbeddings(model_name=os.getenv('EMBEDDING_MODEL'))

client = QdrantClient(
    url=os.getenv("QDRANT_URL")
)

vector_store = QdrantVectorStore(
    client,
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding=embedding
) 

@mcp.tool()
async def similarity_search(query: str) -> List: 
    """Perform a similarity search on a vector store using the given query string."""
    documents = await vector_store.asimilarity_search_with_score(query)
    return documents

if __name__ == "__main__":
    mcp.run()
