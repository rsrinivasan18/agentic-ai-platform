"""
Simplified modular RAG demo that avoids import issues.
"""

import os
import sys
import argparse
import traceback
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: No OpenAI API key found. LLM functionality will not work.")

# Import LangChain components directly
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    DirectoryLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
CHROMA_PERSIST_DIRECTORY = "./chroma_db"


# Document loader functions
def load_documents(source_path: str) -> List[Document]:
    """Load documents from a file or directory."""
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Path not found: {source_path}")

    if os.path.isdir(source_path):
        # Handle directory of files
        loader = DirectoryLoader(
            source_path,
            glob="**/*.*",
            loader_cls=TextLoader,
            loader_kwargs={"autodetect_encoding": True},
        )
        return loader.load()
    else:
        # Handle single file
        _, ext = os.path.splitext(source_path)
        ext = ext.lower()

        if ext == ".pdf":
            loader = PyPDFLoader(source_path)
        elif ext == ".csv":
            loader = CSVLoader(source_path)
        else:
            # Default to text loader
            loader = TextLoader(source_path)

        return loader.load()


def split_documents(documents: List[Document]) -> List[Document]:
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    return text_splitter.split_documents(documents)


def load_and_split_documents(source_path: str) -> List[Document]:
    """Load and split documents in one call."""
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


# Vector store functions
def create_vector_store(documents: List[Document], collection_name: str) -> Chroma:
    """Create a vector store from documents."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        collection_name=collection_name,
    )

    # Persist to disk
    vector_store.persist()

    return vector_store


def get_vector_store(collection_name: str) -> Chroma:
    """Get an existing vector store."""
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_store = Chroma(
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    return vector_store


# LLM functions
def get_llm():
    """Get a configured LLM instance."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API key is required but not found. Please set it in your .env file."
        )

    return ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=0.0, openai_api_key=OPENAI_API_KEY
    )


def simple_rag_response(query: str, context_docs: List[Document], llm=None):
    """Generate a RAG response."""
    if llm is None and OPENAI_API_KEY:
        llm = get_llm()
    elif not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is required but not found.")

    # Create prompt
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful AI assistant. Use the following context to answer the user's question.
        If you don't know the answer, just say that you don't know.

        Context:
        {context}

        Question: {question}

        Answer:
        """,
    )

    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Prepare context
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    # Generate response
    response = chain.run(context=context_text, question=query)

    return response


# Main demo functions
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

        # Get vector store
        vector_store = get_vector_store(collection_name)

        # Retrieve documents with scores
        docs_with_scores = vector_store.similarity_search_with_score(query)

        # Print retrieved documents
        print("\nRetrieved documents:")
        for i, (doc, score) in enumerate(docs_with_scores):
            print(f"\n{i + 1}. Score: {score:.4f}")
            print(f"Content: {doc.page_content}")
            print(f"Metadata: {doc.metadata}")

        # Extract documents
        documents = [doc for doc, _ in docs_with_scores]

        # Generate response
        if OPENAI_API_KEY:
            try:
                # Get LLM
                llm = get_llm()

                # Generate response
                print("\nGenerating response...")
                response = simple_rag_response(query, documents, llm)

                print("\n" + "=" * 50)
                print("RAG Response:")
                print(response)
                print("=" * 50)
            except ValueError as ve:
                print(f"\nCould not generate response: {str(ve)}")
        else:
            print("\nNo OpenAI API key found. Skipping response generation.")

    except Exception as e:
        print(f"Error during query: {str(e)}")
        traceback.print_exc()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Simplified Modular RAG Demo")
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
