"""
Direct runner script for the RAG demo - no batch files needed.
"""

import os
import subprocess
import time


def run_demo():
    print("=" * 50)
    print("Running Agentic AI Platform RAG Demo...")
    print("=" * 50)

    # Ingest sample documents
    print("\nIngesting sample documents...")
    ingest_cmd = ["python", "simple_rag_demo.py", "--ingest", "--collection", "demo"]
    process = subprocess.run(ingest_cmd, capture_output=True, text=True)

    if process.returncode != 0:
        print("Error during document ingestion:")
        print(process.stderr)
        return

    print(process.stdout)

    # Wait a moment to ensure documents are properly stored
    time.sleep(2)

    # Run a sample query
    print("\nRunning sample query...")
    query_cmd = [
        "python",
        "simple_rag_demo.py",
        "--query",
        "What is the Agentic AI Platform?",
        "--collection",
        "demo",
    ]
    process = subprocess.run(query_cmd, capture_output=True, text=True)

    if process.returncode != 0:
        print("Error during query:")
        print(process.stderr)
        return

    print(process.stdout)

    print("\n" + "=" * 50)
    print("Demo completed! Try with your own queries:")
    print('python simple_rag_demo.py --query "Your question here" --collection demo')
    print("=" * 50)


if __name__ == "__main__":
    run_demo()
