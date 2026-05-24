# GenAIOps Learning Agent — Enterprise Azure-Native Architecture

## Overview

This project is a hands-on enterprise-style GenAIOps learning platform built on Azure.

The system demonstrates:

- Azure OpenAI integration
- Enterprise Retrieval-Augmented Generation (RAG)
- Infrastructure as Code (IaC)
- CI/CD automation
- Observability and telemetry
- OpenTelemetry tracing
- Azure Key Vault security
- Managed Identity architecture
- Azure-native monitoring and retrieval workflows

The goal of this project is not only to build an AI chatbot, but to understand the full operational lifecycle of enterprise AI systems.

---

# Project Architecture

## High-Level Flow

```text
User Question
      ↓
Azure AI Search
      ↓
Indexed Enterprise Knowledge
      ↓
Retrieved Context
      ↓
Azure OpenAI
      ↓
Grounded AI Response
      ↓
Application Insights Telemetry
```

---

# Azure Services Used

| Azure Service             | Purpose                      |
| ------------------------- | ---------------------------- |
| Azure OpenAI              | AI model hosting             |
| Azure AI Search           | Enterprise retrieval system  |
| Azure Key Vault           | Secure secret storage        |
| Application Insights      | Monitoring and observability |
| Log Analytics Workspace   | Telemetry storage            |
| Managed Identity          | Passwordless authentication  |
| Azure Developer CLI (azd) | Environment orchestration    |
| Bicep                     | Infrastructure as Code       |
| GitHub Actions            | CI/CD automation             |

---

# Project Folder Structure

```text
my-genaiops-agent/
│
├── agents/
│   ├── assistant_v1.py
│   ├── assistant_v4.py
│   └── assistant_v9.py
│
├── prompts/
│   ├── system_prompt_v1.txt
│   ├── system_prompt_v2.txt
│   └── system_prompt_v3.txt
│
├── evaluations/
│   ├── smoke_test.py
│   └── evaluation scripts
│
├── traces/
│   ├── trace_demo.py
│   └── azure_trace_demo.py
│
├── tools/
│   ├── memory.py
│   ├── logger.py
│   ├── keyvault_demo.py
│   └── azure_search_retriever.py
│
├── scripts/
│   ├── prompt_loader.py
│   ├── create_search_index.py
│   ├── upload_documents.py
│   └── query_search.py
│
├── infra/
│   └── main.bicep
│
├── .github/
│   └── workflows/
│       └── infra-validation.yml
│
├── azure.yaml
├── requirements.txt
└── .env
```

---

# Infrastructure as Code (IaC)

Infrastructure is provisioned using:

- Bicep
- Azure Developer CLI (azd)

## Provisioned Resources

The Bicep template provisions:

- Azure OpenAI
- Azure AI Search
- Application Insights
- Key Vault
- Managed Identity

## Deployment Workflow

```bash
azd env new dev
azd provision
```

This enables reproducible and automated infrastructure deployment.

---

# Azure OpenAI Integration

The application uses Azure OpenAI through:

- AzureOpenAI SDK
- GPT deployment endpoints
- Environment-based configuration

## Example Environment Variables

```env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
```

---

# Prompt Management

Prompts are versioned inside the `prompts/` folder.

Benefits:

- prompt iteration
- testing different system instructions
- evaluation comparisons
- prompt lifecycle management

## Example Prompt Loader

```python
load_prompt("v3")
```

---

# Enterprise RAG Architecture

The project implements enterprise Retrieval-Augmented Generation (RAG) using Azure AI Search.

## RAG Flow

```text
User Question
      ↓
Azure AI Search Query
      ↓
Retrieve Relevant Documents
      ↓
Inject Context Into Prompt
      ↓
Azure OpenAI Response
```

## Azure AI Search Features Used

- Search indexes
- Searchable fields
- Document uploads
- Retrieval queries

---

# Observability and Monitoring

The system integrates:

- OpenTelemetry
- Azure Monitor
- Application Insights

## Monitoring Flow

```text
Application
    ↓
OpenTelemetry
    ↓
Azure Monitor SDK
    ↓
Application Insights
    ↓
Log Analytics Workspace
```

