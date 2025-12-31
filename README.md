# 🚀 Zenith - The Zenith of Machine Learning Platforms

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg)](https://kubernetes.io/)

**The ultimate open-source AI-first MLOps platform for 2026** — combining enterprise-grade ML lifecycle management with cutting-edge LLM, RAG, and agent capabilities. Built to surpass Vertex AI, SageMaker, Azure ML, Databricks, MLflow, W&B, and more.

## 🎯 Architecture Overview

┌─────────────────────────────────────────────────────────────────┐
│ React 19 Frontend UI │
│ Experiments │ Models │ Deployments │ Monitoring │ Agents │
└────────────────────────┬────────────────────────────────────────┘
│ REST API / WebSocket
┌────────────────────────▼────────────────────────────────────────┐
│ FastAPI Backend (Async) │
│ Auth │ Projects │ Datasets │ Features │ Training │ Deploy │
└─┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┘
│ │ │ │ │ │ │ │ │
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼
┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│PG ││Redis││S3/ ││Triton││vLLM││Celery││Jupyter││OTel││Vector││Feature│
│SQL ││Cache││Blob││Serve││GPU ││Worker││Lab ││Export││DB ││Store │
└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘


## ✨ Feature Comparison

| Feature | Zenith | Vertex AI | SageMaker | Azure ML | Databricks | MLflow | W&B |
|---------|--------|-----------|-----------|----------|------------|--------|-----|
| **Open Source** | ✅ | ❌ | ❌ | ❌ | Partial | ✅ | ❌ |
| **LLM-Native** | ✅ | ✅ | ✅ | ✅ | ✅ | Partial | ✅ |
| **Agent Orchestration** | ✅ | Partial | ❌ | Partial | ✅ | ❌ | ❌ |
| **Prompt Playground** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **RAG Pipeline Builder** | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **OpenTelemetry Native** | ✅ | Partial | Partial | Partial | ❌ | ✅ | ❌ |
| **Feature Store (Online)** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Real-time Drift Detection** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | Partial |
| **LLM-as-Judge Eval** | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **LoRA/QLoRA Fine-tuning** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **Collaborative UI** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Self-Hosted** | ✅ | ❌ | ❌ | ❌ | Partial | ✅ | ❌ |
| **Cost** | **Free** | $$$ | $$$ | $$$ | $$$ | Free | $$ |

## 🎁 Core Capabilities

### ML/LLM Lifecycle Management
- **Data Versioning**: Immutable dataset snapshots with lineage tracking
- **Feature Store**: Online (Redis) + Offline (Parquet/Delta) with point-in-time joins
- **Experiment Tracking**: Parameters, metrics, artifacts, prompts, traces with real-time visualization
- **Model Registry**: Staging/production promotion with approval workflows and A/B testing
- **Distributed Training**: PyTorch FSDP/DDP, Hugging Face Accelerate, multi-GPU support
- **Hyperparameter Optimization**: Optuna Bayesian optimization + prompt search
- **Deployment**: Batch/real-time/streaming with autoscaling and canary releases
- **Monitoring**: Drift detection (Evidently), performance metrics, cost tracking
- **Explainability**: SHAP values, attention visualization, feature importance
- **Governance**: Bias detection, PII scanning, audit logs, RBAC

### LLM & Agent Features
- **Prompt Playground**: Interactive testing with multiple models, temperature control, few-shot examples
- **RAG Pipeline Builder**: Visual editor for embedding, retrieval, reranking, generation
- **Agent Orchestration**: LangGraph/CrewAI-style workflows with tool integration
- **Chain Tracing**: OpenTelemetry-based distributed traces for complex LLM chains
- **LLM-as-Judge**: Automated evaluation using GPT-4, Claude for quality scoring
- **Fine-tuning**: LoRA, QLoRA with monitoring and automatic checkpoint management
- **Vector Search**: Integrated embedding storage and semantic search
- **Hallucination Detection**: Confidence scoring and fact verification

### Developer Experience
- **Modern UI**: React 19 + Tailwind + shadcn/ui with dark mode
- **Real-time Collaboration**: Live experiment updates, shared notebooks
- **Jupyter Integration**: Embedded JupyterLab with SDK pre-installed
- **REST + Python SDK**: Comprehensive APIs for all operations
- **OpenTelemetry Export**: Send traces to Datadog, Grafana, Jaeger
- **Plugin System**: Custom evaluators, metrics, retrievers, agents
- **One-command Deploy**: Docker Compose or Kubernetes Helm

## 🚀 Quick Start

### Prerequisites
- Docker 24+ & Docker Compose 2.20+
- 16GB RAM minimum (32GB recommended)
- NVIDIA GPU (optional, for LLM inference)

### Installation

git clone https://github.com/yourusername/zenith-ml.git
cd zenith-ml

cp .env.example .env

docker-compose up -d

docker-compose logs -f backend

### Access Points
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8888 (token: zenith)
- **Triton Inference**: http://localhost:8001

### First Steps

from zenith import ZenithClient

client = ZenithClient("http://localhost:8000")

project = client.create_project(
name="my-first-project",
description="Testing Zenith capabilities"
)

experiment = client.start_experiment(
project_id=project.id,
name="baseline-model"
)

client.log_params({"learning_rate": 0.001, "batch_size": 32})
client.log_metrics({"accuracy": 0.95, "loss": 0.12})

client.log_model(model, name="my-model", framework="pytorch")

## 📊 Feature Deep Dive

### Experiment Tracking
- MLflow-compatible API with superior UI
- Real-time metric streaming with WebSocket
- Side-by-side run comparison with diff views
- Nested runs for hyperparameter sweeps
- Artifact versioning with S3/MinIO backend
- Git integration for code versioning

### Feature Store
- Online serving with Redis (<10ms latency)
- Offline storage with Parquet/Delta Lake
- Point-in-time correct joins for time-series
- Feature transformation pipelines
- Schema evolution and validation
- Feature lineage and impact analysis

### Model Deployment
- Triton Inference Server integration
- vLLM for high-throughput LLM serving
- FastAPI endpoints with automatic OpenAPI
- A/B testing and canary deployments
- Autoscaling based on latency/throughput
- Multi-model serving with routing

### Monitoring & Observability
- Data drift detection (Evidently AI)
- Model performance degradation alerts
- LLM-specific metrics (hallucination rate, toxicity)
- OpenTelemetry traces for debugging
- Cost tracking per model/endpoint
- Real-time dashboards with Recharts

### Agent & RAG Workflows
- Visual workflow builder for agent orchestration
- Pre-built RAG templates (Q&A, summarization, etc.)
- Multi-hop reasoning with chain-of-thought
- Tool calling with automatic schema generation
- Human-in-the-loop approvals
- Workflow versioning and rollback

## 🏗️ Project Structure

zenith-ml/
├── backend/ # FastAPI application
├── frontend/ # React 19 UI
├── jupyter/ # JupyterLab configuration
├── inference/ # Triton models
├── kubernetes/ # Helm charts
├── scripts/ # Utility scripts
├── examples/ # End-to-end tutorials
├── tests/ # Test suite
└── docs/ # Documentation

## 🛠️ Technology Stack

**Backend**: FastAPI, SQLAlchemy 2, asyncpg, Redis, Celery
**Frontend**: React 19, Vite, TypeScript, Tailwind CSS, shadcn/ui, Zustand, TanStack Query
**ML**: PyTorch, Transformers, Accelerate, PEFT, Optuna, Evidently
**Inference**: Triton, vLLM, llama.cpp
**Observability**: OpenTelemetry, Prometheus, Grafana
**Storage**: PostgreSQL, Redis, S3/MinIO
**Orchestration**: Kubernetes, Celery, RQ

## 📚 Examples

- **Tabular ML**: XGBoost with feature store and drift monitoring
- **Computer Vision**: ResNet fine-tuning with distributed training
- **LLM Fine-tuning**: LoRA on Llama 3 for domain adaptation
- **RAG Agent**: Question-answering with retrieval and reranking
- **Multi-modal**: CLIP for image-text matching with monitoring

## 🤝 Contributing

We welcome contributions! See CONTRIBUTING.md for guidelines.

## 📄 License

Apache License 2.0 - see LICENSE file

## 🌟 Star History

⭐ Star us on GitHub to support the project!

## 📧 Support

- Documentation: https://zenith-ml.readthedocs.io
- Discord: https://discord.gg/zenith-ml
- Issues: https://github.com/yourusername/zenith-ml/issues

---

**Built with ❤️ for the ML/AI community**
