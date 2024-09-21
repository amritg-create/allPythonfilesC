import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict
import heapq
from docx import Document

file_path = 'C://Users//amrigupt//OneDrive - Cisco//Amrit favorite basketball teams.docx'

# Function to read and preprocess the document
def read_document(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Specify the file path
file_path = 'C://Users//amrigupt//OneDrive - Cisco//Amrit favorite basketball teams.docx'

# Read the document
document_text = read_document(file_path)
documents = document_text.split('\n')

# Initialize and fit the vectorizer
vectorizer = TfidfVectorizer()
document_vectors = vectorizer.fit_transform(documents)

def search_documents(query, k=1):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, document_vectors)
    top_k_indices = similarities[0].argsort()[-k:][::-1]
    return [(documents[i], similarities[0][i]) for i in top_k_indices]

def summarize_text(text, num_sentences=3):
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    word_frequencies = defaultdict(int)
    for word in word_tokenize(text):
        if word.isalnum():
            word_frequencies[word.lower()] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]

    summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

def query_chatbot(user_query):
    search_results = search_documents(user_query)
    if not search_results:
        return "No relevant information found."
    
    retrieved_text = search_results[0][0]
    summary = summarize_text(retrieved_text)
    return summary

# Streamlit interface
st.title("RAG Chatbot")

user_query = st.text_input("Enter your query:")
if st.button("Submit"):
    if user_query:
        response = query_chatbot(user_query)
        st.write(f"Chatbot: {response}")
    else:
        st.write("Please enter a query.")
