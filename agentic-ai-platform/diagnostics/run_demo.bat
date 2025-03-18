@echo off
echo Running Agentic AI Platform RAG Demo...

:: Activate conda environment
call conda activate agentic-ai-platform

:: Ingest sample documents
python simple_rag_demo.py --ingest --collection demo

:: Run a sample query
python simple_rag_demo.py --query "What is the Agentic AI Platform?" --collection demo

echo.
echo Demo completed! Try with your own queries:
echo python simple_rag_demo.py --query "Your question here" --collection demo