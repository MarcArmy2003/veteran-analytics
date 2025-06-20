## 🗓️ Date: 2025-06-20
**Developer:** Gillon Marchetti
**Project:** VISTA – Veteran Insights & Statistics Tool for Analysis
**Session Time:** 01:00 AM EDT
**Environment:** Local Python venv, Cloudflare Tunnel, Google Cloud

---

### ✅ Accomplishments & Key Decisions

- **Objective 1:** Successfully established a fully functional local Flask API backend that reliably loads and serves data from the "Open VA Data APIs" Google Sheet, handling complex headers and data structures.
- **Decision:** Committed to using a local, non-synced directory (C:\\VISTA_TEMP) for script execution to bypass persistent OneDrive interference and environment pathing issues.
- **Code Created/Modified:** `app.py` (Flask API backend), `openapi_spec.yaml` (OpenAPI specification).
- **Objective 2:** Implemented a robust, automated data cleaning and conversion pipeline for RAG system ingestion.
- **Decision:** Adopted a "deep chunking" strategy for `.xls` files, converting all sheets and rows into multiple smaller Markdown (`.txt`) files to circumvent Vertex AI size and format limitations.
- **Code Created/Modified:** `convert_xls_files.py` (automates `.xls` to Markdown conversion and cleans up `Thumbs.db`, `.DS_Store`, and other temporary/unsupported files).
- **Objective 3:** Successfully integrated the local Flask API with the VISTA Custom GPT and established foundational RAG capabilities in Google Cloud.
- **Decision:** Leveraged Cloudflare Tunnel (`cloudflared.exe`) for secure public access to the local API, after `ngrok` was flagged as a security risk.
- **Decision:** Chose Google Cloud Vertex AI Search for scalable RAG implementation, starting with a multi-region app and a data store for unstructured documents.
- **Code Created/Modified:** `openapi_spec.yaml` updated with Cloudflare Tunnel URL.
- **Objective 4:** Established professional project infrastructure.
- **Decision:** Acquired and configured primary project domains (`veterananalytics.com`, `veteranintel.com`, `vistaadvocacy.com`) and a dedicated business email (`MarcArmy2003@veterananalytics.com`) for professional branding and communication.

### ⚠️ Challenges & Roadblocks

- **Issue:** Persistent `FileNotFoundError` and command recognition issues (`'python' not recognized`) in the terminal, even within an activated virtual environment.
- **Solution:** Diagnosed as a conflict with Microsoft OneDrive syncing and the Microsoft Store's Python alias. Bypassed by performing operations from a simple, local directory (`C:\\VISTA_TEMP`) and explicitly calling Python executables with their absolute paths.
- **Issue:** `gspread` library failing to parse Google Sheet headers (duplicate header, unexpected keyword argument `header`).
- **Solution:** Iteratively debugged by re-installing libraries, recreating virtual environments, switching to title-based sheet opening, and eventually implementing manual header parsing within `app.py` based on observed DataFrame column names.
- **Issue:** Flask API endpoints returning `KeyError` when attempting to filter data by column name.
- **Solution:** Added debugging print statements to log actual DataFrame column names at runtime, then updated Flask API query functions (`query_api_paths`, `query_census_apis_full_list`) to use these precise column names.
- **Issue:** `ngrok.exe` download flagged by Windows Defender as a Trojan.
- **Solution:** Pivoted to Cloudflare Tunnel (`cloudflared.exe`) as a more secure alternative for creating a public tunnel to the local Flask API.
- **Issue:** `cloudflared.exe` command not recognized in terminal, even when in the correct directory.
- **Solution:** Identified a mismatch in the executable filename (`cloudflared.exe` vs. `cloudflared-windows-amd64.exe`) and persistent PATH issues. Resolved by specifying the exact full filename and absolute path during execution.
- **Issue:** Vertex AI Search RAG data ingestion failing due to unsupported file types (`.db`, `.xls`, `.DS_Store`).
- **Solution:** Developed the `convert_xls_files.py` script to automatically identify, convert (`.xls` to Markdown `.txt`), and delete these unsupported files from the local repository before syncing to Cloud Storage.

### 🚀 Next Steps

