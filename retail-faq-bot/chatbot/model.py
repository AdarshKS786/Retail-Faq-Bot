# chatbot/model.py

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A simple list of stopwords (you can expand this or use a library like NLTK)
STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])

class FAQBot:
    def __init__(self, filepath, similarity_threshold=0.3):
        self.df = pd.read_csv(filepath)
        self.similarity_threshold = similarity_threshold
        self.vectorizer = TfidfVectorizer(preprocessor=self._preprocess)
        
        # Vectorize the FAQ questions
        self.faq_vectors = self.vectorizer.fit_transform(self.df['question'])
        
    def _preprocess(self, text):
        """Cleans and preprocesses the text."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
        # Remove stopwords
        text = ' '.join([word for word in text.split() if word not in STOPWORDS])
        return text

    def get_answer(self, user_query):
        """Finds the most relevant FAQ answer for a user query."""
        query_vector = self.vectorizer.transform([user_query])
        
        # Calculate cosine similarity between the user query and all FAQ questions
        similarities = cosine_similarity(query_vector, self.faq_vectors).flatten()
        
        # Find the index of the most similar question
        best_match_index = similarities.argmax()
        max_similarity = similarities[best_match_index]
        
        print(f"DEBUG: Max similarity score: {max_similarity:.4f}")

        # Check if the similarity meets the threshold
        if max_similarity >= self.similarity_threshold:
            return self.df.iloc[best_match_index]['text_answer']
        else:
            return "I'm sorry, I'm not sure how to answer that. Please clarify if you're asking about a product or a service."