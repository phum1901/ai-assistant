import os
from pathlib import Path

from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name='cl100k_base',
    chunk_size=120,
    chunk_overlap=10,
)

embedding = FastEmbedEmbeddings(model_name=os.getenv("EMBEDDING_MODEL"))

file_paths = list(Path(os.getenv('DATA_DIR')).glob('*'))

def indexing_pipeline():
    documents = []
    for file_path in file_paths:
        loader = TextLoader(file_path=file_path)
        documents.extend(loader.load())

    documents = text_splitter.split_documents(documents)

    QdrantVectorStore.from_documents(
        documents,
        embedding,
        url=os.getenv('QDRANT_URL'),
        collection_name=os.getenv("COLLECTION_NAME"),
    )

if __name__ == "__main__":
    indexing_pipeline()
