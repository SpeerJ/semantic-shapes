# Semantic Shapes Backend

A FastAPI backend for visualizing and exploring word embeddings. This application provides API endpoints for retrieving word vectors, finding similar words, performing vector arithmetic, and projecting words into 2D/3D space for visualization.

## Features

- Get raw embedding vectors for words
- Find similar words based on cosine similarity
- Perform vector arithmetic (e.g., `king - man + woman ≈ queen`)
- Project words into 2D or 3D space for visualization using PCA or t-SNE
- Retrieve vocabulary for autocomplete/dropdowns

## Setup

### Prerequisites

- Python 3.10+
- Conda (recommended) or virtualenv

### Installation

1. Clone the repository:
