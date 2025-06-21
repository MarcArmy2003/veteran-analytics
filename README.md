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
  * **Scalable API Backend**: A **Flask**-based API (see `src/vista-api-backend`) to serve the processed data, enabling the creation of web applications and other tools.
  * **Cloud-Native Architecture**: Designed from the ground up to run on **Google Cloud Platform**, utilizing services like Cloud Run for deployment and Cloud Storage for data management.

-----

### 🏛️ Repository Structure

This repository is a monorepo containing all the code, documentation, and assets for the Veteran Analytics project.

```plaintext
veteran-analytics/
├── src/                  # All source code, including the API and data loaders
│   ├── vista-api-backend/  # The core Flask API and processing engine
│   └── ...
├── docs/                 # Detailed documentation, architectural decisions, and guides
├── assets/               # Shared assets like logos and style guides
├── legal/                # Terms of use and trademark information
├── .gitignore            # Git ignore rules for the entire project
└── README.md             # This file
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


➡️ **[VISTA API Backend README](https://www.google.com/search?q=src/vista-api-backend/README.md)**

### 🧪 Running Tests

Install the required packages using `requirements.txt` and run the automated
tests with [pytest](https://docs.pytest.org/):

```bash
pip install -r requirements.txt pytest
pytest
```

### Configuration

Several helper scripts rely on file system paths. These paths can be set using
environment variables or a `config.yml` file in the project root. Each script
looks for environment variables first and falls back to the YAML configuration.
An example configuration file looks like:

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

-----

### 📖 Documentation

For a deeper dive into the project's architecture, goals, and technical implementation, please refer to our documentation.

  * **[Project Overview](https://www.google.com/search?q=docs/project-overview.md)**: A high-level summary of the project.
  * **[VISTA Codex (Knowledge Base)](https://www.google.com/search?q=docs/vista_gem_codex.md)**: The technical specifications and project memory for the VISTA system.

---
### 📘 DAILY LOG – VISTA DEVELOPMENT

➡️ [Click here for the full daily development log](https://github.com/MarcArmy2003/veteran-analytics/blob/main/docs/daily_log.md)

Includes detailed progress tracking, session notes, environment changes, file migrations, and system debugging activities.

-----

### ⚖️ Legal

  * **[Terms of Use](https://www.google.com/search?q=legal/TERMS.md)**
  * **[Trademark Policy](https://www.google.com/search?q=legal/TRADEMARK.md)**
