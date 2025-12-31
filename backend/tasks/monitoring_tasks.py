from backend.tasks.celery_app import celery_app


@celery_app.task(name="check_drift")
def check_drift_task(deployment_id: int):
    return {
        "status": "completed",
        "deployment_id": deployment_id,
        "drift_detected": False
    }


@celery_app.task(name="collect_metrics")
def collect_metrics_task(deployment_id: int):
    return {
        "status": "completed",
        "deployment_id": deployment_id,
        "metrics_collected": True
    }
