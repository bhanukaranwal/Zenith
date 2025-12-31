from typing import Dict, Any, Optional
import torch
from torch import nn
from torch.utils.data import DataLoader
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.telemetry import get_tracer

tracer = get_tracer(__name__)


class TrainingService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.checkpoint_path = Path("/app/artifacts/checkpoints")
        self.checkpoint_path.mkdir(parents=True, exist_ok=True)
    
    async def train_model(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: Dict[str, Any],
        run_id: int
    ):
        with tracer.start_as_current_span("train_model") as span:
            span.set_attribute("run_id", run_id)
            
            optimizer = torch.optim.AdamW(
                model.parameters(),
                lr=config.get("learning_rate", 0.001)
            )
            criterion = nn.CrossEntropyLoss()
            
            num_epochs = config.get("num_epochs", 10)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            
            for epoch in range(num_epochs):
                model.train()
                train_loss = 0.0
                
                for batch_idx, (inputs, targets) in enumerate(train_loader):
                    inputs, targets = inputs.to(device), targets.to(device)
                    
                    optimizer.zero_grad()
                    outputs = model(inputs)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()
                    
                    train_loss += loss.item()
                
                val_loss = await self._validate(model, val_loader, criterion, device)
                
                checkpoint = {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "train_loss": train_loss / len(train_loader),
                    "val_loss": val_loss
                }
                
                checkpoint_file = self.checkpoint_path / f"run_{run_id}_epoch_{epoch}.pt"
                torch.save(checkpoint, checkpoint_file)
            
            return str(checkpoint_file)
    
    async def _validate(
        self,
        model: nn.Module,
        val_loader: DataLoader,
        criterion: nn.Module,
        device: torch.device
    ) -> float:
        model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                val_loss += loss.item()
        
        return val_loss / len(val_loader)


class DistributedTrainingService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def setup_distributed(
        self,
        rank: int,
        world_size: int,
        backend: str = "nccl"
    ):
        import torch.distributed as dist
        dist.init_process_group(
            backend=backend,
            init_method="env://",
            world_size=world_size,
            rank=rank
        )
    
    async def train_distributed(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        config: Dict[str, Any]
    ):
        from torch.nn.parallel import DistributedDataParallel as DDP
        
        device_id = torch.cuda.current_device()
        model = model.to(device_id)
        ddp_model = DDP(model, device_ids=[device_id])
        
        optimizer = torch.optim.AdamW(
            ddp_model.parameters(),
            lr=config.get("learning_rate", 0.001)
        )
        
        for epoch in range(config.get("num_epochs", 10)):
            for batch_idx, (inputs, targets) in enumerate(train_loader):
                inputs = inputs.to(device_id)
                targets = targets.to(device_id)
                
                optimizer.zero_grad()
                outputs = ddp_model(inputs)
                loss = nn.functional.cross_entropy(outputs, targets)
                loss.backward()
                optimizer.step()


class HyperparameterTuningService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def optimize_hyperparameters(
        self,
        objective_function,
        param_space: Dict[str, Any],
        n_trials: int = 100
    ):
        import optuna
        
        study = optuna.create_study(direction="minimize")
        study.optimize(objective_function, n_trials=n_trials)
        
        return {
            "best_params": study.best_params,
            "best_value": study.best_value,
            "trials": len(study.trials)
        }
