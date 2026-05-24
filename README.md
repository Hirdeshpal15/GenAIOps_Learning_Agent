# GenAIOps Learning Agent — Enterprise Azure-Native Architecture

Enterprise Azure-native GenAIOps platform featuring Retrieval-Augmented Generation (RAG), observability, Infrastructure as Code, CI/CD, containerized deployment, and cloud-native AI architecture.

---

# Project Overview

This project demonstrates how modern enterprise AI systems are designed, deployed, monitored, and operated using Azure-native services.

The platform includes:

- Azure OpenAI integration
- Enterprise RAG using Azure AI Search
- FastAPI AI API service
- Docker containerization
- Azure Container Apps deployment
- OpenTelemetry tracing
- Application Insights observability
- Infrastructure as Code using Bicep
- GitHub Actions CI/CD
- Azure Key Vault security
- Managed Identity and RBAC

---

# Architecture

## High-Level System Flow

```text
User / Client
       ↓
Azure Container Apps
       ↓
FastAPI Enterprise API
       ↓
Azure AI Search (RAG Retrieval)
       ↓
Azure OpenAI
       ↓
Grounded AI Response
       ↓
Application Insights + Log Analytics
```

## Supporting Infrastructure

```text
GitHub Actions → CI/CD
Bicep + azd → Infrastructure Deployment
Azure Container Registry → Container Images
Key Vault → Secret Management
Managed Identity → Secure Authentication
```

---

# Azure Services Used

| Service | Purpose |
|---|---|
| Azure OpenAI | LLM inference |
| Azure AI Search | Enterprise retrieval |
| Azure Container Apps | Cloud hosting |
| Azure Container Registry | Docker image storage |
| Application Insights | Monitoring and telemetry |
| Log Analytics | Centralized logging |
| Azure Key Vault | Secret management |
| Managed Identity | Passwordless authentication |
| GitHub Actions | CI/CD pipelines |
| Bicep | Infrastructure as Code |
| Azure Developer CLI (azd) | Environment orchestration |

---

# Enterprise Features Implemented

- Retrieval-Augmented Generation (RAG)
- Cloud-native AI deployment
- Containerized AI APIs
- OpenTelemetry tracing
- AI smoke testing
- Infrastructure as Code
- RBAC-based security
- Managed Identity integration
- Azure observability stack
- GitHub Actions automation
- FastAPI API architecture

---

# Project Structure

```text
my-genaiops-agent/
│
├── api/
├── agents/
├── prompts/
├── traces/
├── evaluations/
├── tools/
├── scripts/
├── infra/
├── .github/workflows/
├── Dockerfile
├── azure.yaml
├── requirements.txt
└── README.md
```

---

# Local Development

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run FastAPI API

```bash
uvicorn api.main:app --reload
```

## Open Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

# Docker Deployment

## Build Container

```bash
docker build -t genaiops-api .
```

## Run Container

```bash
docker run -p 8000:8000 --env-file .env genaiops-api
```

---

# Azure Deployment

## Provision Infrastructure

```bash
azd provision
```

## Deploy Container App

```bash
azd deploy
```

---

# CI/CD

GitHub Actions pipeline automates:

- dependency installation
- infrastructure validation
- smoke testing
- deployment workflows

---

# Observability

The platform integrates:

- OpenTelemetry
- Azure Monitor
- Application Insights
- Log Analytics

This enables:

- tracing
- telemetry
- monitoring
- operational visibility

---

# Security Architecture

Security implementation includes:

- Azure Key Vault
- Managed Identity
- RBAC authorization
- GitHub Secrets
- secret scanning awareness

---

# Key Learning Areas

This project demonstrates practical experience with:

- GenAIOps
- Azure-native AI systems
- enterprise RAG
- cloud observability
- CI/CD pipelines
- Infrastructure as Code
- containerized deployments
- operational AI lifecycle management

---

# Future Improvements

Potential future enhancements:

- Vector search
- Semantic ranking
- Prompt evaluation gates
- FastAPI authentication
- Managed Identity for Key Vault access
- Multi-agent orchestration
- Azure dashboards
- Cost optimization

---

# Repository Description

Azure-native GenAIOps learning platform featuring enterprise RAG, CI/CD, observability, IaC, Azure AI Search, Key Vault, and OpenTelemetry.

---

# Author

Hirdesh Pal
