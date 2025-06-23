# GPT Actions

This folder hosts OpenAPI specifications and example schema files used by the VISTA Custom GPT.  These specs define the HTTP actions that the model can invoke to retrieve VA and Census data through our backend services.

## Available Specs
- **`openapi_spec.yaml`** – primary backend specification. It exposes two actions:
  - `GET /query_api_paths` – search the "API Name and Path" sheet for VA dataset paths.
  - `GET /query_census_apis_full_list` – search the "Census Bureau APIs - Full List" sheet by dataset name and year.
- **`specs/VA Core Datasets API.txt`** – condensed OpenAPI spec containing ~30 high‑value VA endpoints optimized for GPT actions.
- **`specs/OpenAPI JSON spec for VA Data.txt`** – comprehensive listing of 123 VA dataset endpoints.
- **`specs/VISTA_CustomGPT_Actions_Config 2025-06-03 04_58_52.json`** – sample configuration showing third‑party APIs (EPA, CDC, NARA, Census) that can be wired into the GPT.
- Numerous additional Google API specs are provided under `specs/` for experimentation.

## Usage
Start the Flask backend (`python app/app.py`) so the actions are reachable.  Once running, they can be invoked via standard HTTP requests:

```bash
curl "http://localhost:5000/query_api_paths?category=Demographics"
curl "http://localhost:5000/query_census_apis_full_list?dataset_name=cbp&year=1986"
```

The Custom GPT calls these endpoints using the same parameters. Responses are returned as JSON arrays.

## Integration with the Backend
The endpoints defined in `openapi_spec.yaml` are implemented in `app/app.py`.  Data is loaded from Google Sheets via `sheets_reader.py` and cached in memory for fast responses.  By referencing these specs in a Custom GPT configuration, the model can issue structured API calls and incorporate the results directly into its replies.