- **Immediate Goal:** Re-run the `convert_xls_files.py` script from `C:\\VISTA_TEMP` to ensure all `.xls` data has been properly chunked and converted into `.txt` Markdown files, and that all unsupported file types are removed from the local repository.
- **Immediate Goal:** Upload the cleaned and converted `.txt` files from the local repository to the Google Cloud Storage bucket (`gs://vista-api-backend-rag-files`) using `gcloud storage cp --recursive`.
- **Immediate Goal:** Trigger a MANUAL SYNC in the Vertex AI Search console for the `conversation-transcript-store` data store to ingest all newly uploaded documents.
- **Immediate Goal:** Test the RAG system extensively with queries targeting both the conversation transcript and the newly indexed Annual Benefits Reports, focusing on fact retrieval, summarization, and comparative analysis.
- **Future Goal:** Diagnose and fix the "header row contains duplicates" error in the Flask API when deployed to Google Cloud Run to ensure a stable, permanent URL for the backend.
- **Future Goal:** Refine the VISTA Custom GPT's instructions to optimize its interaction with the deployed API and RAG system for more intuitive and powerful natural language responses.

## 🗓️ Date: 2025-06-16  
**Developer:** Gillon Marchetti  
**Project:** VISTA – Veteran Insights & Statistics Tool for Analysis  
**Session Time:** 10:27 PM EDT → Close of day  
**Environment:** Local Git CLI, GitHub UI, Windows Command Line

---

### ✅ Accomplishments & Key Decisions

- **Objective 1:** Diagnose and resolve the Vertex AI data ingestion failure where files were exceeding the size limit, even after initial chunking attempts.
- **Objective 2:** Improve the project’s file structure integrity on GitHub, correct repository submodule behavior, and enable proper frontend folder browsing.
- **Decision (Chunking Logic):** The script's size estimation was inaccurate due to the overhead of markdown formatting. The definitive solution was to calculate the actual byte size of the UTF-8 encoded markdown content prior to file write.
- **Decision (File Conversion):** Introduced a pre-processing step to automatically convert `.xls` to `.xlsx` files using `pyexcel` to prevent runtime incompatibilities.
- **Decision (Submodule Resolution):** Resolved a lingering Git submodule state for `src/vista-api-backend/` by manually clearing the Git index, removing metadata, and restoring the backend as a standard directory.
- **Code Created/Modified:**
  - `definitive_chunker_v4.py` – includes byte-precise markdown output sizing and file format conversion.
  - `openapi_spec.yaml` – refined parameter descriptions and examples for enhanced usability.
  - `app.py` – added comprehensive docstrings and inline commentary for maintainability.
- **API Specification:** Updated `openapi_spec.yaml` to clarify query parameters for API path selection and Census dataset queries.
- **CI/CD Planning:** Drafted a `pylint.yml` GitHub Actions workflow to enforce static code quality checks during automated builds.
- **Repository Hygiene:**
  - Removed all submodule traces from `.git/config` and Git index.
  - Re-added the `vista-api-backend/` directory under `src/` as a regular Git-tracked folder.
  - Validated final folder appearance via GitHub UI—resolved submodule icon issue and ensured all backend files are explorable in-browser.

---

### ⚠️ Challenges & Roadblocks

- **Vertex AI File Rejections:**
  - Hundreds of `.txt` files continued exceeding the 2.5MB ingestion limit despite chunking.
  - **Root Cause:** Markdown rendering via `pandas.to_markdown()` introduced unpredictable size inflation. Resolved by calculating the encoded byte size of final content.
- **Python Runtime Failures:**
  - `FileNotFoundError` from misconfigured input folder paths.
  - `Missing optional dependency 'openpyxl'` for Excel I/O – resolved via package installation.
  - `WinError 32` due to improper file handling – resolved by refactoring script to close handles via `with` context manager.
- **Git Submodule Persistence:**
  - Despite prior removal attempts, GitHub displayed `vista-api-backend/` as a submodule (arrow icon, inaccessible folder).
  - Resolved by deleting cached folder references, clearing `.git/config`, and recommitting the directory structure cleanly.

---

### 🚀 Next Steps

- **Immediate Task:** Validate that `definitive_chunker_v4.py` completes successfully and produces sub-2.5MB `.txt` outputs across all datasets.
- **Ingestion Finalization:**
  - Purge previous ingest attempts from GCS (`vista-api-backend-rag-files`)
  - Deploy new data using `gcloud storage rsync`
  - Trigger the ingestion pipeline within Vertex AI for final verification
