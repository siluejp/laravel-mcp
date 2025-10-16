from pathlib import Path

# Defines the absolute path to the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Defines the absolute path to the vector store
VECTOR_STORE_PATH = PROJECT_ROOT / "faiss_index"
