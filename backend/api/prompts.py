from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.prompt import PromptTemplate, PromptVersion

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_prompt_template(
    name: str,
    project_id: int,
    description: str = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    template = PromptTemplate(
        name=name,
        description=description,
        project_id=project_id
    )
    
    db.add(template)
    await db.commit()
    await db.refresh(template)
    
    return template


@router.post("/{template_id}/versions", status_code=status.HTTP_201_CREATED)
async def create_prompt_version(
    template_id: int,
    version: str,
    template_text: str,
    variables: list = None,
    model_config: dict = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    prompt_version = PromptVersion(
        template_id=template_id,
        version=version,
        template_text=template_text,
        variables=variables or [],
        model_config=model_config
    )
    
    db.add(prompt_version)
    await db.commit()
    await db.refresh(prompt_version)
    
    return prompt_version


@router.get("")
async def list_prompts(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PromptTemplate)
        .where(PromptTemplate.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    prompts = result.scalars().all()
    return prompts


@router.get("/{template_id}/versions")
async def list_prompt_versions(
    template_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PromptVersion).where(PromptVersion.template_id == template_id)
    )
    versions = result.scalars().all()
    return versions


@router.post("/{template_id}/test")
async def test_prompt(
    template_id: int,
    version: str,
    variables: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PromptVersion)
        .where(PromptVersion.template_id == template_id, PromptVersion.version == version)
    )
    prompt_version = result.scalar_one_or_none()
    
    if not prompt_version:
        raise HTTPException(status_code=404, detail="Prompt version not found")
    
    rendered_prompt = prompt_version.template_text
    for key, value in variables.items():
        rendered_prompt = rendered_prompt.replace(f"{{{key}}}", str(value))
    
    return {"rendered_prompt": rendered_prompt}
