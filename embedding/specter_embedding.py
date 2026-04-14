from transformers import AutoTokenizer, AutoModel
import torch
model_path = "models/specter2/specter2_base"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModel.from_pretrained(model_path, local_files_only=True)
def get_embedding(text):
    """Convert input text into a single dense vector using SPECTER2."""
    # Tokenize text into tensors expected by the transformer model.
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    )

    # Inference only: disable gradients to reduce memory and compute overhead.
    with torch.no_grad():
        outputs = model(**inputs)

    # Mean-pool token embeddings to produce one vector for the full chunk/query.
    emb = outputs.last_hidden_state.mean(dim=1)
    return emb.squeeze().numpy()