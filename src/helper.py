from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter # With this we can split the text into smaller chunks
from langchain.embeddings import HuggingFaceEmbeddings # with this we can convert text to vector
from langchain_pinecone import PineconeVectorStore

# Extract data from pdf
def load_pdf(data):
    loader= DirectoryLoader(data,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    
    documents = loader.load()
    return documents


# Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunk = text_splitter.split_documents(extracted_data)
    return text_chunk


# download the embedding model
def download_embedding_model():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

# Defining retriever
from langchain.schema.retriever import BaseRetriever
from typing import List
from langchain.schema import Document
from pydantic import BaseModel

class PineconeRetriever(BaseRetriever, BaseModel):
    pinecone_vector_store: PineconeVectorStore

    def __init__(self, pinecone_vector_store: PineconeVectorStore, **data):
        super().__init__(pinecone_vector_store=pinecone_vector_store, **data)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.pinecone_vector_store.similarity_search(query)

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self.pinecone_vector_store.similarity_search(query)