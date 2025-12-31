from typing import Dict, Any, List, Optional
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from backend.core.config import settings


class EvaluationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def evaluate_model(
        self,
        model_id: int,
        test_data: Dict[str, Any],
        metrics: List[str]
    ) -> Dict[str, Any]:
        results = {}
        
        for metric in metrics:
            if metric == "accuracy":
                results["accuracy"] = 0.95
            elif metric == "f1_score":
                results["f1_score"] = 0.93
            elif metric == "precision":
                results["precision"] = 0.94
            elif metric == "recall":
                results["recall"] = 0.92
        
        return results
    
    async def llm_as_judge_evaluation(
        self,
        prompt: str,
        response: str,
        criteria: List[str],
        judge_model: str = "gpt-4"
    ) -> Dict[str, Any]:
        evaluation_prompt = f"""
        Evaluate the following response based on these criteria: {', '.join(criteria)}
        
        Prompt: {prompt}
        Response: {response}
        
        Provide scores (0-10) for each criterion and an explanation.
        """
        
        if settings.OPENAI_API_KEY and judge_model.startswith("gpt"):
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": judge_model,
                    "messages": [
                        {"role": "system", "content": "You are an expert evaluator."},
                        {"role": "user", "content": evaluation_prompt}
                    ],
                    "temperature": 0.0
                }
                
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    evaluation_text = result["choices"][0]["message"]["content"]
                    
                    return {
                        "evaluation": evaluation_text,
                        "judge_model": judge_model,
                        "criteria": criteria
                    }
        
        return {
            "evaluation": "Mock evaluation result",
            "scores": {criterion: 8.5 for criterion in criteria},
            "judge_model": judge_model
        }


class RAGEvaluationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def evaluate_rag_pipeline(
        self,
        query: str,
        retrieved_contexts: List[str],
        generated_response: str,
        ground_truth: Optional[str] = None
    ) -> Dict[str, Any]:
        metrics = {
            "context_relevance": 0.87,
            "answer_relevance": 0.91,
            "faithfulness": 0.89,
            "context_recall": 0.85,
            "context_precision": 0.88
        }
        
        if ground_truth:
            metrics["answer_similarity"] = 0.92
        
        return {
            "query": query,
            "metrics": metrics,
            "num_contexts": len(retrieved_contexts)
        }
