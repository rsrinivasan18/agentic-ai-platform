"""
Integration tests for the Agentic AI Platform API.
"""

import pytest
from httpx import AsyncClient
from main import app
import json
from bson import ObjectId

# Test user data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "password123",
}

# Test agent data
test_agent = {
    "name": "Test RAG Agent",
    "description": "A test RAG agent",
    "type": "rag",
    "config": {"collection_name": "test_collection"},
}


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_and_login(client):
    # Register user
    response = await client.post("/api/auth/register", json=test_user)
    assert response.status_code == 201
    assert response.json()["username"] == test_user["username"]
    assert response.json()["email"] == test_user["email"]

    # Login
    response = await client.post(
        "/api/auth/token",
        data={"username": test_user["username"], "password": test_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_agent(client):
    # First register and login
    token = await test_register_and_login(client)

    # Create agent
    test_agent_copy = test_agent.copy()
    test_agent_copy["owner_id"] = (
        "placeholder"  # Will be replaced by the API with the current user's ID
    )

    response = await client.post(
        "/api/agents",
        json=test_agent_copy,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == test_agent["name"]
    assert response.json()["type"] == test_agent["type"]

    return response.json()["id"], token


@pytest.mark.asyncio
async def test_query_agent(client):
    # First create an agent
    agent_id, token = await test_create_agent(client)

    # Query the agent
    response = await client.post(
        f"/api/agents/{agent_id}/query",
        json={"query": "What is the Agentic AI Platform?"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    # The exact response will depend on the agent implementation
    # but we can check for some expected structure
    assert "answer" in response.json() or "result" in response.json()