- **Post-Ingestion Tasks:**
  - Confirm file visibility, completeness, and integrity within Vertex AI's retrieval system
  - Begin formal API endpoint testing
  - Commit finalized GitHub Actions CI/CD workflow (`pylint.yml`) and integrate automated checks into future pushes

⸻

## 🗓️ Date: 2025-06-16  
**Developer:** Gillon Marchetti  
**Project:** VISTA – Veteran Insights & Statistics Tool for Analysis  
**Session Time:** 12:05 AM EDT  
**Environment:** Local Python venv, OneDrive, gcloud CLI, Google Cloud Storage  
**File(s) Modified:** `definitive_chunker.py`  

---

### ✅ Accomplishments & Key Decisions

#### 📌 Objective
- Diagnose the root cause of Vertex AI ingestion failures due to oversized `.txt` chunk files exceeding the 2.5MB limit.

#### 🧠 Key Findings
- The issue was traced to the use of `pandas.to_markdown()`, which inflated file size unpredictably depending on cell contents and formatting.
- Estimations based on row/column counts were insufficient to prevent oversize output.

#### 🛠️ Fix Implemented
- Developed `definitive_chunker.py v2`, which now:
  - Calculates actual byte size (`len(content.encode("utf-8"))`) of each Markdown-rendered chunk
  - Hard-caps chunk file sizes below the ingestion threshold before writing to disk

#### 📝 Documentation / Process Refinement
- Clarified full data handling workflow:
  - Temporary workspace: `C:\VISTA_TEMP` (used to avoid OneDrive sync interference)
  - Upload command: `gcloud storage rsync` for precise deployment to GCS ingestion bucket

#### 🧯 Contingency Plan
- If size-control script fails again, escalate to using a dedicated cloud-native ETL system (e.g., **Google Cloud Dataflow**) for pipeline control and scaling.

---

### ⚠️ Challenges & Roadblocks

#### 🔄 First Attempt Failure
- Lowering `MAX_CHUNK_SIZE` in the original script was insufficient; multiple `.txt` files still exceeded 5MB in actual size.

#### 🧩 Root Cause
- Markdown rendering unpredictably increased file size.
- The script’s estimation logic failed to account for text expansion caused by formatting characters and cell value length.

---

### 🚀 Next Steps

#### 🎯 Immediate Goal
- Run full end-to-end execution of the chunking and conversion process using `definitive_chunker.py v2`.
- Validate that all `.txt` outputs conform to Vertex AI's ingestion requirements (<2.5MB/file).

#### 📡 Near-Term Target
- After successful ingestion, initiate **retrieval augmentation (RAG)** testing within Vertex AI using newly processed data.

---

#### 🧱 Repository Reorganization (Structural Refactor)
- Defined a standardized repository layout where `veteran-analytics` serves as the parent project, and `vista-api-backend` is located under `src/`.
- Created or confirmed presence of high-level folders:
  - `src/`
  - `docs/`
  - `assets/`
  - `legal/`
- Created nested backend structure under `src/vista-api-backend`:
  - `app/`
  - `data/`
  - `scripts/`
  - `specs/`
  - `docs/`
  - `openapi_spec.yaml`, `Dockerfile`, `requirements.txt`

#### 📁 Manual File Moves (CMD)
- Encountered Windows-specific move restrictions (`Access is denied`)
- Used `rmdir /s /q` to remove locked directories before successful relocation
- Successfully moved:
  - `app/` → `src/vista-api-backend/app/`
  - `scripts/` → `src/vista-api-backend/scripts/`
  - `specs/` → `src/vista-api-backend/specs/`
  - `data/` → `src/vista-api-backend/data/`
  - Top-level files (`Dockerfile`, `requirements.txt`, `openapi_spec.yaml`) to backend root

#### 🔧 Git Operations
- Resolved `git push` rejection due to remote divergence
- Performed a clean `git pull`, managed in-terminal merge via Vim/Nano
- Committed and pushed resolved merge: `Moved backend files into src/vista-api-backend`

#### 📁 Markdown & Documentation
- Added `[Gemini Gem Setup Guide](docs/vista_gem_codex.md)` and `[Daily Log Template](docs/daily_log_template.md)` to the main `README.md`
- Created and organized `TRADEMARK.md`, `TERMS.md`, and `LICENSE` under `/legal`
- Updated and committed `README.md` to reflect current architecture and project scope

---

