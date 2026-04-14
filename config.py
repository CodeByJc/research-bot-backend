# GROBID endpoint for converting PDF papers into machine-readable text/TEI.
GROBID_URL = "http://localhost:8070/api/processHeaderDocument"
# Ollama generate endpoint used for non-streaming local inference.
OLLAMA_URL = "http://localhost:11434/api/generate"

# Default local model for response generation.
MODEL_NAME = "qwen2.5:14b"