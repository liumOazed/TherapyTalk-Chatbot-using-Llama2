# TherapyTalk-Chatbot-using-Llama2

## Steps to run the project

```bash
conda create -n mindbot python=3.8 -y
```
### If you face any problem running conda on git bash from vscode try the below easy solution:
1. Locate your Anaconda installed folder in your windows machine and head straight to the script folder.
2. Now copy the absolute path and put it in you environment variable (Adding only the "C:\...\anaconda3\Scripts" directory to the system PATH is generally safer than adding the entire Anaconda installation directory.)
3. Now run ```conda create -n yourenvname ```
4. Now activate the env by using ```conda activate yourenvname```
5. If you face any conda init error simply run ```conda init bash ``` and close the git bash from your vscode and rerun step 4
6. Run ```pip install -r requirements.txt ```

### Project Requirements Explanation:
1. Ctransformers is needed because I will run this model in cpu so we need ctransformers to load the quantized model. and also I will be using langchain so that's why this package is needed.
2. Sentence-Transformer is for embedding purpose. It's opensource and free.
3. Pinecone for the vector database.  
4. Langchain - A framework that empowers developers to create data-aware and agentic applications using language models.
5. Python Flask for front-end development

## Download the llama2 quantized model from huggingface
llama-2-7b-chat.ggmlv3.q4_0.bin from here: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main 

## Get your Pinecone API Key for accessing vector database
from here: https://app.pinecone.io/

## Testing the Limits of the entire RAG pipeline
- We've tested around ~102 pages of PDF file(4.2MB) to perform summarization, NER and LDA(Topic Modeler) to workout the `main_query` and `context_queries` in json format which took around 13mins 37seconds on a T4 GPU of 15GiB.
- Then the json is being feeded into the Llama2 model for question-answering to check the performance.
- The performance is much more better with the RAG modeling than just feeding the complete RAW pdf file into the Llama2.