### 🚧 Outstanding Tasks / Follow-Up
- Finish confirming all backend folders were fully migrated and no residual folders remain in root
- Re-test Python app execution after refactor (`flask run` or entrypoint)
- Validate all relative paths in `Dockerfile`, `requirements.txt`, and Python imports
- Update OpenAPI spec paths if affected by move
- Begin front-end or deployment layer planning (Cloud Run or App Engine)

---

### 🔖 Notes
- Editor for Git merge was likely Vim (resolved with `:wq`)
- Repeated Git guidance helped build confidence in repo hygiene
- Markdown links require raw content path (`raw.githubusercontent.com/...`) for Gemini ingestion


## VISTA Project Log: 2025-06-15

**Session Time:** 11:15 AM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Successfully diagnose and solve the persistent `FileNotFoundError` that was preventing the Python data processing script from running.
* **Decision:** The root cause of the execution errors was identified as a likely conflict with the Microsoft OneDrive sync folder. The definitive solution is to move the script and its source data (`XLS_TO_PROCESS` folder) to a simple, local directory (`C:\VISTA_TEMP`) before execution.
* **Code Created/Modified:** Finalized the `definitive_chunker.py` script to read `.xls` files directly, convert all sheets to Markdown, and save the output to a dedicated folder, automating the entire data cleaning pipeline.

### ⚠️ Challenges & Roadblocks

* **Issue:** The Python script `definitive_chunker.py` was consistently failing with a `FileNotFoundError`, even when the file was confirmed to be in the correct directory and executed with an absolute path. This pointed to an issue beyond a simple pathing mistake.
* **Solution:** We bypassed the problem by creating a local, non-synced folder (`C:\VISTA_TEMP`) and running the script from there. This confirmed that the OneDrive folder was the source of the file system conflict, providing a reliable workaround for all future script executions.

### 🚀 Next Steps

* **Immediate Goal:** Run the `definitive_chunker.py` script from the `C:\VISTA_TEMP` directory to process all the source `.xls` files.
* **Future Goal:** After the script successfully converts all files, copy the cleaned `.txt` files from the output folder back into the main `VISTA_Repository`, sync the repository with Google Cloud Storage, and trigger a `MANUAL SYNC` in Vertex AI to complete the data ingestion.

## VISTA Project Log: 2025-06-14

**Session Time:** 11:55 PM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Build a live API backend to replace static data sources for the VISTA Custom GPT.
* **Decision:** We decided to use Python with Flask for the backend, `gspread` to read from Google Sheets, and `pandas` for data manipulation.
* **Code Created/Modified:** Created the initial `sheets_reader.py` to connect to the Google Sheet and a full `app.py` Flask application to serve the data via queryable endpoints.
* **Key Accomplishment:** Successfully connected the VISTA Custom GPT to the local Flask API via a Cloudflare Tunnel and received valid data from test queries, proving the end-to-end circuit works.

### ⚠️ Challenges & Roadblocks

* **Issue:** The initial Python environment setup failed because the `python` command was intercepted by a Microsoft Store alias.
* **Solution:** We bypassed this by using the `py` command and later, by calling the `python.exe` executable with its full, absolute path from within the virtual environment's `Scripts` folder.
* **Issue:** The `gspread` library threw multiple authentication and attribute errors (e.g., `'Client' object has no attribute 'open_by_id'`), and header parsing errors (`the header row in the worksheet contains duplicates: ['']`).
* **Solution:** We resolved this through an iterative process of revising the script to handle authentication more explicitly and then adding logic to manually parse the headers from the specific worksheets that were causing the problem.
* **Issue:** The `ngrok` tunneling service was flagged as a potential trojan by Windows Defender, preventing its use.
* **Solution:** We pivoted to using Cloudflare Tunnel (`cloudflared.exe`) as a more secure and reliable alternative to expose the local API to the internet.

### 🚀 Next Steps

* **Immediate Goal:** Transition from the temporary Cloudflare Tunnel to a permanent, stable URL for the API backend.
* **Future Goal:** Deploy the Flask application to Google Cloud Run to provide a production-ready API endpoint, which will allow for further iteration on the VISTA Custom GPT's instructions and capabilities.

## VISTA Project Log: 2025-06-13

**Session Time:** 11:45 PM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Set up the foundational Google Cloud and local Python environments required to build the VISTA API backend.
* **Decision:** We committed to using a service account with a downloadable JSON key for server-to-server authentication between the Python script and the Google Sheets API. This is a more secure and scalable method than using user-based OAuth.
* **Code Created/Modified:** Wrote the first version of the `sheets_reader.py` script, which established the core logic for connecting to the spreadsheet and attempting to read data from the specified worksheets.

