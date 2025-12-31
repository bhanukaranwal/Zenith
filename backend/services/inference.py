from typing import Dict, Any
import httpx
import torch
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.model import Deployment, ModelVersion
from backend.core.config import settings
from backend.core.telemetry import get_tracer

tracer = get_tracer(__name__)


class InferenceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.triton_url = settings.TRITON_URL
    
    async def deploy_model(self, deployment_id: int) -> str:
        with tracer.start_as_current_span("deploy_model") as span:
            span.set_attribute("deployment_id", deployment_id)
            
            result = await self.db.execute(
                select(Deployment).where(Deployment.id == deployment_id)
            )
            deployment = result.scalar_one_or_none()
            
            if not deployment:
                raise ValueError("Deployment not found")
            
            endpoint_url = f"http://localhost:8000/v1/models/{deployment.name}"
            
            return endpoint_url
    
    async def predict(
        self,
        deployment_id: int,
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        with tracer.start_as_current_span("predict") as span:
            span.set_attribute("deployment_id", deployment_id)
            
            result = await self.db.execute(
                select(Deployment).where(Deployment.id == deployment_id)
            )
            deployment = result.scalar_one_or_none()
            
            if not deployment:
                raise ValueError("Deployment not found")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    deployment.endpoint_url,
                    json=inputs,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Prediction failed: {response.text}")
    
    async def load_model_from_storage(
        self,
        model_version_id: int
    ) -> torch.nn.Module:
        result = await self.db.execute(
            select(ModelVersion).where(ModelVersion.id == model_version_id)
        )
        version = result.scalar_one_or_none()
        
        if not version:
            raise ValueError("Model version not found")
        
        model_path = Path(version.storage_path)
        
        if version.framework == "pytorch":
            model = torch.load(model_path)
            model.eval()
            return model
        else:
            raise ValueError(f"Unsupported framework: {version.framework}")


class VLLMInferenceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vllm_enabled = False
    
    async def generate_text(
        self,
        model_name: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 512
    ) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.TRITON_URL}/v1/completions",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=60.0
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["text"]
            else:
                raise Exception(f"Generation failed: {response.text}")
