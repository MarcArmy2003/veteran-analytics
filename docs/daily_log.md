## VISTA Project Log: 2025-07-02

**Session Time:** 11:23 PM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Successfully implemented a cloud-based solution for converting `.xls` files to Markdown (`.txt`) and deep-chunking them to meet Vertex AI Search ingestion size limits.
* **Objective 2:** Successfully ran the `xls` conversion and deep-chunking job in Google Cloud Run.
* **Decision:** Opted for a Cloud Run Job to perform the `xls` conversion and deep-chunking.
* **Decision:** Decided to save the converted and deep-chunked Markdown files to a new, dedicated Cloud Storage path (`gs://vista-api-backend-rag-files/converted_and_deep_chunked_markdown/`) for clean ingestion into Vertex AI Search.
* **Decision:** Determined that a new, separate Vertex AI Search data store for the converted XLS data is the wisest approach for clarity and isolation.
* **Code Created/Modified:**
    * `XLS_Deep_Chunker.py`: Modified the XLS conversion script to include deep-chunking logic and interact with Google Cloud Storage paths for input (`ABRs/ABR Tables/`) and output (`converted_and_deep_chunked_markdown/`).
    * `Dockerfile`: Updated to correctly reference `XLS_Deep_Chunker.py` and streamline build steps.
    * `requirements.txt`: Confirmed necessary libraries like `pandas`, `google-cloud-storage`, and `openpyxl`.

### ⚠️ Challenges & Roadblocks

* **Issue:** Initial `gsutil cp` commands in Cloud Shell failed due to placeholder filenames and later due to files not being in the current working directory.
* **Solution:** Resolved by guiding precise `mv` commands and later relying on `cloudshell edit` for direct file manipulation in the correct directory.
* **Issue:** `ServiceException: 401 Anonymous caller does not have storage.objects.create access` during Cloud Storage uploads and `storage.objects.get` during `gsutil ls`.
* **Solution:** Resolved by confirming `Storage Object Admin` IAM role for the user account and allowing time for permissions propagation.
* **Issue:** Docker image build failed (`COPY failed: file not found`) because the `Dockerfile` referenced the old script name (`definitive_convert_no_chunking_gcs.py`) instead of `XLS_Conversion.py` (which was renamed to `XLS_Deep_Chunker.py` for this purpose).
* **Solution:** Updated the `Dockerfile` to correctly reference `XLS_Deep_Chunker.py`.
* **Issue:** `gcloud run jobs create` failed with `unrecognized arguments: --no-cpu-throttling`.
* **Solution:** Removed the unsupported `--no-cpu-throttling` flag for Cloud Run Jobs.
* **Issue:** `gcloud run jobs update` failed with `unrecognized arguments: --timeout=3600 (did you mean '--task-timeout'?)`.
* **Solution:** Corrected the flag to `--task-timeout=3600` for Cloud Run Jobs.
* **Issue:** Cloud Run Job failed to find `.xls` files, logging "No .xls files found in the specified GCS path".
* **Solution:** Identified the correct source path for `.xls` files as `ABRs/ABR Tables/` in the bucket and updated the `SOURCE_PREFIX` in `XLS_Deep_Chunker.py`.
* **Issue:** Cloud Run Job timed out (`600 seconds`) before completing XLS conversion.
* **Solution:** Increased the job timeout to 3600 seconds (1 hour) using `--task-timeout=3600`.
* **Issue:** Vertex AI Search ingestion previously failed for `.xls` files with "File extension type is xls, and it is not supported" and later for converted `.txt` files due to exceeding 10MB limit ("can be at most 10000000 bytes, got 38922990").
* **Solution:** Implemented `XLS_Deep_Chunker.py` to perform byte-size based deep-chunking of converted Markdown content, ensuring files are below the 10MB limit.

### 🚀 Next Steps

* **Immediate Goal:** Create a new Vertex AI Search data store (e.g., `vista-deep-chunked-xls-data`) pointing to `gs://vista-api-backend-rag-files/converted_and_deep_chunked_markdown/` to ingest the newly processed and deep-chunked XLS data.
* **Future Goal:** Create a Vertex AI Search application to query the ingested data.
* **Future Goal:** Integrate API calls using a Google Sheet as another data source within the final VISTA application.

----

## VISTA Project Log: 2025-06-22

**Session Time:** 12:54 AM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1: Secure Cloud Deployment of API Backend**
    * Successfully provisioned and securely stored the Google Cloud Service Account Key in Google Cloud Secret Manager.
    * Granted the necessary `secretmanager.secretAccessor` IAM role to the Cloud Run service account for the secret.
    * Successfully containerized the Flask API application into a Docker image.
    * Successfully pushed the Docker image to Google Container Registry.
    * Successfully deployed the Flask API to Google Cloud Run, configured to securely retrieve credentials from Secret Manager at runtime.
