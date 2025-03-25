# Agentic AI Platform

A platform for building and deploying AI agents including RAG, Search, and ML Model agents.

## Project Structure

The project is divided into two main parts:

1. **Backend**: FastAPI application with MongoDB for data storage and ChromaDB for vector embeddings
2. **Frontend**: React application with Tailwind CSS for styling

## Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- MongoDB
- Conda (recommended for environment management)

### Backend Setup

```bash
# Create and activate conda environment
conda create -n agentic-ai-platform python=3.10
conda activate agentic-ai-platform

# Set up backend structure and files
python setup_structure.py

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file to add your API keys and configuration

# Start the backend server
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000 with API documentation at http://localhost:8000/docs

### Frontend Setup

```bash
# Set up frontend structure and files
python setup_frontend_complete.py

# Install frontend dependencies
cd frontend
npm install

# Start the frontend development server
npm start
```

The frontend will be available at http://localhost:3000

### Docker Setup

You can also use Docker Compose to run the entire application:

```bash
docker-compose up
```

## Project Phases

1. ✅ Phase 1: Create a simple RAG application
2. ✅ Phase 2: Create a simple Search Agent and a ML Model Agent
3. 🔄 Phase 3/4: Build an interactive UI with Node.js, FAST API, MongoDB, ChromaDB
4. Phase 5: Create a text to Image Agent
5. Phase 6: Create text to Audio Agent, Stock screener, Resume screener
6. Phase 7: Create a Chain of Thoughts Agent
7. Phase 8: Register all agents to MCP (Master Control Program)
8. Phase 9: Make agents flexible to be used with any LLMs
9. Phase 11: Create a CI/CD Pipeline

## Features

- **User Management**: Registration, authentication, and profile management
- **Agent Management**: Create, configure, and interact with different types of agents
- **RAG Agent**: Leverage your own data with language models
- **Search Agent**: Search the web for information and provide answers
- **ML Agent**: Train and deploy machine learning models

## API Endpoints

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/token`: Get authentication token

### Users

- `GET /api/users/`: Get all users
- `GET /api/users/me`: Get current user info
- `GET /api/users/{user_id}`: Get specific user
- `PUT /api/users/{user_id}`: Update user
- `DELETE /api/users/{user_id}`: Delete user

### Agents

- `GET /api/agents/`: Get all agents
- `POST /api/agents/`: Create new agent
- `GET /api/agents/{agent_id}`: Get specific agent
- `PUT /api/agents/{agent_id}`: Update agent
- `DELETE /api/agents/{agent_id}`: Delete agent
- `POST /api/agents/{agent_id}/query`: Query an agent
- `POST /api/agents/{agent_id}/upload`: Upload document to RAG agent

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.