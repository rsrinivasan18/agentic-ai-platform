# Agentic AI Platform 
 
An extensible platform for building and deploying AI agents. 
 
## Phases 
 
1. RAG Application 
2. Search Agent and ML Model Agent 
3/4. Interactive UI and Infrastructure 
5. Text to Image Agent 
6. Text to Audio Agent, Stock Screener, Resume Screener 
7. Chain of Thoughts Agent 
8. Master Control Program (MCP) 
9. LLM Configuration System 
11. CI/CD Pipeline 


# Agentic AI Platform

An extensible platform for building and deploying AI agents.

## Overview

This platform allows you to build and deploy various AI agents, starting with a Retrieval-Augmented Generation (RAG) system as the foundation. The platform is designed to be modular and extensible, making it easy to add new types of agents and capabilities.

## Project Phases

1. **RAG Application** (Current phase)
2. Search Agent and ML Model Agent
3/4. Interactive UI and Infrastructure
5. Text to Image Agent
6. Text to Audio Agent, Stock Screener, Resume Screener
7. Chain of Thoughts Agent
8. Master Control Program (MCP)
9. LLM Configuration System
11. CI/CD Pipeline

## Setup

### Prerequisites

- Python 3.10+
- Conda

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/agentic-ai-platform.git
cd agentic-ai-platform

# Create and activate conda environment
conda create -n agentic-ai-platform python=3.10
conda activate agentic-ai-platform

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory with the following content:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Vector DB Settings
CHROMA_PERSIST_DIRECTORY=./chroma_db

# LLM Settings
LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

## Usage

### Quick Demo

To try the RAG system with sample documents:

```bash
python simple_rag_demo.py --ingest --collection demo
python simple_rag_demo.py --query "What is the Agentic AI Platform?" --collection demo
```

### Running the API Server

```bash
python app.py
```

This will start the FastAPI server at http://localhost:8000.

### API Endpoints

1. **Create a Collection**
   ```
   POST /api/collections/create?collection_name=your_collection
   ```

2. **Upload Documents**
   ```
   POST /api/documents/upload
   Form data:
   - collection_name: your_collection
   - file: your_document.pdf
   ```

3. **Query the RAG System**
   ```
   POST /api/rag/query
   Body:
   {
     "collection_name": "your_collection",
     "query": "Your question here?",
     "k": 4,
     "temperature": 0.0
   }
   ```

## Project Structure

```
agentic-ai-platform/
├── .env                 # Environment variables
├── app.py               # Main FastAPI application
├── simple_rag_demo.py   # Demo script
├── src/
│   ├── config/          # Configuration settings
│   ├── rag/             # RAG components
│   ├── llm/             # LLM interface
│   ├── agents/          # Agent definitions
│   └── api/             # API routes
```

## License

MIT