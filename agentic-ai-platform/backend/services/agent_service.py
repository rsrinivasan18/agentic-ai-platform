"""
Agent service for handling agent-related operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
import tempfile
import os
import shutil
import asyncio
import logging
from fastapi import UploadFile

from models.agent_model import Agent
from schemas.agent_schema import AgentCreate, AgentUpdate
from db.mongodb import get_database

# Import agents from the src directory
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.agents.rag_agent import RagAgent
from src.agents.search_agent import SearchAgent
from src.agents.ml_model_agent import MLModelAgent

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.agents

        # Map agent types to their classes
        self.agent_classes = {
            "rag": RagAgent,
            "search": SearchAgent,
            "ml": MLModelAgent,
        }

    async def create_agent(self, agent_data: AgentCreate) -> Agent:
        # Validate agent type
        if agent_data.type not in self.agent_classes:
            raise ValueError(
                f"Invalid agent type: {agent_data.type}. Available types: {list(self.agent_classes.keys())}"
            )

        # Create new agent
        agent_dict = agent_data.dict()

        # Convert owner_id to ObjectId
        agent_dict["owner_id"] = ObjectId(agent_dict["owner_id"])

        # Add timestamps
        now = datetime.now()
        agent_dict["created_at"] = now
        agent_dict["updated_at"] = now

        # Insert into database
        result = await self.collection.insert_one(agent_dict)

        # Get the created agent
        created_agent = await self.collection.find_one({"_id": result.inserted_id})

        return Agent(**created_agent)

    async def get_agents(self) -> List[Agent]:
        agents = []
        async for agent in self.collection.find():
            agents.append(Agent(**agent))
        return agents

    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        agent = await self.collection.find_one({"_id": ObjectId(agent_id)})
        if agent:
            return Agent(**agent)
        return None

    async def update_agent(
        self, agent_id: str, agent_data: AgentUpdate
    ) -> Optional[Agent]:
        agent = await self.collection.find_one({"_id": ObjectId(agent_id)})
        if not agent:
            return None

        # Update agent data
        update_data = agent_data.dict(exclude_unset=True)

        # Update timestamp
        update_data["updated_at"] = datetime.now()

        # Update in database
        await self.collection.update_one(
            {"_id": ObjectId(agent_id)}, {"$set": update_data}
        )

        # Get the updated agent
        updated_agent = await self.collection.find_one({"_id": ObjectId(agent_id)})

        return Agent(**updated_agent)

    async def delete_agent(self, agent_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(agent_id)})
        return result.deleted_count > 0

    async def process_query(
        self, agent_id: str, query: str, parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        # Get agent from database
        agent_data = await self.get_agent(agent_id)
        if not agent_data:
            raise ValueError(f"Agent not found: {agent_id}")

        # Get agent class
        agent_class = self.agent_classes.get(agent_data.type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_data.type}")

        # Initialize agent
        config = {**agent_data.config, "name": agent_data.name}
        agent = agent_class(config)

        # Process query
        if agent_data.type == "ml":
            # ML agent takes parameters as input
            result = await agent.process(parameters or {})
        else:
            # Other agents take query string as input
            result = await agent.process(query)

        return result

    async def process_document(
        self, agent_id: str, file: UploadFile, collection_name: Optional[str] = None
    ) -> Dict[str, Any]:
        # Get agent from database
        agent_data = await self.get_agent(agent_id)
        if not agent_data:
            raise ValueError(f"Agent not found: {agent_id}")

        # Ensure agent is a RAG agent
        if agent_data.type != "rag":
            raise ValueError("Document upload is only supported for RAG agents")

        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            # Copy uploaded file content to temp file
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        try:
            # Initialize RAG agent
            config = {**agent_data.config, "name": agent_data.name}
            if collection_name:
                config["collection_name"] = collection_name

            agent = RagAgent(config)

            # Import document loading function
            from src.rag.document_loader import load_and_split_documents

            # Load and split documents
            documents = load_and_split_documents(temp_path)

            # Add documents to agent
            agent.add_documents(documents)

            return {
                "message": f"Successfully processed document: {file.filename}",
                "document_count": len(documents),
            }
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
