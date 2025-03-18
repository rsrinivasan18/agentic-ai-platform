"""
Simplified demo script for the Agentic AI Platform agents.
This version doesn't use async functionality for better compatibility.
"""

import os
import sys
import argparse
import traceback
from typing import List
from dotenv import load_dotenv

# Load environment variables
print("Starting simple agent demo...")
load_dotenv()

# Add current directory to Python path
sys.path.append(os.getcwd())

from langchain.schema import Document

print("Setting up demo data...")


# Sample documents for RAG demo
def load_sample_documents() -> List[Document]:
    """Load sample documents for RAG demo."""
    return [
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


# Sample ML data
SAMPLE_IRIS_DATA = [
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "species": "setosa",
    },
    {
        "sepal_length": 4.9,
        "sepal_width": 3.0,
        "petal_length": 1.4,
        "petal_width": 0.2,
        "species": "setosa",
    },
    {
        "sepal_length": 7.0,
        "sepal_width": 3.2,
        "petal_length": 4.7,
        "petal_width": 1.4,
        "species": "versicolor",
    },
    {
        "sepal_length": 6.4,
        "sepal_width": 3.2,
        "petal_length": 4.5,
        "petal_width": 1.5,
        "species": "versicolor",
    },
    {
        "sepal_length": 6.3,
        "sepal_width": 3.3,
        "petal_length": 6.0,
        "petal_width": 2.5,
        "species": "virginica",
    },
    {
        "sepal_length": 5.8,
        "sepal_width": 2.7,
        "petal_length": 5.1,
        "petal_width": 1.9,
        "species": "virginica",
    },
]


def demo_rag():
    """Demo the RAG functionality without the agent wrapper."""
    print("\n" + "=" * 50)
    print("RAG Demo")
    print("=" * 50)

    try:
        # Import only what we need
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_community.chat_models import ChatOpenAI
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        # Get API key
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            print("WARNING: OPENAI_API_KEY not found. LLM functionality will not work.")
            return

        # Constants
        CHROMA_PERSIST_DIRECTORY = "./demo_chroma_db"
        COLLECTION_NAME = "simple_demo"

        print("Loading documents...")
        documents = load_sample_documents()

        print("Setting up embedding model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        print("Creating vector store...")
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
            collection_name=COLLECTION_NAME,
        )
        vector_store.persist()

        print("Setting up LLM...")
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo", temperature=0.0, openai_api_key=OPENAI_API_KEY
        )

        query = "What is the Agentic AI Platform?"
        print(f"Processing query: {query}")

        # Retrieve documents
        docs_with_scores = vector_store.similarity_search_with_score(query, k=2)

        # Print retrieved documents
        print("\nRetrieved documents:")
        for i, (doc, score) in enumerate(docs_with_scores, 1):
            print(f"{i}. {doc.page_content} (Score: {score:.4f})")

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
        documents = [doc for doc, _ in docs_with_scores]
        context_text = "\n\n".join([doc.page_content for doc in documents])

        # Generate response
        print("\nGenerating response...")
        response = chain.run(context=context_text, question=query)

        print("\nResponse:")
        print(response)

    except Exception as e:
        print(f"Error in RAG demo: {str(e)}")
        traceback.print_exc()


def demo_ml():
    """Demo the ML functionality without the agent wrapper."""
    print("\n" + "=" * 50)
    print("ML Demo")
    print("=" * 50)

    try:
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
        )

        print("Preparing data...")
        df = pd.DataFrame(SAMPLE_IRIS_DATA)

        # Split data
        X = df.drop(columns=["species"])
        y = df["species"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        print("Training Random Forest classifier...")
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        print("Making predictions...")
        y_pred = model.predict(X_test)

        print("Calculating metrics...")
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, average="weighted"),
            "recall": recall_score(y_test, y_pred, average="weighted"),
            "f1": f1_score(y_test, y_pred, average="weighted"),
        }

        print("\nMetrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

    except Exception as e:
        print(f"Error in ML demo: {str(e)}")
        traceback.print_exc()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Simplified Agentic AI Platform Demo")
    parser.add_argument(
        "--demo",
        type=str,
        choices=["rag", "ml", "all"],
        default="all",
        help="Demo to run",
    )

    args = parser.parse_args()

    if args.demo == "rag" or args.demo == "all":
        demo_rag()

    if args.demo == "ml" or args.demo == "all":
        demo_ml()


if __name__ == "__main__":
    try:
        print("Running main function...")
        main()
        print("Demo completed successfully!")
    except Exception as e:
        print(f"Error in main function: {e}")
        traceback.print_exc()
