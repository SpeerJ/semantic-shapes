from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from typing import List, Optional
import os

from utils import WordEmbeddings

app = FastAPI(
    title="Semantic Shapes API",
    description="API for visualizing and exploring word embeddings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize word embeddings
word_embeddings = WordEmbeddings()

@app.on_event("startup")
async def startup_event():
    # Load the word embeddings model on startup
    word_embeddings.load_model()

@app.get("/")
async def root():
    return {"message": "Welcome to the Semantic Shapes API"}

@app.get("/api/info")
async def get_info():
    """Return metadata about the model (type, dimensions, vocab size)"""
    return {
        "model_type": word_embeddings.model_type,
        "dimensions": word_embeddings.dimensions,
        "vocab_size": word_embeddings.vocab_size,
    }

@app.get("/api/vector")
async def get_vector(word: str):
    """Return the raw embedding vector for a given word"""
    try:
        vector = word_embeddings.get_vector(word)
        return {"word": word, "vector": vector.tolist()}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found in vocabulary")

@app.get("/api/similar")
async def get_similar(word: str, n: int = 10):
    """Return top-N most similar words (cosine similarity)"""
    try:
        similar_words = word_embeddings.get_similar_words(word, n)
        return {"word": word, "similar": similar_words}
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Word '{word}' not found in vocabulary")

@app.get("/api/arithmetic")
async def vector_arithmetic(expr: str, n: int = 5):
    """Compute vector arithmetic and return top-N nearest words"""
    try:
        result = word_embeddings.calculate_expression(expr, n)
        return {"expression": expr, "results": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/projected")
async def get_projected(
    words: str, 
    method: str = "pca", 
    dimensions: int = 2
):
    """Return 2D or 3D coordinates of words (via PCA or t-SNE)"""
    word_list = [w.strip() for w in words.split(",")]
    
    if not all(word in word_embeddings.vocabulary for word in word_list):
        unknown_words = [word for word in word_list if word not in word_embeddings.vocabulary]
        raise HTTPException(
            status_code=404, 
            detail=f"Words not found in vocabulary: {', '.join(unknown_words)}"
        )
    
    try:
        coordinates = word_embeddings.project_words(word_list, method, dimensions)
        return {
            "words": word_list,
            "method": method,
            "dimensions": dimensions,
            "coordinates": coordinates
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/vocab")
async def get_vocabulary(
    limit: int = 10000, 
    starts_with: Optional[str] = None
):
    """Return list of available vocabulary words"""
    vocab = word_embeddings.get_vocabulary(limit, starts_with)
    return {"count": len(vocab), "words": vocab}
