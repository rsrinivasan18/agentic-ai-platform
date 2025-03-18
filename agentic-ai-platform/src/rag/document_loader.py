"""
Document loading and text splitting functionality.
"""

import os
from typing import List

# Updated imports for langchain-community
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    DirectoryLoader,
)
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_documents(source_path: str) -> List[Document]:
    """
    Load documents from a file or directory.

    Args:
        source_path (str): Path to file or directory

    Returns:
        List[Document]: List of loaded documents
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Path not found: {source_path}")

    if os.path.isdir(source_path):
        # Handle directory of files
        return _load_directory(source_path)
    else:
        # Handle single file
        return _load_file(source_path)


def _load_file(file_path: str) -> List[Document]:
    """Load a single file based on its extension."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".csv":
        loader = CSVLoader(file_path)
    elif ext in [".txt", ".md", ".py", ".js", ".html", ".css"]:
        loader = TextLoader(file_path)
    else:
        # Default to text loader for unknown types
        loader = TextLoader(file_path)

    return loader.load()


def _load_directory(dir_path: str) -> List[Document]:
    """Load all supported files from a directory."""
    loader = DirectoryLoader(
        dir_path,
        glob="**/*.*",
        loader_cls=TextLoader,
        loader_kwargs={"autodetect_encoding": True},
    )
    return loader.load()


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks for better embedding and retrieval.

    Args:
        documents (List[Document]): List of documents to split

    Returns:
        List[Document]: List of document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    return text_splitter.split_documents(documents)


def load_and_split_documents(source_path: str) -> List[Document]:
    """
    Convenience function to load and split documents in one call.

    Args:
        source_path (str): Path to file or directory

    Returns:
        List[Document]: List of document chunks
    """
    documents = load_documents(source_path)
    return split_documents(documents)


def create_sample_documents() -> List[Document]:
    """Create sample documents for testing."""
    docs = [
        Document(
            page_content="The Agentic AI Platform is designed to help users build and deploy AI agents.",
            metadata={"source": "sample", "title": "Overview"},
        ),
        Document(
            page_content="RAG (Retrieval-Augmented Generation) combines retrieval systems with generative AI.",
            metadata={"source": "sample", "title": "RAG"},
        ),
        Document(
            page_content="Phase 1 of the project involves building a simple RAG application.",
            metadata={"source": "sample", "title": "Phase 1"},
        ),
        Document(
            page_content="Phase 2 involves creating a Search Agent and ML Model Agent.",
            metadata={"source": "sample", "title": "Phase 2"},
        ),
        Document(
            page_content="The platform will use Node.js, FastAPI, MongoDB, and ChromaDB for the backend.",
            metadata={"source": "sample", "title": "Technology Stack"},
        ),
    ]
    return docs
