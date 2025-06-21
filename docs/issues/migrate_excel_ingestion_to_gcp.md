# Migrate Excel Data Ingestion to Google Cloud Storage & Cloud Run/Functions

**Overview**

The existing Excel processing workflow (`definitive_chunker.py`) runs manually on a local drive. We need to migrate this to Google Cloud Platform to improve scalability and reliability.

**Goals**

- Use Google Cloud Storage (GCS) for all input and output files.
- Trigger a cloud-based process automatically when new `.xls` files are uploaded.
- Run `definitive_chunker.py` in Cloud Run or Cloud Functions.
- Store processed `.txt` files in a destination bucket and ingest them into Vertex AI.

**Why Migrate?**

- **Scalability**: Local processing can't easily handle large data or concurrent jobs.
- **Reliability**: Removing manual steps reduces errors like `FileNotFoundError`.
- **Operational Simplicity**: Frees local resources and sets up the foundation for a full-service backend.
- **Cloud Alignment**: Keeps all data and compute within GCP.

**Sub‑Tasks & Considerations**

1. **Setup GCS Buckets**
   - Create source bucket for raw uploads (e.g., `gs://vista-raw-data-uploads`).
   - Create destination bucket for processed output (e.g., `gs://vista-processed-data`).

2. **Refactor `definitive_chunker.py`**
   - Read from a GCS URI instead of a local path.
   - Write processed output to a GCS URI.
   - Add robust error handling for cloud operations.
   - Confirm sheet name sanitization and chunking logic.

3. **Containerize (if using Cloud Run)**
   - Build a Dockerfile with all dependencies (pandas, xlrd, etc.).
   - Ensure `requirements.txt` is complete.

4. **Choose Execution Environment**
   - Decide between Cloud Functions (simple, event‑driven) or Cloud Run (containerized).
   - Configure triggers: object finalize event for Functions or Pub/Sub for Run.

5. **IAM & Deployment**
   - Grant the service account read/write access to both buckets.
   - Deploy the service and connect the trigger.

6. **Integration & Testing**
   - Upload a test `.xls` file to verify end-to-end automation.
   - Check that the `.txt` output is created in the destination bucket.
   - Confirm Vertex AI ingestion works without file-size errors.
   - Set up Cloud Monitoring and Logging for troubleshooting.

🚀 **Next Steps**

- Document deployment instructions and update the repository once the migration is tested and stable.

