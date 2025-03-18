"""
Vector store functionality using ChromaDB.
"""

from typing import List, Optional

from langchain.schema import Document

# Updated import for langchain-community
from langchain_community.vectorstores import Chroma

from src.rag.embeddings import get_embeddings_model

# Default persist directory
CHROMA_PERSIST_DIRECTORY = "./chroma_db"


def create_vector_store(
    documents: List[Document],
    collection_name: str,
    embedding_model_name: Optional[str] = None,
    persist_directory: Optional[str] = None,
) -> Chroma:
    """
    Create a new vector store from documents.

    Args:
        documents (List[Document]): List of documents to add to the vector store
        collection_name (str): Name of the collection
        embedding_model_name (str, optional): Name of embedding model to use
        persist_directory (str, optional): Directory to persist the vector store

    Returns:
        Chroma: The created vector store
    """
    embeddings = get_embeddings_model(embedding_model_name)
    persist_dir = persist_directory or CHROMA_PERSIST_DIRECTORY

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name,
    )

    # Persist to disk
    vector_store.persist()

    return vector_store


def get_vector_store(
    collection_name: str,
    embedding_model_name: Optional[str] = None,
    persist_directory: Optional[str] = None,
) -> Chroma:
    """
    Get an existing vector store.

    Args:
        collection_name (str): Name of the collection
        embedding_model_name (str, optional): Name of embedding model to use
        persist_directory (str, optional): Directory where the vector store is persisted

    Returns:
        Chroma: The retrieved vector store
    """
    embeddings = get_embeddings_model(embedding_model_name)
    persist_dir = persist_directory or CHROMA_PERSIST_DIRECTORY

    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    return vector_store


def add_documents(vector_store: Chroma, documents: List[Document]) -> None:
    """
    Add documents to an existing vector store.

    Args:
        vector_store (Chroma): The vector store
        documents (List[Document]): Documents to add
    """
    vector_store.add_documents(documents)
    vector_store.persist()
