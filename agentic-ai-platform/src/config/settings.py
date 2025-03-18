"""
Configuration settings for the Agentic AI Platform.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector DB Settings
CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# LLM Settings
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
