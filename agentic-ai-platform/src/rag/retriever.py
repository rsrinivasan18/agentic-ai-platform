"""
Retrieval functionality for the RAG system.
"""

from typing import List, Dict, Any, Optional, Tuple

from langchain.schema import Document

from src.rag.vector_store import get_vector_store


class Retriever:
    """Simple retriever class for the RAG system."""

    def __init__(
        self,
        collection_name: str,
        embedding_model_name: Optional[str] = None,
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize the retriever.

        Args:
            collection_name (str): Name of the vector store collection
            embedding_model_name (str, optional): Name of embedding model to use
            persist_directory (str, optional): Directory where vector store is persisted
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name
        self.persist_directory = persist_directory
        self.vector_store = get_vector_store(
            collection_name, embedding_model_name, persist_directory
        )

    def retrieve(
        self, query: str, k: int = 4, filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query (str): The query text
            k (int, optional): Number of documents to retrieve. Defaults to 4.
            filter (Dict[str, Any], optional): Filter criteria. Defaults to None.

        Returns:
            List[Document]: Retrieved documents
        """
        documents = self.vector_store.similarity_search(query=query, k=k, filter=filter)
        return documents

    def retrieve_with_scores(
        self, query: str, k: int = 4, filter: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Document, float]]:
        """
        Retrieve relevant documents with similarity scores.

        Args:
            query (str): The query text
            k (int, optional): Number of documents to retrieve. Defaults to 4.
            filter (Dict[str, Any], optional): Filter criteria. Defaults to None.

        Returns:
            List[Tuple[Document, float]]: Retrieved documents with scores
        """
        documents_with_scores = self.vector_store.similarity_search_with_score(
            query=query, k=k, filter=filter
        )
        return documents_with_scores


def create_retriever(
    collection_name: str,
    embedding_model_name: Optional[str] = None,
    persist_directory: Optional[str] = None,
) -> Retriever:
    """
    Factory function to create a retriever.

    Args:
        collection_name (str): Name of the vector store collection
        embedding_model_name (str, optional): Name of embedding model to use
        persist_directory (str, optional): Directory where vector store is persisted

    Returns:
        Retriever: A configured retriever instance
    """
    return Retriever(
        collection_name=collection_name,
        embedding_model_name=embedding_model_name,
        persist_directory=persist_directory,
    )
