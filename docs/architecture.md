# Zenith Architecture

## Overview

Zenith is built on a modern microservices architecture optimized for AI/ML workloads.

## Core Components

### Backend API (FastAPI)
- Async-first design for high performance
- RESTful API with OpenAPI documentation
- JWT-based authentication
- Role-based access control

### Frontend (React 19)
- Server-side rendering support
- Real-time updates via WebSocket
- Responsive design with Tailwind CSS
- Component library with shadcn/ui

### Database Layer
- PostgreSQL for metadata storage
- Redis for caching and online feature store
- S3/MinIO for artifact storage

### Worker Pool (Celery)
- Distributed task execution
- Long-running training jobs
- Scheduled monitoring tasks

### Inference Layer
- Triton Inference Server for model serving
- vLLM for high-throughput LLM inference
- Auto-scaling based on load

### Observability
- OpenTelemetry for distributed tracing
- Prometheus metrics collection
- Grafana dashboards

## Data Flow

1. User creates experiment via UI/SDK
2. Backend stores metadata in PostgreSQL
3. Training job queued in Celery
4. Worker executes training, logs metrics
5. Model artifacts saved to S3
6. Model registered in registry
7. Deployment creates inference endpoint
8. Monitoring tracks performance and drift

## Security

- All endpoints require authentication
- RBAC for fine-grained access control
- Secrets managed via environment variables
- TLS encryption for all connections

## Scalability

- Horizontal scaling of API servers
- Worker pool scales based on queue depth
- Database connection pooling
- CDN for static assets
