# VISTA API Backend

The **VISTA API Backend** is the core processing engine of the [Veteran Analytics](https://github.com/MarcArmy2003/veteran-analytics) project. It transforms structured Excel and CSV data into clean, chunked `.txt` files for AI analysis, and provides a future-ready framework for exposing RESTful APIs to support Veteran health data advocacy.

## 🎯 Purpose

This backend is designed for:

- Converting government Excel datasets into usable machine-readable formats
- Preparing AI-ready inputs for ingestion by Vertex AI and similar platforms
- Structuring outputs for synchronization to cloud storage (e.g., Google Cloud)

## 🧠 Features

- Modular Python scripts for cleaning, chunking, and formatting
- Docker-compatible for container deployment
- OpenAPI YAML spec included for future API endpoints
- Supports staged syncing to external tools and cloud infrastructure

## 📁 Folder Structure

```
vista-api-backend/
├── app/              # Python modules for conversion, chunking, parsing
├── data/             # Input Excel + transcript folders
├── specs/            # OpenAPI specs, GPT action configs
├── scripts/          # Utilities (e.g., unzip, restructure)
├── docs/             # Usage notes, external API references
├── Dockerfile
├── config.yml
├── openapi_spec.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## 🛠 Setup Instructions

### 1. Clone this repo (if separate)

```
git clone https://github.com/MarcArmy2003/veteran-analytics.git
cd veteran-analytics/vista-api-backend
```

### 2. Create a virtual environment

```
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

## 🔄 How It Works

1. Place Excel source files into the input folder:

```
data/XLS_TO_PROCESS/
```

2. Run the definitive chunking script to clean and convert the files:

```
python app/definitive_chunker.py
```

3. Processed `.txt` files are exported to a staging directory outside this repository:

```
C:\VISTA_Repository\ABR Excel Table Markdowns
```

4. Final output is synchronized with Google Cloud Storage (GCS) for use in downstream systems such as Vertex AI.

## 🔐 Note on Credentials

Google Cloud service account keys (`*.json`) are excluded from version control.

To use these credentials:

- Store them securely, e.g.:

```
C:\VISTA_Credentials\
```

- Reference them in your scripts using environment variables:

```python
import os
from google.oauth2 import service_account

key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
creds = service_account.Credentials.from_service_account_file(key_path)
```

## 📄 License

This repository is part of a prototype developed under the Veteran Analytics project.

While it supports public-interest use cases, it is privately developed and not yet licensed for distribution.  
Licensing terms will be finalized prior to any public release or commercial deployment.
