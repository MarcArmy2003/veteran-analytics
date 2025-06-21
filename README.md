-----

# Veteran Analytics

**Core development repository for Veteran Analytics – AI-powered tools and data advocacy for veterans.**

-----

### 📜 Our Mission

The **VISTA (Veteran Insights & Statistics Tool for Analysis)** project aims to build a suite of tools that help veterans and their families navigate the complexities of accessing benefits. By leveraging AI and modern data processing techniques, we transform opaque government data into an accessible, searchable, and actionable knowledge base.

-----

### ✨ Key Features

  * **Automated Data Processing**: Scripts that automatically clean, chunk, and structure raw government data (Excel, CSV) into formats ready for AI analysis.
  * **AI-Powered Knowledge Base**: Integration with **Google Cloud's Vertex AI** to create a powerful, searchable repository of veteran-related information.
  * **Modular GPT & Data Framework: All backend logic is organized under `src/`, with dedicated modules for ingestion (`data-loaders/`) and GPT prompt handling (`gpt-actions/`). Flask-based APIs and services, if reintroduced, will reside under `app/` for clarity and scalability.
  * **Cloud-Native Architecture**: Designed from the ground up to run on **Google Cloud Platform**, utilizing services like Cloud Run for deployment and Cloud Storage for data management.

-----

### 🏛️ Repository Structure

This repository is a monorepo containing all the code, documentation, and assets for the Veteran Analytics project.

```plaintext
veteran-analytics/
├── .github/                    # GitHub configuration and automation
│   └── workflows/              # GitHub Actions CI/CD workflows
├── app/                        # Core application logic (e.g., UI, API, or service layer)
├── config/                     # Project-level settings and environment configuration
├── src/                        # Source code modules for data processing and GPT tooling
│   ├── data-loaders/           # Ingestion, transformation, and preprocessing routines
│   ├── gpt-actions/            # Prompt routing and GPT interaction logic
├── docs/                       # Technical documentation, internal SOPs, and architecture records
├── data/                       # Structured reference datasets used in development or testing
├── assets/                     # Visual and brand assets used across the project
│   ├── images/                 # Graphics, diagrams, and screenshots
│   ├── logos/                  # Official logos for presentations and docs
├── scripts/                    # Utility scripts for data processing, transformation, and repository maintenance
│   └── Metlakatla              # Compiled timezone data file
├── specs/                      # API specifications, table schemas, and legacy C API interfaces
│   └── Apia/                   # Subfolder for schema-related or experimental specifications
├── legal/                      # Licensing, terms of use, and compliance documentation
├── .gitignore                  # Git exclusion rules for build, system, and binary files
└── README.md                   # This file – project overview and contributor instructions
```

-----

### 💻 Core Technologies

This project uses a modern, scalable technology stack:

  * **Backend**: Python, Flask
  * **Data Processing**: Pandas
  * **Cloud Platform**: Google Cloud Platform (GCP)
  * **AI / RAG System**: Vertex AI Search
  * **Containerization**: Docker
  * **Deployment**: Cloud Run, Gunicorn

-----

### 🚀 Getting Started

The primary component of this project is the **VISTA API Backend**. For detailed instructions on how to set up the development environment, run the data processing scripts, and launch the API, please see the dedicated README file:


➡️ **[VISTA API Backend README](src/vista-api-backend/README.md)**

### 🧪 Running Tests

Install the required packages using `requirements.txt` and run the automated
tests with [pytest](https://docs.pytest.org/):

```bash
pip install -r requirements.txt pytest
pytest
```

### Configuration



```yaml
paths:
  ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR: /path/to/ChatGPT Instructions
  ONEDRIVE_VISTA_API_BACKEND_DIR: /path/to/ChatGPT Instructions/VISTA API Backend
  NEW_VISTA_PROJECT_ROOT: /path/to/VISTA_Project
  MARKDOWN_OUTPUT_FOLDER: /path/to/ABR Excel Table Markdowns
```

You can also set these variables directly in your shell before running any
script, for example:

```bash
export NEW_VISTA_PROJECT_ROOT=/projects/vista
```

If no values are provided, the scripts fall back to their original Windows
paths.
The API's public URL is exposed through a Cloudflare Tunnel. This URL changes
whenever you start a new tunnel. Set the `API_BASE_URL` environment variable (or
edit `.env`) to your current Cloudflare URL and update `openapi_spec.yaml`
accordingly whenever a new tunnel is created.


-----

### 📖 Documentation

For a deeper dive into the project's architecture, goals, and technical implementation, please refer to our documentation.

  * **[Project Overview](docs/project-overview.md)**: A high-level summary of the project.
  * **[VISTA Codex (Knowledge Base)](docs/vista_gem_codex.md)**: The technical specifications and project memory for the VISTA system.

---
### 📘 DAILY LOG – VISTA DEVELOPMENT

➡️ [Click here for the full daily development log](docs/daily_log.md)

Includes detailed progress tracking, session notes, environment changes, file migrations, and system debugging activities.

-----

### ⚖️ Legal

  * **[Terms of Use](legal/TERMS.md)**
  * **[Trademark Policy](legal/TRADEMARK.md)**
