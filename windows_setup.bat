@echo off
echo Setting up Agentic AI Platform project structure...

:: Create main directory if it doesn't exist
mkdir agentic-ai-platform
cd agentic-ai-platform

:: Create the requirements.txt file
echo langchain>=0.1.0 > requirements.txt
echo chromadb>=0.4.22 >> requirements.txt
echo sentence-transformers>=2.2.2 >> requirements.txt
echo openai>=1.10.0 >> requirements.txt
echo tiktoken>=0.5.1 >> requirements.txt
echo fastapi>=0.104.1 >> requirements.txt
echo uvicorn>=0.23.2 >> requirements.txt
echo pydantic>=2.4.2 >> requirements.txt
echo python-dotenv>=1.0.0 >> requirements.txt

:: Create .env file
echo # API Keys > .env
echo OPENAI_API_KEY=your_openai_api_key_here >> .env
echo. >> .env
echo # Vector DB Settings >> .env
echo CHROMA_PERSIST_DIRECTORY=./chroma_db >> .env
echo. >> .env
echo # LLM Settings >> .env
echo LLM_MODEL=gpt-3.5-turbo >> .env
echo EMBEDDING_MODEL=all-MiniLM-L6-v2 >> .env
echo. >> .env
echo # API Settings >> .env
echo API_HOST=0.0.0.0 >> .env
echo API_PORT=8000 >> .env

:: Create README.md
echo # Agentic AI Platform > README.md
echo. >> README.md
echo An extensible platform for building and deploying AI agents. >> README.md
echo. >> README.md
echo ## Phases >> README.md
echo. >> README.md
echo 1. RAG Application >> README.md
echo 2. Search Agent and ML Model Agent >> README.md
echo 3/4. Interactive UI and Infrastructure >> README.md
echo 5. Text to Image Agent >> README.md
echo 6. Text to Audio Agent, Stock Screener, Resume Screener >> README.md
echo 7. Chain of Thoughts Agent >> README.md
echo 8. Master Control Program (MCP) >> README.md
echo 9. LLM Configuration System >> README.md
echo 11. CI/CD Pipeline >> README.md

:: Create directory structure
mkdir src
mkdir src\config
mkdir src\rag
mkdir src\llm
mkdir src\agents
mkdir src\api

:: Create empty __init__.py files
echo. > src\__init__.py
echo. > src\config\__init__.py
echo. > src\rag\__init__.py
echo. > src\llm\__init__.py
echo. > src\agents\__init__.py
echo. > src\api\__init__.py

echo Project setup complete!
echo.
echo Next steps:
echo 1. Update the .env file with your API keys
echo 2. Create conda environment with: conda create -n agentic-ai-platform python=3.10
echo 3. Activate conda environment with: conda activate agentic-ai-platform
echo 4. Install dependencies with: pip install -r requirements.txt
echo 5. Initialize Git repository with: git init
echo 6. Create .gitignore file
echo 7. Make initial commit and push to GitHub
