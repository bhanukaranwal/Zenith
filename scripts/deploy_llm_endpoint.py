import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import httpx


async def deploy_llm_endpoint():
    api_url = "http://localhost:8000/api/v1"
    
    token_response = httpx.post(
        f"{api_url}/auth/login",
        data={"username": "admin", "password": "admin"}
    )
    
    if token_response.status_code != 200:
        print("Login failed")
        return
    
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    deployment_data = {
        "name": "llm-endpoint-prod",
        "model_version_id": 1,
        "config": {
            "batch_size": 8,
            "max_tokens": 512,
            "temperature": 0.7
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_url}/deployments",
            json=deployment_data,
            headers=headers
        )
        
        if response.status_code == 201:
            deployment = response.json()
            print(f"Deployment created successfully!")
            print(f"ID: {deployment['id']}")
            print(f"Name: {deployment['name']}")
            print(f"Endpoint: {deployment.get('endpoint_url', 'Pending')}")
        else:
            print(f"Deployment failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(deploy_llm_endpoint())
