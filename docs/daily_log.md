## 🗓️ Date: 2025-06-16  
**Developer:** Gillon Marchetti  
**Project:** Veteran Analytics – VISTA API Backend  
**Environment:** Windows (CMD + Git Bash), GitHub, local venv  
**Repo:** https://github.com/MarcArmy2003/veteran-analytics  

---

### ✅ Summary of Work Performed

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
