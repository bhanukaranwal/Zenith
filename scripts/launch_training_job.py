import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.tasks.training_tasks import train_model_task


async def main():
    config = {
        "learning_rate": 0.001,
        "batch_size": 32,
        "num_epochs": 10,
        "optimizer": "adamw"
    }
    
    run_id = 1
    
    print(f"Launching training job for run {run_id}")
    print(f"Config: {config}")
    
    result = train_model_task.apply_async(args=[run_id, config])
    
    print(f"Task submitted with ID: {result.id}")
    print(f"Check task status: result.status")
    
    print("\nWaiting for task completion...")
    final_result = result.get(timeout=600)
    
    print(f"\nTraining completed!")
    print(f"Result: {final_result}")


if __name__ == "__main__":
    asyncio.run(main())
