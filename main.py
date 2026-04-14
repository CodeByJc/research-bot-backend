from fastapi import FastAPI, UploadFile, File
import os
import json
import re
from backend.parser.grobid_parser import parse_with_grobid
from backend.utils.preprocess import clean_text
from backend.rag.chunking import chunk_text
from backend.embedding.specter_embedding import get_embedding
from backend.rag.vector_store import VectorStore
from backend.rag.retrieval import retrieve_chunks
from backend.llm.qwen_client import generate_answer

app = FastAPI()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    """Run end-to-end paper analysis and return a structured LLM summary."""

    # 1. Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    print("File saved:", file.filename)

    # 2. Parse
    raw_text = parse_with_grobid(file_path)
    print("Parsed text length:", len(raw_text))

    # 3. Clean
    clean = clean_text(raw_text)
    print("🧹 Cleaned text length:", len(clean))

    # 4. Chunk
    chunks = chunk_text(clean)
    # Limit chunk count to reduce latency and model cost for this endpoint.
    chunks = chunks[:20]

    print("Number of chunks:", len(chunks))

    # PRINT SAMPLE CHUNKS (important)
    for i, c in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i} ---\n{c[:200]}...\n")


    # 5. Embeddings
    embeddings = [get_embedding(c) for c in chunks]

    print("Embedding dimension:", len(embeddings[0]))
    print("Sample embedding:", embeddings[0][:5])  # first 5 values

    # 6. Vector DB
    vs = VectorStore(len(embeddings[0]))
    vs.add(embeddings, chunks)
    print("📦 Stored embeddings in FAISS")

    # 7. Retrieval
    # Use a fixed analysis query so retrieval focuses on objective + methodology.
    # query = """
    # Identify the core research objective and the methodology used in this scientific paper.
    # Focus on abstract, introduction, and methodology sections.
    # """
    # query = """
    # research objective problem statement contribution
    # methodology method algorithm model framework approach
    # abstract introduction methodology section     
    # """

    # top_chunks = retrieve_chunks(vs, query, k=4)

    goal_query = """
    core research objective problem statement main contribution research question
    abstract introduction motivation
    """

    method_query = """
    methodology proposed method algorithm model framework technique approach
    method section experimental setup system design
    """

    goal_chunks = retrieve_chunks(vs, goal_query, k=2)
    method_chunks = retrieve_chunks(vs, method_query, k=4)

    top_chunks = list(dict.fromkeys(goal_chunks + method_chunks))
    context = " ".join(top_chunks)

    print("Number of Top chunks:", len(top_chunks))

    print("\n🎯 Retrieved Top Chunks:")
    for i, tc in enumerate(top_chunks):
        print(f"\n--- Top Chunk {i} ---\n{tc[:200]}...\n")

    context = " ".join(top_chunks)

    # 8. Prompt
    # prompt = f"""
    # You are an expert research assistant.

    # Extract:
    # 1. Core Research Goal
    # 2. Core Research Method

    # Rules:
    # - Short (1-2 lines each)
    # - No copying
    # - Clear explanation

    # Text:
    # {context}

    # Return JSON:
    # {{
    # "research_goal": "...",
    # "research_method": "..."
    # }}
    # """

    prompt = f"""
    You are a senior interdisciplinary research scientist with expertise across computer science, mathematics, statistics, physics, and engineering.

    Your task is to extract the **core scientific contribution** of the paper from the provided text.

    Extract the following (STRICT LENGTH + EXPANSION REQUIRED):

    1. Short Research Goal → EXACTLY 2 sentences (minimum 25 words total)
    2. Short Research Method → EXACTLY 3 sentences (minimum 50 words total)
    3. Detailed Research Goal → EXACTLY 4 sentences (~80–100 words)
    4. Detailed Research Method → EXACTLY 7–8 sentences (~120–150 words)

    MANDATORY RULES:
    - If output is too short → EXPAND with more technical detail
    - Add explanation of components, variables, or process to increase length
    - Do NOT keep answers concise
    - Do NOT stop early

    Method-Specific Rules:
    - Always name the actual technique:
    - Algorithms (e.g., EM, MCMC, optimization)
    - Models (e.g., Bayesian model, neural network, ODE system)
    - Frameworks (e.g., causal inference, variational method)
    - Theory (e.g., convergence analysis, error bounds)

    - Avoid vague phrases like:
    "uses machine learning"
    "applies statistical methods"

    - Instead use:
    "proposes a transformer-based architecture"
    "derives convergence guarantees for stochastic optimization"

    Uncertainty Handling:
    - If method is implicit, infer best possible technical description
    - Do NOT hallucinate unsupported techniques

    Text:
    {context}

    Return ONLY valid JSON (no extra text, no explanation):

    {{
    "short_goal": "...",
    "short_method": "...",
    "detailed_goal": "...",
    "detailed_method": "..."
    }}
    """

    # 9. LLM
    result = generate_answer(prompt)

    # print("🤖 LLM Output:", result)

    # # return {"result": result}
    # clean_result = result.strip()

    # # remove markdown ```json ``` if present
    # if clean_result.startswith("```"):
    #     clean_result = clean_result.split("```")[1]  # remove first ```
    #     clean_result = clean_result.replace("json", "", 1).strip()
    #     clean_result = clean_result.replace("```", "").strip()

    # try:
    #     return json.loads(clean_result)
    # except Exception as e:
    #     print("❌ JSON Parse Error:", e)
    #     return {"raw_output": result}
    
    print("🤖 LLM Output:", result)

    def extract_json(text):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        return match.group(0) if match else None

    clean_result = extract_json(result)

    if clean_result:
        try:
            parsed = json.loads(clean_result)
            return parsed
        except Exception as e:
            print("❌ JSON Parse Error:", e)
            return {"raw_output": result}
    else:
        print("❌ No JSON found in output")
        return {"raw_output": result}