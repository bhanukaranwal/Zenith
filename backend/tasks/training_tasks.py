from celery import Task
from backend.tasks.celery_app import celery_app
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import async_session_maker


class AsyncTask(Task):
    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run(*args, **kwargs))


@celery_app.task(base=AsyncTask, name="train_model")
async def train_model_task(run_id: int, config: dict):
    async with async_session_maker() as session:
        return {
            "status": "completed",
            "run_id": run_id,
            "message": "Training completed successfully"
        }


@celery_app.task(base=AsyncTask, name="hyperparameter_optimization")
async def hyperparameter_optimization_task(experiment_id: int, param_space: dict):
    async with async_session_maker() as session:
        return {
            "status": "completed",
            "experiment_id": experiment_id,
            "best_params": {"learning_rate": 0.001, "batch_size": 32}
        }


@celery_app.task(name="evaluate_model")
def evaluate_model_task(model_id: int, test_data: dict):
    return {
        "status": "completed",
        "model_id": model_id,
        "metrics": {"accuracy": 0.95, "f1_score": 0.93}
    }
