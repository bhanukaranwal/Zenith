import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import httpx
import pandas as pd
import numpy as np


async def run_monitoring_check():
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
    
    np.random.seed(42)
    reference_data = {
        "age": list(np.random.randint(18, 80, 1000)),
        "income": list(np.random.randint(20000, 200000, 1000)),
        "score": list(np.random.uniform(0, 1, 1000))
    }
    
    current_data = {
        "age": list(np.random.randint(18, 80, 1000)),
        "income": list(np.random.randint(25000, 180000, 1000)),
        "score": list(np.random.uniform(0.1, 0.9, 1000))
    }
    
    deployment_id = 1
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{api_url}/monitoring/deployments/{deployment_id}/drift",
            json={
                "reference_data": reference_data,
                "current_data": current_data
            },
            headers=headers,
            timeout=60.0
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Drift Check Results:")
            print(f"Drift Detected: {result['drift_detected']}")
            print(f"Drift Score: {result['drift_score']:.4f}")
            print(f"Drifted Features: {result['drifted_features']}")
        else:
            print(f"Drift check failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(run_monitoring_check())
