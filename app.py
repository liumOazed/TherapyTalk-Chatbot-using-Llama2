from flask import Flask, render_template, jsonify, request
from src.helper import   download_embedding_model, PineconeRetriever
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers   
from langchain.chains import RetrievalQA # with this we can ask questions to the model
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

embeddings = download_embedding_model()

# Initialize pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("mindbot")
# with this we can load the vector
docsearch = PineconeVectorStore.from_existing_index( index_name='mindbot', embedding=embeddings) 

# Creating Prompt Template (reading it from prompt.py)
prompt = PromptTemplate(template=promp_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": prompt} # Created this chain type argument because I will be using Retrieval QA chain

# Loading llm model
llm = CTransformers(model="model\llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={"max_new_tokens": 512,
                            "temperature": 0.8})

# Create a PineconeRetriever object
pinecone_retriever = PineconeRetriever(docsearch)

# Creating Retrieval QA  Object
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=pinecone_retriever,
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

# Define the route to serve static files
app.static_folder = 'static'
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])

# Initializing the class
if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=8080, debug=True)