from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
import os

qdrant_client = QdrantClient(url="http://localhost:6333")

def process_pdf(file):
    """Extract text chunks from PDF."""
    loader = PyPDFLoader(file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

def store_embeddings(chunks):
    """Generate embeddings and store in Qdrant."""
    embeddings = OpenAIEmbeddings()
    qdrant_vector_store = Qdrant.from_documents(
        chunks, embedding=embeddings, client=qdrant_client, collection_name="documents"
    )
    return qdrant_vector_store

def initialize_vector_store():
    """Check or initialize vector store."""
    if not qdrant_client.get_collections():
        print("Initializing Qdrant vector store...")
        return None
    return Qdrant(client=qdrant_client, collection_name="documents")

vector_store = initialize_vector_store()
