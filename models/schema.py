from pydantic import BaseModel

class OutputSchema(BaseModel):
    """Structured fields expected from paper-analysis output."""

    # One-line statement of the paper's main objective.
    research_goal: str
    # Main approach/technique used by the paper.
    research_methods: str
    # Dataset explicitly used for experiments/evaluation.
    dataset_used: str
    # Core novel contributions reported by the authors.
    key_contributions: str