## Benefits

- centralized telemetry
- tracing
- latency analysis
- operational visibility
- cloud observability

---

# OpenTelemetry Tracing

Distributed tracing is implemented using:

```python
from opentelemetry import trace
```

Spans are generated for:

- prompt loading
- model requests
- evaluations
- workflows

Telemetry is exported to Azure Application Insights.

---

# Security Architecture

## Security Evolution

```text
.env
   ↓
GitHub Secrets
   ↓
Azure Key Vault
   ↓
Managed Identity
   ↓
RBAC Authorization
```

## Azure Key Vault

Secrets are securely stored in:

- Azure Key Vault

Examples:

- API keys
- connection strings
- credentials

---

# Managed Identity

The project provisions a:

- User Assigned Managed Identity

Purpose:

- passwordless authentication
- RBAC-based authorization
- secure Azure service access

## Enterprise Identity Flow

```text
Azure Application
       ↓
Managed Identity
       ↓
Azure RBAC
       ↓
Key Vault Access
```

---

# RBAC (Role-Based Access Control)

RBAC is used for:

- Key Vault authorization
- identity-based permissions
- least-privilege security

Roles used:

- Key Vault Secrets Officer
- Key Vault Secrets User

---

# CI/CD Pipeline

GitHub Actions pipeline automates:

- infrastructure validation
- dependency installation
- AI smoke testing

## Pipeline Flow

```text
Git Push
    ↓
GitHub Actions
    ↓
Infrastructure Validation
    ↓
AI Smoke Tests
    ↓
Deployment Readiness
```

---

# AI Smoke Testing

The project includes automated AI validation.

Purpose:

- verify AI connectivity
- validate deployment health
- detect runtime failures

Example:

```python
response = client.chat.completions.create(...)
```

---

# Environment Management

The project uses Azure Developer CLI environments.

## Example

```bash
azd env new dev
```

Environment configuration enables:

- dev/test/prod separation
- deployment targeting
- configuration management

---

# Key Engineering Concepts Learned

## GenAIOps

- AI operational lifecycle
- prompt management
- evaluations
- observability
- deployment automation

## DevOps

- Infrastructure as Code
- CI/CD pipelines
- environment orchestration
- automation workflows

## Azure Architecture

- Azure-native services
- cloud observability
- identity-based security
- enterprise retrieval systems

---

# Common Debugging Scenarios Encountered

During development the following operational issues were solved:

- Azure endpoint misconfiguration
- deleted Azure resources
- CI/CD secret mismatches
- GitHub Actions environment issues
- RBAC propagation delays
- Key Vault authorization problems
- Azure Portal caching issues
- Azure AI Search indexing delays

These debugging exercises helped develop real operational engineering understanding.

---

# Future Improvements

Possible next-level enhancements:

- FastAPI deployment
- Azure Container Apps
- vector search
- semantic ranking
- hybrid search
- evaluation gates
- prompt regression testing
- Azure dashboards
- cost monitoring
- multi-agent orchestration

---

# Final Learning Outcome

This project demonstrates practical understanding of:

- Azure-native GenAIOps
- enterprise AI architecture
- operational AI systems
- observability
- security
- retrieval systems
- CI/CD automation
- Infrastructure as Code

The project evolved from a simple AI assistant into a cloud-native enterprise GenAIOps learning platform.

---

# Recommended Commands Reference

## Infrastructure

```bash
azd provision
```

## Run Enterprise Agent

```bash
python -m agents.assistant_v9
```

## Run Azure Trace Demo

```bash
python traces/azure_trace_demo.py
```

## Create Search Index

```bash
python scripts/create_search_index.py
```

## Upload Documents

```bash
python scripts/upload_documents.py
```

## Query Azure Search

```bash
python scripts/query_search.py
```

---

# Conclusion

This project provides a strong foundation in:

- Azure-native AI engineering
- enterprise GenAIOps
- cloud observability
- secure Azure architecture
- enterprise retrieval systems
- operational AI lifecycle management

The learning approach focused on:

- building manually
- debugging real issues
- understanding architecture deeply
- connecting enterprise concepts together

This creates much stronger engineering understanding than only following tutorials.
