import json
import glob
import os
from preprocessing_pipeline import (
    DocumentProcessor, 
    TopicModeler, 
    RAGInputGenerator
)

def run_rag(pdf_directory="data"):
    try:
        # Find all PDF files in the directory
        pdf_files = glob.glob(os.path.join(pdf_directory, '*.pdf'))
        if not pdf_files:
            raise ValueError("No PDF file found in the directory.")
        if len(pdf_files) > 1:
            raise ValueError("More than one PDF file found in the directory. Please ensure only one PDF is present.")

        # Assuming there's only one PDF file, use it
        pdf_path = pdf_files[0]
        print("Processing PDF:", pdf_path)  # Optional: Output the path of the PDF being processed

    except Exception as e:
        print("An error occurred:", e)

    document_processor = DocumentProcessor(pdf_path)
    summary = document_processor.summarize_text()
    entities = document_processor.perform_ner()

    lda_modeler = TopicModeler([document_processor.text])
    lda_model, feature_names = lda_modeler.perform_lda()
    topics = lda_modeler.get_topics(lda_model, feature_names)

    context_queries = [entity[0] for entity in entities] + topics
    rag_input = RAGInputGenerator.generate_rag_input(summary, context_queries)

    print(rag_input)

    #Save to a JSON file
    with open('rag_input.json', 'w') as json_file:
        json.dump(rag_input, 
                  json_file, 
                  indent=4
            )

# Usage
run_rag()