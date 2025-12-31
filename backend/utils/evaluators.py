from typing import Dict, Any, List, Callable
from abc import ABC, abstractmethod


class BaseEvaluator(ABC):
    @abstractmethod
    async def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass


class AccuracyEvaluator(BaseEvaluator):
    async def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        predictions = inputs.get("predictions", [])
        targets = inputs.get("targets", [])
        
        correct = sum(p == t for p, t in zip(predictions, targets))
        accuracy = correct / len(predictions) if predictions else 0.0
        
        return {"accuracy": accuracy}


class F1ScoreEvaluator(BaseEvaluator):
    async def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        predictions = inputs.get("predictions", [])
        targets = inputs.get("targets", [])
        
        true_positives = sum((p == 1 and t == 1) for p, t in zip(predictions, targets))
        false_positives = sum((p == 1 and t == 0) for p, t in zip(predictions, targets))
        false_negatives = sum((p == 0 and t == 1) for p, t in zip(predictions, targets))
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "f1_score": f1,
            "precision": precision,
            "recall": recall
        }


class EvaluatorRegistry:
    def __init__(self):
        self.evaluators: Dict[str, BaseEvaluator] = {
            "accuracy": AccuracyEvaluator(),
            "f1_score": F1ScoreEvaluator()
        }
    
    def register(self, name: str, evaluator: BaseEvaluator):
        self.evaluators[name] = evaluator
    
    def get(self, name: str) -> BaseEvaluator:
        return self.evaluators.get(name)
    
    async def evaluate_all(
        self,
        inputs: Dict[str, Any],
        metric_names: List[str]
    ) -> Dict[str, Any]:
        results = {}
        
        for metric_name in metric_names:
            evaluator = self.get(metric_name)
            if evaluator:
                result = await evaluator.evaluate(inputs)
                results.update(result)
        
        return results