### ⚠️ Challenges & Roadblocks

* **Issue:** The Python executable was not installed or correctly added to the system's PATH, causing the initial `python -m venv venv` command to fail.
* **Solution:** The user installed Python directly, which allowed us to create and activate the virtual environment and proceed with installing the necessary libraries (`gspread`, `pandas`, `Flask`).
* **Issue:** We encountered a persistent `AttributeError: 'Client' object has no attribute 'open_by_id'` when using `gspread`.
* **Solution:** After multiple attempts to fix this by re-authenticating and trying different `gspread` client initialization methods, we pivoted to opening the sheet by its title. This revealed the true underlying problem: a `SpreadsheetNotFound` error, which we correctly diagnosed as the service account not having "Viewer" permissions on the Google Sheet.
* **Issue:** After fixing the permissions, the script failed with a new error: `the header row in the worksheet contains duplicates: ['']`.
* **Solution:** We identified that this was due to merged cells or empty columns in the header row of the "API Name and Path" and "Census Bureau APIs - Full List" worksheets. The decision was made to handle this by adding specific logic to the script to manually parse the headers for those sheets.

### 🚀 Next Steps

* **Immediate Goal:** Refine the `sheets_reader.py` script to successfully load data from all worksheets by correctly handling the problematic headers.
* **Future Goal:** Integrate the now-functional data-loading script into a Flask application to create the first API endpoints.

## VISTA Project Log: 2025-06-12

**Session Time:** 02:30 PM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Define the high-level technical architecture for the VISTA project.
* **Decision:** We established the core strategy of moving from static files to a dynamic, API-driven system. The plan is to build a Python backend using Flask that reads data from a Google Sheet and serves it to the VISTA Custom GPT via a custom API.
* **Decision:** Agreed on a strategy to overcome the 30 `operationId` limit in Custom GPTs by designing generalized, parameterized API actions. The backend API would handle the complex logic of mapping these general calls to specific data sources listed in the Google Sheet.

---

### ⚠️ Challenges & Roadblocks

* **Issue:** How to integrate VISTA with over 100 identified `data.va.gov` resources without violating the 30 `operationId` limit for GPT Actions.
* **Solution:** The chosen solution was to create a few broad API endpoints (e.g., `getDemographicsData`) that accept a `dataset` parameter. This allows the GPT to make a simple call, while the Python backend uses the parameter to look up the correct, specific data source from the master Google Sheet.
* **Issue:** Potential for hitting API rate limits from our data sources.
* **Solution:** We proactively reviewed the specific API quotas for both the Google Sheets API and `data.va.gov` to ensure the architecture would be robust and to plan for future scaling.

---

### 🚀 Next Steps

* **Immediate Goal:** Begin the practical, hands-on development by setting up the necessary Google Cloud Project and service account credentials for the Google Sheets API.
* **Future Goal:** Write the initial Python script to programmatically connect to the Google Sheet and read the data, which would serve as the foundation for the Flask API.

## VISTA Project Log: 2025-06-19

**Session Time:** 12:15 PM EDT

---

### ✅ Accomplishments & Key Decisions

- **Objective 1:** Integrated Excel conversion and chunking into a unified pipeline.
- **Decision:** All Excel files are converted to individual CSVs per worksheet, then chunked into markdown `.txt` files under 2MB. Intermediate CSVs are removed.
- **Code Created/Modified:** `xls_to_csv_and_chunk.py` handles sheet detection, CSV export, chunking, and cleanup.
- **Objective 2:** Established a master source index for veteran research material with a four-tier hierarchy prioritizing open federal sources such as M21-1, Title 38 CFR, VA Forms, VetPop, and BVA decisions.

### ⚠️ Challenges & Roadblocks

- Earlier scripts failed with multi-worksheet files and inconsistent chunk sizes. Rewrote the logic with sheet name sanitization and size checks.
- Consolidating fragmented source data required a centralized retrieval strategy with metadata tagging.

### 🚀 Next Steps

- Run the new script on all historical Excel files in `C:\VISTA_TEMP\data\XLS_TO_PROCESS`.
- Develop an automated pipeline to monitor new Excel files and prepare them for Vertex AI ingestion.
- Begin ingestion and schema mapping of the curated veteran benefits and exposure data.
