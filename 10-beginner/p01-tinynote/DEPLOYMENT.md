# 🚀 TinyNote Deployment Guide

## Quick Start (Local Testing)

### 1. Clone & Setup
```bash
git clone https://github.com/priyanshurai5432-droid/cloud-lab-priyanshu.git
cd cloud-lab-priyanshu/10-beginner/p01-tinynote

python -m venv .venv
.\venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # macOS/Linux

pip install -r requirements.txt
```

### 2. Test Locally
```bash
func start
```
Server runs on http://localhost:7071

## Deploy to Azure

### Prerequisites
- Azure CLI: `az --version`
- Azure Functions Core: `func --version`
- Bicep CLI: `az bicep version`

### 1. Login
```bash
az login
```

### 2. Deploy Infrastructure
```bash
cd infra
az deployment sub create \
  --template-file main.bicep \
  --location centralindia
```

### 3. Deploy Function App
```bash
func azure functionapp publish <FUNCTION-APP-NAME>
```

### 4. Test Live API
```bash
# Create note
curl -X POST https://<FUNCTION-APP>.azurewebsites.net/api/notes \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello Cloud"}'

# Get note
curl https://<FUNCTION-APP>.azurewebsites.net/api/notes/<NOTE-ID>
```

## Architecture
- **Compute:** Azure Functions (Python 3.11, Consumption Plan)
- **Storage:** Azure Blob Storage (Standard LRS)
- **IaC:** Bicep
- **API:** RESTful JSON endpoints
