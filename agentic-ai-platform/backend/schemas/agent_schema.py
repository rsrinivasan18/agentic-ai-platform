"""
Agent schemas for API requests and responses.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    config: Dict[str, Any] = Field(default_factory=dict)


class AgentCreate(AgentBase):
    owner_id: str


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class AgentResponse(AgentBase):
    id: str
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AgentQuery(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)
