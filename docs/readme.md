-----

# Veteran Analytics

**Core development repository for Veteran Analytics – AI-powered tools and data advocacy for veterans.**

-----

### 📜 Our Mission

The **VISTA (Veteran-Informed Systems & Technology Access)** project aims to build a suite of tools that help veterans and their families navigate the complexities of accessing benefits. By leveraging AI and modern data processing techniques, we transform opaque government data into an accessible, searchable, and actionable knowledge base.

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

➡️ **[VISTA API Backend README](../src/vista-api-backend/README.md)**

-----

### 📖 Documentation

For a deeper dive into the project's architecture, goals, and technical implementation, please refer to our documentation.

  * **[Project Overview](project-overview.md)**: A high-level summary of the project.
  * **[VISTA Codex (Knowledge Base)](vista_gem_codex.md)**: The technical specifications and project memory for the VISTA system.

-----

### ⚖️ Legal

  * **[Terms of Use](../legal/TERMS.md)**
  * **[Trademark Policy](../legal/TRADEMARK.md)**