* **Decision:**
    * Established and implemented the critical security decision to **never commit service account keys directly to GitHub**.
    * Adopted the use of environment variables (`GOOGLE_APPLICATION_CREDENTIALS`) for handling credentials in `app.py` for both local and cloud environments.
    * Confirmed using Google Cloud Secret Manager as the secure storage solution for production secrets.
    * Consolidated `Dockerfile`, `app.py`, and `requirements.txt` into a single `/app` directory within `vista-api-backend` for streamlined Docker builds.

* **Code Created/Modified:**
    * `app.py`: Updated to read `GOOGLE_APPLICATION_CREDENTIALS` from environment variables; added detailed comments and docstrings.
    * `Dockerfile`: Content provided and used for containerization.

### ⚠️ Challenges & Roadblocks

* **Issue: Permission Denied during Secret Creation:** Initially, the authenticated Google Cloud account lacked the necessary IAM permissions to create secrets.
* **Solution:** Resolved by explicitly granting the `Secret Manager Admin` role (or confirming `Owner` role) to the user's Google Cloud account via the IAM section in the Google Cloud Console.
* **Issue: Windows Command Prompt (CMD) Syntax Differences:** Repeated errors due to incorrect syntax for environment variables (`export` vs `set`, `${VAR}` vs `%VAR%`) and multi-line commands (`#` comments, missing `^` characters) in `cmd.exe`.
* **Solution:** Provided precise `cmd.exe` syntax for setting environment variables (`set VAR=value`) and for multi-line command continuation (`^`).
* **Issue: Docker Daemon Connectivity:** Encountered "ERROR: error during connect: The system cannot find the file specified" when attempting `docker build`, implying Docker Desktop was not running.
* **Solution:** Ensured Docker Desktop application was fully running and accessible before re-attempting Docker commands.
* **Issue: Unauthenticated Docker Push:** Received "error from registry: Unauthenticated request" when pushing the Docker image to GCR.
* **Solution:** Authenticated Docker with Google Cloud credentials using `gcloud auth configure-docker`.
* **Issue: "Image not found" during Cloud Run Deployment:** Initial deployment failed because the Cloud Run service could not locate the Docker image.
* **Solution:** This was a cascading issue resolved by the successful `docker build` and `docker push` commands following the authentication fix.
* **Issue: `gcloud` Project ID Not Recognized:** The `--project=%GOOGLE_CLOUD_PROJECT%` was not always correctly interpreted, leading to `not a valid project ID` error.
* **Solution:** Explicitly set the default `gcloud` project for the CLI session using `gcloud config set project vista-api-backend`.

### 🚀 Next Steps

* **Immediate Goal:** Thoroughly test the newly deployed Cloud Run API service using the provided Service URL to confirm all endpoints function correctly.
* **Future Goal:** Begin refining the OpenAPI documentation (`openapi_spec.yaml`) and enhancing overall project documentation (`README.md`, `project-overview.md`), incorporating the clarity gained from deployment. Subsequently, start sketching out the user interface and user flow for the VISTA application, building upon the now-accessible API.

----

## VISTA Project Log: 2025-06-21

**Session Time:** 3:45 AM EDT

---

### ✅ Accomplishments & Key Decisions

- **Objective 1:** Successfully executed the preliminary automated file organization. Approximately 5700 files were copied and categorized from OneDrive sources into the new `C:\veteran-analytics` Git repository.
- **Objective 2:** Diagnosed and resolved a critical GitHub Push Protection error (GH013) caused by accidentally committed Google Cloud Service Account credentials.
- **Objective 3:** Removed the sensitive credential file from Git history and added its specific paths (`misfit/vista-api-backend-6578a1a1c769.json`, `specs/vista-api-backend-6578a1a1c769.json`) to `.gitignore` to prevent future accidental commits.
- **Decision:** Renamed the local project root folder from `C:\VISTA_Project` to `C:\veteran-analytics` for consistency with the GitHub repository. This directory is now the definitive source for all project files.
- **Decision:** Opted not to proceed with automated versioning/renaming of conflicting files, completing the file organization phase after the initial copy.
- **Code Created/Modified:** Updated `organize_project.py` to correctly import `file_helpers.py` functions, added a `confirm_all` parameter and an optional combined execution path, and refined `file_helpers.py` path handling.

### ⚠️ Challenges & Roadblocks

- **Issue:** Persistent `FileNotFoundError` when running `organize_project.py` due to incorrect file locations and import errors.
- **Solution:** Saved both scripts in `C:\VISTA_Project` and revised import statements for direct, robust access to helper functions.
- **Issue:** `git push` rejected by GitHub Push Protection detecting the credential file.
- **Solution:** Removed the file with `git rm --cached`, added the paths to `.gitignore` via PowerShell, amended the commit to scrub history, and pushed with `--force-with-lease`.
- **Issue:** Could not access `C:\veteran-analytics` via File Explorer for `.gitignore` edits.
- **Solution:** Modified `.gitignore` directly from PowerShell and verified the folder with `Get-ChildItem`.

