# Research Paper Analyzer Backend

## Contributors

- [Jaineel Chhatraliya](https://github.com/CodeByJc) (jaineelchhatraliya@gmail.com)
- [Om Makadia](https://github.com/ommakadiya) (ommakadia1615@gmail.com)

This backend provides a FastAPI service that reads a research paper PDF and extracts the core scientific intent of the paper, especially:

- Research goal
- Research method

The service uses a Retrieval-Augmented Generation pipeline to focus the language model on the most relevant parts of the paper before generating the final output.

## What This Backend Does

When you call the analyze API with a PDF, the backend performs the following steps:

1. Saves the uploaded PDF in backend/uploads.
2. Sends the PDF to GROBID to extract machine-readable text.
3. Cleans and normalizes extracted text.
4. Splits text into chunks.
5. Converts chunks into embeddings using SPECTER2.
6. Stores embeddings in FAISS for similarity search.
7. Retrieves top chunks for two focused queries:
	 - Research objective query
	 - Research methodology query
8. Builds a strong prompt from retrieved context.
9. Sends prompt to Ollama with Qwen model.
10. Returns structured JSON containing short and detailed research goal and research method.

## API Overview

- Endpoint: POST /analyze
- Input: multipart/form-data with one PDF file field named file
- Output: JSON with fields:
	- short_goal
	- detailed_method

## Tech Stack Used

- API framework: FastAPI
- ASGI server: Uvicorn
- PDF scientific parsing: GROBID
- Embedding model: allenai/specter2_base
- Transformer runtime: Hugging Face Transformers + PyTorch
- Vector index: FAISS (CPU)
- LLM runtime: Ollama
- LLM used: qwen2.5:14b
- Language: Python 3.11 (recommended)

## Models Used

1. Embedding model
- Model: allenai/specter2_base
- Purpose: Convert paper chunks and queries into dense vectors for semantic retrieval.

2. Generation model
- Model: qwen2.5:14b via Ollama
- Purpose: Generate detailed research goal and research method from retrieved context.

## Project Structure (Important Parts)

- backend/main.py: FastAPI app and complete analyze pipeline
- backend/parser/grobid_parser.py: PDF parsing via GROBID API
- backend/embedding/specter_embedding.py: SPECTER2 embedding loading and inference
- backend/rag/vector_store.py: FAISS vector store
- backend/rag/retrieval.py: Top-k semantic retrieval
- backend/config.py: GROBID and Ollama endpoint + model config

## Setup and Installation

Follow these steps on a fresh machine.

### 1) Install Miniconda or Anaconda

Install either:

- Miniconda (lightweight, recommended)
- Anaconda (full distribution)

After install, open a new terminal.

### 2) Clone this repository

From your workspace directory:

git clone https://github.com/CodeByJc/research-bot-backend
cd research-bot

### 3) Ensure GROBID source is present in backend/grobid

If backend/grobid is not already present, clone it:

cd backend
git clone --branch master https://github.com/grobidOrg/grobid grobid
cd ..

### 4) Download SPECTER2 model into backend/models/specter2_base

Create model directory and clone:

mkdir -p backend/models
cd backend/models
git clone https://huggingface.co/allenai/specter2_base
cd ../..

Expected final model path:

backend/models/specter2_base

### 5) Create and activate Conda environment

Example with Python 3.11:

conda create -n research-bot python=3.11 -y
conda activate research-bot

### 6) Install Python dependencies

From repository root:

pip install -r backend/requirements.txt

### 7) Start GROBID with Docker

Run in a separate terminal:

docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.8.0

This exposes GROBID at http://localhost:8070.

### 8) Start backend server

From repository root:

python -m uvicorn main:app --reload

Server runs at:

http://127.0.0.1:8000

## How to Use

You can test with curl:

curl -X POST "http://127.0.0.1:8000/analyze" \
	-F "file=@/absolute/path/to/paper.pdf"

The response will include extracted and expanded research goal and method.

Then use it and have fun.

## Notes and Troubleshooting

- If model loading fails, verify backend/models/specter2_base contains files like config.json and tokenizer files.
- If GROBID parsing fails, make sure Docker container is running on port 8070.
- If Ollama is not running, start it and ensure qwen2.5:14b is available locally.
- If needed, pull the model:
	- ollama pull qwen2.5:14b


