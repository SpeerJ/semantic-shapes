import os
import numpy as np
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import logging
from typing import List, Dict, Any, Optional

class WordEmbeddings:
    """WordEmbeddings class A wrapper for a word2vec model
     Find similar words, see how words relate to one another
     Requires a pre-trained word embeddings model, not in binary format
     Model that I used: wiki-news-300d-1M-subword.vec
     Model can be downloaded from https://fasttext.cc/docs/en/english-vectors.html
    """
    def __init__(self, model_path: str = None):
        self.model_path = model_path or os.environ.get('MODEL_PATH', "model/model.bin")
        self.model = None
        self.model_type = None
        self.dimensions = 300
        self.vocab_size = 0
        self.vocabulary = set()

    def load_model(self):
        """Load pre-trained word embeddings"""
        try:
            if not os.path.exists(self.model_path):
                logging.warning(f"Model file not found at \"{self.model_path}\". Will use dummy model for testing.")
                self._create_dummy_model()
                return

            logging.info(f"Loading word embeddings from {self.model_path}")
            self.model = KeyedVectors.load_word2vec_format(self.model_path, binary=False)
            self.dimensions = self.model.vector_size
            self.vocab_size = len(self.model.key_to_index)
            self.vocabulary = set(self.model.key_to_index.keys())
            logging.info(f"Loaded model with {self.vocab_size} words and {self.dimensions} dimensions")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            self._create_dummy_model()

    def _create_dummy_model(self):
        """Create a small dummy model for testing when no model is available"""
        from gensim.models import Word2Vec

        # Sample vocabulary for testing
        words = ["king", "queen", "man", "woman", "prince", "princess", 
                 "boy", "girl", "father", "mother", "son", "daughter",
                 "dog", "cat", "paris", "france", "berlin", "germany", 
                 "tokyo", "japan", "computer", "keyboard", "mouse"]
                 
        # Create dummy sentences for training
        sentences = []
        for i in range(len(words)):
            for j in range(i+1, len(words)):
                sentences.append([words[i], words[j]])
        model = Word2Vec(sentences, vector_size=10, window=2, min_count=1, workers=1)
        self.model = model.wv
        self.model_type = "gensim"
        self.dimensions = self.model.vector_size
        self.vocab_size = len(self.model.key_to_index)
        self.vocabulary = set(self.model.key_to_index.keys())
        logging.warning(f"Created dummy model with {self.vocab_size} words and {self.dimensions} dimensions")

    def get_vector(self, word: str) -> np.ndarray:
        """Get the embedding vector for a word"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        return self.model[word]
    
    def get_similar_words(self, word: str, n: int = 10) -> List[Dict[str, Any]]:
        """Find n most similar words to the given word"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        similar = self.model.most_similar(word, topn=n)
        return [{"word": w, "similarity": float(s)} for w, s in similar]
    
    def calculate_expression(self, expression: str, n: int = 5) -> List[Dict[str, Any]]:
        """Calculate word vector arithmetic expressions like 'king - man + woman'.
        Handles words with trailing periods by removing them."""
        if not self.model:
            raise ValueError("Model not loaded")
        parts = expression.lower().replace(" ", "").replace("-", "+-").split("+")
        parts = [p for p in parts if p]  # Remove empty parts
        
        if not parts:
            raise ValueError("Invalid expression")
        result_vector = None
        for part in parts:
            if "-" in part:
                word = part.split("-")[1]
                if word not in self.model:
                    raise ValueError(f"Word '{word}' not in vocabulary")
                vector = -self.model[word]
            else:
                if part not in self.model:
                    raise ValueError(f"Word '{part}' not in vocabulary")
                vector = self.model[part]
            
            if result_vector is None:
                result_vector = vector.copy()
            else:
                result_vector += vector
        # Find similar words to the resulting vector
        similar_raw = self.model.similar_by_vector(result_vector, topn=n + len(parts))
        # Remove words from the result that are already in the expression and strip periods
        similar = [(w.rstrip('.'), s) for w, s in similar_raw
                   if w.lower().rstrip('.') not in [p.lower().rstrip('.') for p in parts]][:n]
        return [{"word": w, "similarity": float(s)} for w, s in similar]
    
    def project_words(
        self, 
        words: List[str], 
        method: str = "pca", 
        dimensions: int = 2
    ) -> Dict[str, List[float]]:
        """Project word vectors to 2D or 3D space using PCA or t-SNE"""
        if not self.model:
            raise ValueError("Model not loaded")
        if dimensions not in [2, 3]:
            raise ValueError("Dimensions must be 2 or 3")
        
        # Get vectors for all words
        vectors = np.array([self.model[word] for word in words])
        
        # Apply dimensionality reduction
        if method.lower() == "pca":
            reducer = PCA(n_components=dimensions)
        elif method.lower() == "tsne":
            reducer = TSNE(n_components=dimensions, random_state=42)
        else:
            raise ValueError("Method must be 'pca' or 'tsne'")
        reduced_vectors = reducer.fit_transform(vectors)
        
        # Format the result
        result = {}
        for i, word in enumerate(words):
            result[word] = reduced_vectors[i].tolist()
        
        return result

    def get_vocabulary(self, limit: int = 10000, starts_with: Optional[str] = None) -> List[str]:
        """Get a list of vocabulary words, optionally filtered by prefix"""
        if not self.model:
            raise ValueError("Model not loaded")
        
        vocab = list(self.model.key_to_index.keys())
        
        if starts_with:
            vocab = [w for w in vocab if w.startswith(starts_with.lower())]
        return vocab[:limit]