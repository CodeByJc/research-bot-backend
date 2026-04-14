def clean_text(text):
    """Normalize whitespace so downstream chunking/embedding is consistent."""
    # Flatten line breaks that can fragment sentence context.
    text = text.replace("\n", " ")
    # Collapse repeated spaces/tabs into single spaces.
    text = " ".join(text.split())
    return text