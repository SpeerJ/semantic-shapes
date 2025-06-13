# Semantic Shapes Frontend

A React-based web application for exploring and learning about word2vec embeddings and vector arithmetic. This interactive tool helps users understand how words are represented as high-dimensional vectors and how semantic relationships can be discovered through mathematical operations.

## Features
- **Vector Arithmetic**: Perform mathematical operations on word vectors (e.g., "king - man + woman = queen")
- **More to come**

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm package manager
- Backend API server running (see backend documentation)

### Installation

1. Clone the repository:
```
git clone www.github.com/speerj/semantic-shapes cd frontend
``` 

2. Install dependencies:
```
npm install
``` 

3. Start the development server:
```
npm run dev
``` 

4. Open your browser and navigate to `http://localhost:5173`

## Usage

### Vector Arithmetic

The most fascinating property of word embeddings is that they capture semantic relationships through linear operations:

- **Analogies**: `A is to B as C is to D` can be computed as `B - A + C ≈ D`
- **Gender Relations**: `king - man + woman ≈ queen`
- **Geographic Relations**: `tokyo - japan + france ≈ paris`
- **Linguistic Relations**: `walking - walk + swim ≈ swimming`
- **Philosophical Relations**: `animal + culpable ≈ human`

Use the format: `word1 - word2 + word3` or combinations of addition and subtraction.
## API Integration

The frontend connects to the Semantic Shapes API with the following endpoints:

- `/api/info` - Model metadata (dimensions, vocabulary size)
- `/api/similar` - Find similar words
- `/api/arithmetic` - Vector arithmetic operations
- `/api/projected` - Get 2D/3D coordinates for visualization
- `/api/vocab` - Browse vocabulary
- `/api/vector` - Raw embedding vectors

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Tech Stack

- **React 19.1.0** - UI framework
- **Vite 6.3.5** - Build tool and dev server
- **ESLint** - Code linting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Word2Vec algorithm by Mikolov et al.
- Built with modern React and Vite
