import pdfplumber
import torch
import spacy
import nltk
from collections import Counter
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from transformers import pipeline

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class DocumentProcessor:
    """Processes documents to extract text, summarize, and perform NER."""

    def __init__(self, pdf_path):
        """Initialize the processor with a PDF path."""
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if torch.cuda.is_available() else -1)
        self.text = self.extract_text_from_pdf(pdf_path)

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from each page of the PDF."""
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += " " + (page.extract_text() or "")
        return text.strip()

    def summarize_text(self, max_length=1024, min_length=100):
        """Summarizes the text extracted from the PDF."""
        sentences = nltk.sent_tokenize(self.text)
        summarized_text = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + " "
            else:
                part_summary = self.summarizer(
                    current_chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False)
                summarized_text.append(part_summary[0]['summary_text'])
                current_chunk = sentence + " "
        if current_chunk:
            part_summary = self.summarizer(
                current_chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False)
            summarized_text.append(part_summary[0]['summary_text'])
        return " ".join(summarized_text)

    def perform_ner(self):
        """Performs Named Entity Recognition (NER) on the extracted text."""
        doc = self.nlp(self.text)
        return [(ent.text, ent.label_) for ent in doc.ents]


class TopicModeler:
    """Performs topic modeling on the provided texts."""

    def __init__(self, texts, num_topics=10):
        """Initialize with texts and the number of topics."""
        self.texts = texts
        self.num_topics = num_topics

    def perform_lda(self, max_df=None, min_df=None):
        """Performs LDA to determine topics in the texts, adjusting min_df and max_df dynamically."""
        n_docs = len(self.texts)
        
        # Default values if not provided
        if min_df is None:
            min_df = 1
        if max_df is None:
            max_df = 1.0
        
        # Adjust min_df and max_df based on the number of documents
        if n_docs == 1:
            # If there's only one document, use lower min_df and adjust max_df to cover all terms
            min_df = 1
            max_df = 1.0  # Include all terms since there's only one document
        else:
            # Adjust min_df and max_df if specified as a proportion
            min_df = min_df if min_df >= 1 else int(min_df * n_docs)
            max_df = max_df if max_df >= 1 else int(max_df * n_docs)

        # Ensure max_df is never less than min_df
        if max_df < min_df:
            max_df = min_df

        vectorizer = CountVectorizer(
            stop_words='english',
            max_df=max_df,
            min_df=min_df,
            ngram_range=(
                1,
                2))
        doc_term_matrix = vectorizer.fit_transform(self.texts)
        lda = LatentDirichletAllocation(
            n_components=self.num_topics, random_state=0)
        lda.fit(doc_term_matrix)
        return lda, vectorizer.get_feature_names_out()

    def get_topics(self, lda_model, feature_names, n_top_words=10):
        topics = []
        for topic_idx, topic in enumerate(lda_model.components_):
            topics.append(" ".join([feature_names[i]
                          for i in topic.argsort()[:-n_top_words - 1:-1]]))
        return topics


class RAGInputGenerator:
    """Generates input for the RAG model based on summarization and topics."""

    @staticmethod
    def clean_context_queries(queries):
        unique_queries = []
        seen = set()
        for query in queries:
            normalized_query = query.lower()
            if normalized_query not in seen:
                seen.add(normalized_query)
                unique_queries.append(query)
        return unique_queries

    @staticmethod
    def generate_rag_input(summary, context_queries):
        """Generates RAG input structure from summary and context queries."""
        cleaned_queries = RAGInputGenerator.clean_context_queries(
            context_queries)
        return {
            "main_query": summary,
            "context_queries": cleaned_queries
        }