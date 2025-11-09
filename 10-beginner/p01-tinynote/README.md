# 🧠 TinyNote — Serverless Notes API

**Tier:** Beginner • **Stack:** Azure Functions (Python) • **Services:** Azure Blob Storage  
**Status:** ✅ Completed • **Goal:** Demonstrate end-to-end understanding of serverless fundamentals on Azure

## 📌 Overview

TinyNote is a minimal cloud-native REST API built entirely with Azure Functions and Azure Blob Storage. It lets users create and retrieve short text notes through simple HTTP calls — no databases, no heavy backend, purely serverless.

The project focuses on understanding the building blocks of cloud engineering:
- How to expose a Function as an HTTP endpoint
- How to handle request/response lifecycles
- How to use environment variables for configuration
- How to persist data in a cloud service securely (Blob Storage)

## 🎯 What It Does

| Endpoint | Method | Description | Example |
|----------|--------|-------------|----------|
| `/api/notes` | POST | Accepts `{ "text": "..." }` and saves it as a JSON file in Azure Blob Storage. Returns a unique ID. | `POST → { "id": "5d2f..." }` |
| `/api/notes/{id}` | GET | Fetches the note with that ID and returns its contents. | `GET → { "id": "5d2f...", "text": "buy milk" }` |

Each note is stored as an individual JSON blob inside the container `notes/` (e.g. `notes/5d2f.json`).  
The app runs on a serverless consumption plan, scaling automatically when requests increase.

## 🏗️ Architecture

```
Client / Postman
      ↓ HTTP POST/GET
  Azure Function App (Python)
      ↓ SDK calls
  Azure Blob Storage
      ↓ Stores
  notes/<id>.json
```

**Components:**
- **Azure Function App:** Hosts the Python HTTP functions (`create_note`, `get_note`)
- **Azure Blob Storage:** Acts as the data layer; each note = one blob
- **App Settings:** Connection strings stored securely (`NOTES_STORAGE_CONNECTION`, `NOTES_CONTAINER`)

## ⚙️ Running Locally

```powershell
# 1. Clone the repo and open project
git clone https://github.com/priyanshurai5432-droid/cloud-lab-priyanshu.git
cd cloud-lab-priyanshu/10-beginner/p01-tinynote

# 2. Set up environment
python -m venv .venv
.\venv\Scripts\Activate.ps1  # on Windows
# or: source .venv/bin/activate  # on macOS/Linux

pip install -r requirements.txt

# 3. Configure local settings
# Edit local.settings.json, add your Azure Storage connection string
func start

# 4. Test
Invoke-RestMethod "http://localhost:7071/api/notes?text=Hello"
```

## 🚀 Deploying to Azure (CLI)

```bash
az login
az group create -n rg-tinynote -l centralindia
az storage account create -n sttinynote123 -g rg-tinynote -l centralindia --sku Standard_LRS
az functionapp plan create -g rg-tinynote -n plan-tinynote --location centralindia --sku Y1 --is-linux
az functionapp create -g rg-tinynote -p plan-tinynote -n func-tinynote-123 \
  --runtime python --runtime-version 3.11 --functions-version 4 \
  --storage-account sttinynote123 --os-type Linux

func azure functionapp publish func-tinynote-123
```

After deployment, live endpoints:
- `POST https://func-tinynote-123.azurewebsites.net/api/notes`
- `GET  https://func-tinynote-123.azurewebsites.net/api/notes/{id}`

## 🧩 Folder Structure

```
p01-tinynote/
├─ app/
│  ├─ function_app.py        # Defines HTTP endpoints
│  ├─ notes_service.py       # Handles blob read/write logic
│  └─ __init__.py
├─ infra/
│  └─ main.bicep             # IaC for Function App + Storage
├─ tests/
│  └─ test_notes.py          # Simple pytest for create/get
├─ requirements.txt
├─ local.settings.json       # Environment variables (ignored in Git)
├─ .env.sample
└─ README.md                 # This file
```

## ✅ What This Project Proves

✓ Understanding of Azure Functions (Python) — triggers, bindings, routes  
✓ Ability to connect application logic to Azure services using SDKs  
✓ Correct use of environment configuration and deployment pipelines  
✓ Familiarity with HTTP APIs, JSON handling, status codes, and response design  
✓ Comfort with CLI provisioning and local debugging  

## 🧭 Repository Structure

This project lives in: `cloud-lab-priyanshu/10-beginner/p01-tinynote`

**At a glance:**
- ✅ Professional README with clear sections
- 🗂️ Simple, modular folder structure (app, infra, tests)
- ⚙️ `requirements.txt` and `local.settings.json` for quick setup
- 🧪 Test file included (pytest)
- 🚀 Ready for CI/CD integration

**GitHub Profile:**
- ✅ Repository pinned to profile
- 🎯 Clear status and learning objectives
- 🔗 Suitable for recruiter/senior engineer review
