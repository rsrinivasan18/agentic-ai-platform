"""
API routes for agent management and interaction.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Body,
    File,
    UploadFile,
    Form,
)
from typing import List, Optional, Dict, Any

from models.user_model import User
from models.agent_model import Agent
from schemas.agent_schema import AgentCreate, AgentResponse, AgentUpdate, AgentQuery
from services.agent_service import AgentService
from utils.security import get_current_user

router = APIRouter()


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate, current_user: User = Depends(get_current_user)
):
    # Set the owner_id to the current user
    agent_data.owner_id = str(current_user.id)

    agent_service = AgentService()
    try:
        agent = await agent_service.create_agent(agent_data)
        return agent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AgentResponse])
async def get_agents(current_user: User = Depends(get_current_user)):
    agent_service = AgentService()
    # In a real application, you might want to filter by owner_id
    agents = await agent_service.get_agents()
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, current_user: User = Depends(get_current_user)):
    agent_service = AgentService()
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
):
    agent_service = AgentService()
    # Check if agent exists and user is the owner
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if str(agent.owner_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this agent",
        )

    updated_agent = await agent_service.update_agent(agent_id, agent_data)
    return updated_agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(agent_id: str, current_user: User = Depends(get_current_user)):
    agent_service = AgentService()
    # Check if agent exists and user is the owner
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if str(agent.owner_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this agent",
        )

    deleted = await agent_service.delete_agent(agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
    return None


@router.post("/{agent_id}/query", status_code=status.HTTP_200_OK)
async def query_agent(
    agent_id: str,
    query_data: AgentQuery,
    current_user: User = Depends(get_current_user),
):
    agent_service = AgentService()
    # Check if agent exists
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    try:
        # Process the query based on agent type
        result = await agent_service.process_query(
            agent_id, query_data.query, query_data.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_id}/upload", status_code=status.HTTP_200_OK)
async def upload_document(
    agent_id: str,
    file: UploadFile = File(...),
    collection_name: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
):
    agent_service = AgentService()
    # Check if agent exists and user is the owner
    agent = await agent_service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if str(agent.owner_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload documents to this agent",
        )

    if agent.type != "rag":
        raise HTTPException(
            status_code=400, detail="Document upload is only supported for RAG agents"
        )

    try:
        # Process the uploaded document
        result = await agent_service.process_document(agent_id, file, collection_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
