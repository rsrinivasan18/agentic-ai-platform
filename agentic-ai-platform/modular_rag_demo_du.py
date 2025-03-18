"""
Modular RAG demo script using the project's component structure.
"""

import os
import sys
import argparse
import traceback
from typing import List

# Add current directory to Python path to help with imports
sys.path.append(os.getcwd())

from langchain.schema import Document

# Try different import approaches to make sure at least one works
try:
    # First try importing from src.rag directly
    from src.rag import (
        create_sample_documents,
        load_and_split_documents,
        create_vector_store,
        get_vector_store,
    )
    from src.rag import create_retriever
    from src.llm.model import simple_rag_response, get_llm

    print("Imported using 'from src.rag import...' approach")
except ImportError:
    try:
        # If that fails, try importing from the specific modules
        from src.rag.document_loader import (
            load_and_split_documents,
            create_sample_documents,
        )
        from src.rag.vector_store import create_vector_store, get_vector_store
        from src.rag.retriever import create_retriever
        from src.llm.model import simple_rag_response, get_llm

        print("Imported using 'from src.rag.module import...' approach")
    except ImportError as e:
        print(f"Import error: {e}")
        # If both approaches fail, try a more direct approach
        print("Attempting to load modules directly...")
        import src.rag.document_loader as document_loader
        import src.rag.vector_store as vector_store
        import src.rag.retriever as retriever
        import src.llm.model as model

        # Assign function references
        load_and_split_documents = document_loader.load_and_split_documents
        create_sample_documents = document_loader.create_sample_documents
        create_vector_store = vector_store.create_vector_store
        get_vector_store = vector_store.get_vector_store
        create_retriever = retriever.create_retriever
        simple_rag_response = model.simple_rag_response
        get_llm = model.get_llm
        print("Imported using direct module approach")


def ingest_documents(collection_name: str, docs_path: str = None) -> None:
    """Ingest documents into the vector store."""
    try:
        if docs_path and os.path.exists(docs_path):
            print(f"Loading documents from {docs_path}...")
            documents = load_and_split_documents(docs_path)
        else:
            print("Using sample documents...")
            documents = create_sample_documents()

        print(f"Creating vector store with {len(documents)} documents...")
        create_vector_store(documents, collection_name)
        print(f"Documents ingested into collection '{collection_name}'")
    except Exception as e:
        print(f"Error during document ingestion: {str(e)}")
        traceback.print_exc()


def query_documents(collection_name: str, query: str) -> None:
    """Query the RAG system."""
    try:
        print(f"Querying collection '{collection_name}' with: {query}")

        # Create retriever
        retriever = create_retriever(collection_name)

        # Retrieve documents with scores
        docs_with_scores = retriever.retrieve_with_scores(query)

        # Print retrieved documents
        print("\nRetrieved documents:")
        for i, (doc, score) in enumerate(docs_with_scores):
            print(f"\n{i + 1}. Score: {score:.4f}")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")

        # Extract documents
        documents = [doc for doc, _ in docs_with_scores]

        # Generate response
        try:
            # Get LLM
            llm = get_llm()

            # Generate response
            print("\nGenerating response...")
            response = simple_rag_response(query=query, context_docs=documents, llm=llm)

            print("\n" + "=" * 50)
            print("RAG Response:")
            print(response)
            print("=" * 50)
        except ValueError as ve:
            print(f"\nCould not generate response: {str(ve)}")

    except Exception as e:
        print(f"Error during query: {str(e)}")
        traceback.print_exc()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Modular RAG Demo")
    parser.add_argument(
        "--collection", type=str, default="demo", help="Collection name"
    )
    parser.add_argument("--ingest", action="store_true", help="Ingest documents")
    parser.add_argument("--docs-path", type=str, help="Path to documents")
    parser.add_argument("--query", type=str, help="Query to run")

    args = parser.parse_args()

    if args.ingest:
        ingest_documents(args.collection, args.docs_path)

    if args.query:
        query_documents(args.collection, args.query)

    if not args.ingest and not args.query:
        print(
            "No action specified. Use --ingest to ingest documents or --query to run a query."
        )


if __name__ == "__main__":
    main()
