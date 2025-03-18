"""
Direct RAG demo without using subprocess or external scripts.
"""

import os
import sys
from typing import List

from langchain.schema import Document

# Make sure src is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import our modules
from src.rag.document_loader import load_and_split_documents
from src.rag.vector_store import create_vector_store, get_vector_store
from src.rag.retriever import create_retriever
from src.llm.model import simple_rag_response, get_llm
from src.config.settings import OPENAI_API_KEY


def create_sample_documents() -> List[Document]:
    """Create sample documents for testing."""
    print("Creating sample documents...")
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


def run_demo():
    """Run the complete demo in one function."""
    print("=" * 50)
    print("Running Agentic AI Platform RAG Demo...")
    print("=" * 50)

    # Check if OpenAI API key is set
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY is not set in your .env file!")
        print("Please set it and try again.")
        return

    collection_name = "demo"

    # Step 1: Create and ingest sample documents
    print("\nStep 1: Ingesting sample documents...")
    try:
        documents = create_sample_documents()
        print(f"Created {len(documents)} sample documents")

        # Create the vector store
        print(f"Creating vector store with collection name: {collection_name}")
        vector_store = create_vector_store(documents, collection_name)
        print("Documents successfully ingested into vector store")
    except Exception as e:
        print(f"Error during document ingestion: {str(e)}")
        return

    # Step 2: Query the system
    print("\nStep 2: Querying the system...")
    try:
        query = "What is the Agentic AI Platform?"
        print(f"Query: {query}")

        # Create retriever
        retriever = create_retriever(collection_name)

        # Retrieve documents
        print("Retrieving relevant documents...")
        docs_with_scores = retriever.retrieve_with_scores(query)

        # Print retrieved documents
        print("\nRetrieved documents:")
        for i, (doc, score) in enumerate(docs_with_scores):
            print(f"\n{i + 1}. Score: {score:.4f}")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")

        # Generate response
        print("\nGenerating response from LLM...")
        documents = [doc for doc, _ in docs_with_scores]
        response = simple_rag_response(query, documents)

        print("\n" + "=" * 50)
        print("RAG Response:")
        print(response)
        print("=" * 50)
    except Exception as e:
        print(f"Error during query: {str(e)}")
        import traceback

        traceback.print_exc()
        return

    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)


if __name__ == "__main__":
    run_demo()
