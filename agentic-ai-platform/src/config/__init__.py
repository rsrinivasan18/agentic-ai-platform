# Config module initialization

# Import settings to make them available when importing the config module
from src.config.settings import (
    OPENAI_API_KEY,
    CHROMA_PERSIST_DIRECTORY,
    LLM_MODEL,
    EMBEDDING_MODEL,
    API_HOST,
    API_PORT,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
