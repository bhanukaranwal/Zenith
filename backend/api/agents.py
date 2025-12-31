from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.agent import Agent, AgentExecution
from backend.services.agents import AgentService

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_agent(
    name: str,
    project_id: int,
    agent_type: str,
    config: dict,
    tools: list = None,
    description: str = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    agent = Agent(
        name=name,
        description=description,
        project_id=project_id,
        agent_type=agent_type,
        config=config,
        tools=tools or []
    )
    
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    
    return agent


@router.get("")
async def list_agents(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agent)
        .where(Agent.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    agents = result.scalars().all()
    return agents


@router.post("/{agent_id}/execute")
async def execute_agent(
    agent_id: int,
    input_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    agent_service = AgentService(db)
    execution = await agent_service.execute_agent(agent_id, input_data)
    return execution


@router.get("/{agent_id}/executions")
async def list_executions(
    agent_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AgentExecution)
        .where(AgentExecution.agent_id == agent_id)
        .offset(skip)
        .limit(limit)
    )
    executions = result.scalars().all()
    return executions
