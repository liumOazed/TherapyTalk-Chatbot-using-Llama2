# Defining Prompt Template
promp_template = """
Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know. Do not make up an answer.
context: {context}
question: {question}
Only return the helpful answer and information about the context. Do not make up an answer.
Helpful Answer:
"""