### 🚀 Next Steps

- **Immediate Goal:** File organization phase marked complete.
- **Future Goal:** Determine next steps, potentially building a scalable data ingestion solution on Google Cloud, formalizing legal paperwork, and setting up placeholder websites.

----

## VISTA Project Log: 2025-06-20

**Session Time:** 01:00 AM EDT

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

----

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

- Validate `definitive_chunker_v4.py` across all datasets to produce sub-2.5MB `.txt` outputs and complete Vertex AI ingestion.
- Purge previous ingest attempts from GCS (`vista-api-backend-rag-files`) and deploy new data using `gcloud storage rsync`, then trigger the ingestion pipeline within Vertex AI for final verification.
- Confirm file visibility, completeness, and integrity within Vertex AI's retrieval system.
- Begin formal API endpoint testing and confirm backend functionality after restructuring; plan deployment to Cloud Run or App Engine.
- Commit finalized GitHub Actions CI/CD workflow (`pylint.yml`) and integrate automated checks into future pushes.

----

## VISTA Project Log: 2025-06-16

**Session Time:** 12:05 AM–10:27 PM EDT

---

### ✅ Accomplishments & Key Decisions

- Diagnosed Vertex AI ingestion failures caused by `pandas.to_markdown()` inflating `.txt` sizes. Updated `definitive_chunker.py` to calculate encoded byte size and hard-cap output, including automatic `.xls` to `.xlsx` conversion via `pyexcel`.
- Reorganized the repository: removed lingering submodule references, moved backend files into `src/vista-api-backend`, and added a `pylint.yml` CI workflow.
- Updated `openapi_spec.yaml`, improved project documentation with new guides in `/docs`, and added licensing files under `/legal`.
- Standardized the workflow using `C:\\VISTA_TEMP` and `gcloud storage rsync` for clean uploads to Google Cloud Storage.
- Established a contingency plan to migrate the pipeline to Google Cloud Dataflow if file-size issues persist.

### ⚠️ Challenges & Roadblocks

- Repeated file rejections and runtime errors from misconfigured paths and missing dependencies.
- Windows file move restrictions required command-line workarounds.
- Persistent Git submodule artifacts after deletion.

### 🚀 Next Steps

- Validate `definitive_chunker_v4.py` across all datasets to produce sub-2.5MB `.txt` outputs and complete Vertex AI ingestion.
- Purge previous ingest attempts from GCS (`vista-api-backend-rag-files`) and deploy new data using `gcloud storage rsync`, then trigger the ingestion pipeline within Vertex AI for final verification.
- Confirm file visibility, completeness, and integrity within Vertex AI's retrieval system.
- Begin formal API endpoint testing and confirm backend functionality after restructuring; plan deployment to Cloud Run or App Engine.
- Commit finalized GitHub Actions CI/CD workflow (`pylint.yml`) and integrate automated checks into future pushes.

----

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

----

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

----

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

----

## VISTA Project Log: 2025-06-12

**Session Time:** 02:30 PM EDT

---

### ✅ Accomplishments & Key Decisions

* **Objective 1:** Define the high-level technical architecture for the VISTA project.
* **Decision:** We established the core strategy of moving from static files to a dynamic, API-driven system. The plan is to build a Python backend using Flask that reads data from a Google Sheet and serves it to the VISTA Custom GPT via a custom API.
* **Decision:** Agreed on a strategy to overcome the 30 `operationId` limit in Custom GPTs by designing generalized, parameterized API actions. The backend API would handle the complex logic of mapping these general calls to specific data sources listed in the Google Sheet.

### ⚠️ Challenges & Roadblocks

* **Issue:** How to integrate VISTA with over 100 identified `data.va.gov` resources without violating the 30 `operationId` limit for GPT Actions.
* **Solution:** The chosen solution was to create a few broad API endpoints (e.g., `getDemographicsData`) that accept a `dataset` parameter. This allows the GPT to make a simple call, while the Python backend uses the parameter to look up the correct, specific data source from the master Google Sheet.
* **Issue:** Potential for hitting API rate limits from our data sources.
* **Solution:** We proactively reviewed the specific API quotas for both the Google Sheets API and `data.va.gov` to ensure the architecture would be robust and to plan for future scaling.

### 🚀 Next Steps

* **Immediate Goal:** Begin the practical, hands-on development by setting up the necessary Google Cloud Project and service account credentials for the Google Sheets API.
* **Future Goal:** Write the initial Python script to programmatically connect to the Google Sheet and read the data, which would serve as the foundation for the Flask API.

