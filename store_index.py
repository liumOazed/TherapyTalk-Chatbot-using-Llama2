from src.helper import load_pdf, text_split , download_embedding_model
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# load the data from pdf
extracted_data = load_pdf("data/")

# Create chunks
text_chunks = text_split(extracted_data)
#download the embedding
embeddings = download_embedding_model()

# Initialize pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("mindbot")
# Creating embeddings for each of the text chunks and store them in pinecone. (This is our knowledge base) 
docsearch = PineconeVectorStore.from_texts([t.page_content for t in text_chunks], index_name='mindbot', embedding=embeddings)