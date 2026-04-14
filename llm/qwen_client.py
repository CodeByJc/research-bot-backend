import requests
from backend.config import OLLAMA_URL, MODEL_NAME

def generate_answer(prompt):
    """Send the composed prompt to Ollama and return the model text output."""

    # Request a single complete response (non-streaming) for simple API usage.
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    # Ollama returns generated text under the "response" key.
    return response.json()["response"]