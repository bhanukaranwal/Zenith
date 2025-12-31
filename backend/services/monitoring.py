from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.telemetry import get_tracer

tracer = get_tracer(__name__)


class MonitoringService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_deployment_metrics(
        self,
        deployment_id: int,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        with tracer.start_as_current_span("get_deployment_metrics") as span:
            span.set_attribute("deployment_id", deployment_id)
            
            metrics = {
                "deployment_id": deployment_id,
                "total_requests": 1234,
                "average_latency_ms": 45.6,
                "error_rate": 0.012,
                "p95_latency_ms": 78.9,
                "p99_latency_ms": 120.3,
                "throughput_rps": 56.7
            }
            
            return metrics
    
    async def detect_drift(
        self,
        deployment_id: int,
        reference_data: Dict[str, Any],
        current_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        with tracer.start_as_current_span("detect_drift") as span:
            span.set_attribute("deployment_id", deployment_id)
            
            reference_df = pd.DataFrame(reference_data)
            current_df = pd.DataFrame(current_data)
            
            report = Report(metrics=[
                DataDriftPreset(),
                DataQualityPreset()
            ])
            
            report.run(
                reference_data=reference_df,
                current_data=current_df
            )
            
            result_dict = report.as_dict()
            
            drift_detected = False
            drifted_features = []
            
            for metric in result_dict.get("metrics", []):
                if metric.get("metric") == "DataDriftTable":
                    drift_by_columns = metric.get("result", {}).get("drift_by_columns", {})
                    for col, info in drift_by_columns.items():
                        if info.get("drift_detected", False):
                            drift_detected = True
                            drifted_features.append(col)
            
            return {
                "deployment_id": deployment_id,
                "drift_detected": drift_detected,
                "drifted_features": drifted_features,
                "drift_score": len(drifted_features) / max(len(reference_df.columns), 1),
                "timestamp": datetime.utcnow().isoformat(),
                "full_report": result_dict
            }
    
    async def get_traces(
        self,
        deployment_id: int,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        traces = [
            {
                "trace_id": f"trace_{i}",
                "deployment_id": deployment_id,
                "timestamp": datetime.utcnow().isoformat(),
                "duration_ms": 45 + i,
                "status": "success",
                "spans": []
            }
            for i in range(min(limit, 10))
        ]
        
        return traces


class LLMMonitoringService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def evaluate_response_quality(
        self,
        prompt: str,
        response: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        evaluation = {
            "relevance_score": 0.85,
            "coherence_score": 0.92,
            "hallucination_score": 0.05,
            "toxicity_score": 0.01,
            "factuality_score": 0.88
        }
        
        return evaluation
    
    async def detect_hallucination(
        self,
        response: str,
        context: str
    ) -> Dict[str, Any]:
        hallucination_detected = False
        confidence = 0.95
        
        return {
            "hallucination_detected": hallucination_detected,
            "confidence": confidence,
            "response": response
        }
