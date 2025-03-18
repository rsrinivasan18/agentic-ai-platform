"""
Demo script for the Agentic AI Platform agents.
"""

import os
import sys
import asyncio
import argparse
import json
import pandas as pd
from typing import Dict, Any, List, Optional
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.getcwd())

from langchain.schema import Document

# Import agents
from src.agents.rag_agent import RagAgent
from src.agents.search_agent import SearchAgent
from src.agents.ml_model_agent import MLModelAgent

# Sample data for ML demo
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


async def demo_rag_agent(query: str) -> None:
    """
    Demo for the RAG Agent.

    Args:
        query (str): Query to process
    """
    print("\n" + "=" * 50)
    print("RAG Agent Demo")
    print("=" * 50)

    try:
        # Initialize agent
        config = {"collection_name": "demo", "name": "RAG Demo Agent"}
        agent = RagAgent(config)

        # Load sample documents
        documents = load_sample_documents()
        agent.add_documents(documents)

        print(f"Loaded {len(documents)} sample documents into collection 'demo'")

        # Process query
        print(f"\nProcessing query: {query}")
        result = await agent.process(query)

        # Print result
        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for i, doc in enumerate(result["source_documents"][:2], 1):
            print(f"{i}. {doc['content']} (Score: {doc['score']:.4f})")

    except Exception as e:
        print(f"Error in RAG Agent demo: {str(e)}")
        traceback.print_exc()


async def demo_search_agent(query: str) -> None:
    """
    Demo for the Search Agent.

    Args:
        query (str): Query to process
    """
    print("\n" + "=" * 50)
    print("Search Agent Demo")
    print("=" * 50)

    try:
        # Initialize agent
        config = {"name": "Search Demo Agent", "num_results": 3}
        agent = SearchAgent(config)

        # Process query
        print(f"\nProcessing query: {query}")
        result = await agent.process(query)

        # Print result
        print("\nAnswer:")
        print(result["answer"])

        print("\nSearch Results:")
        for i, result_item in enumerate(result["search_results"][:2], 1):
            print(f"{i}. {result_item['title']}")
            print(f"   URL: {result_item['link']}")
            print(f"   Snippet: {result_item['snippet'][:100]}...")

    except Exception as e:
        print(f"Error in Search Agent demo: {str(e)}")
        traceback.print_exc()


async def demo_ml_agent() -> None:
    """Demo for the ML Model Agent."""
    print("\n" + "=" * 50)
    print("ML Model Agent Demo")
    print("=" * 50)

    try:
        # Initialize agent
        config = {"name": "ML Model Demo Agent"}
        agent = MLModelAgent(config)

        # Prepare input data
        input_data = {
            "data": SAMPLE_IRIS_DATA,
            "model_type": "random_forest_classifier",
            "target_column": "species",
            "task_type": "classification",
        }

        print("Training a Random Forest classifier on Iris dataset sample...")
        result = await agent.process(input_data)

        # Print result
        print("\nModel trained successfully!")
        print(f"Model type: {result['model_type']}")
        print(f"Task type: {result['task_type']}")
        print(f"Data shape: {result['data_shape']}")

        print("\nMetrics:")
        for metric, value in result["metrics"].items():
            print(f"{metric}: {value:.4f}")

        print("\nExplanation:")
        print(result["explanation"])

    except Exception as e:
        print(f"Error in ML Model Agent demo: {str(e)}")
        traceback.print_exc()


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Agentic AI Platform Demo")
    parser.add_argument(
        "--agent",
        type=str,
        choices=["rag", "search", "ml", "all"],
        default="all",
        help="Agent to demo",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What is the Agentic AI Platform?",
        help="Query for RAG and Search agents",
    )

    args = parser.parse_args()

    if args.agent == "rag" or args.agent == "all":
        await demo_rag_agent(args.query)

    if args.agent == "search" or args.agent == "all":
        await demo_search_agent(args.query)

    if args.agent == "ml" or args.agent == "all":
        await demo_ml_agent()


if __name__ == "__main__":
    asyncio.run(main())
