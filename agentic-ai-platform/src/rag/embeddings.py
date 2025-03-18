"""
Embedding models for text-to-vector conversion.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Updated imports for langchain-community
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings


def get_embeddings_model(model_name: Optional[str] = None):
    """
    Get the embedding model based on specified model name or default.

    Args:
        model_name (str, optional): Name of embedding model to use. Defaults to None.

    Returns:
        Object: A configured embedding model instance
    """
    model_name = model_name or "all-MiniLM-L6-v2"

    # Use Hugging Face models by default for cost efficiency
    if "openai" in model_name.lower() and OPENAI_API_KEY:
        # For OpenAI embeddings (e.g., text-embedding-ada-002)
        return OpenAIEmbeddings(model=model_name, openai_api_key=OPENAI_API_KEY)
    else:
        # For Hugging Face models (e.g., all-MiniLM-L6-v2)
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
