# --- File: app.py ---
# Description: This script deploys a Flask-based API backend for the VISTA project.
# It serves data retrieved from a Google Sheet, acting as a data source for other services.
# The API uses an in-memory cache to ensure fast response times after the initial data load.

from flask import Flask, jsonify, request
import gspread
import pandas as pd
import os

app = Flask(__name__)

# --- Global Cache ---
# A global variable to store the data from Google Sheets after the first request.
# This prevents re-fetching the data on every API call, significantly improving performance.
_spreadsheet_data_cache = None

def get_data():
    """
    Retrieves data from the 'Open VA Data APIs' Google Sheet, utilizing an in-memory cache.

    On the first request, this function connects to the Google Sheets API using service account
    credentials, loads specific worksheets into pandas DataFrames, and stores them in the 
    global '_spreadsheet_data_cache'. Subsequent calls return the cached data directly.

    Returns:
        dict: A dictionary where keys are worksheet names and values are pandas DataFrames.
              In case of an error during the initial load, it returns a dictionary 
              with 'error' and 'message' keys.
    """
    global _spreadsheet_data_cache
    # If the cache is already populated, return it immediately.
    if _spreadsheet_data_cache is not None:
        return _spreadsheet_data_cache

    print("--- First request received. Loading data from Google Sheets into cache... ---")
    try:
        # --- Configuration for Google Sheets ---
        # Service account key file for authentication.
        key_file = 'vista-api-backend-6578a1a1c769.json'
        # The exact title of the Google Sheet to open.
        spreadsheet_title = 'Open VA Data APIs'
        # A list of specific worksheets to load from the spreadsheet.
        worksheet_names = [
            "API Name and Path", "VA Data Census Bureau APIs",
            "Census Bureau APIs - Full List", "VISTA Custom GPT Actions", "Utilities"
        ]

        gc = gspread.service_account(filename=key_file)
        spreadsheet = gc.open(spreadsheet_title)
        all_data = {}
        # Iterate through the specified worksheet names and load each into a DataFrame.
        for sheet_name in worksheet_names:
            worksheet = spreadsheet.worksheet(sheet_name)
            records = worksheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                all_data[sheet_name] = df
        
        # Populate the cache with the loaded data.
        _spreadsheet_data_cache = all_data
        print("--- Caching complete. ---")
        return _spreadsheet_data_cache

    except Exception as e:
        # If any error occurs during the process, cache the error information.
        error_info = {"error": "Failed to load data on first request", "message": str(e)}
        _spreadsheet_data_cache = error_info
        print(f"--- ERROR during data load: {str(e)} ---")
        return _spreadsheet_data_cache

@app.route('/')
def home():
    """
    A simple health-check endpoint for the API.

    Triggers the initial data load if the cache is empty and confirms that the API is running.

    Returns:
        str: A simple string "VA Data Backend API is running." on success.
        tuple: A JSON error object and a 500 status code if the data cache fails to load.
    """
    data = get_data()
    if isinstance(data, dict) and data.get("error"):
        return jsonify(data), 500
    return "VA Data Backend API is running."

@app.route('/query_api_paths')
def query_api_paths():
    """
    An API endpoint to query VA API paths from the 'API Name and Path' sheet.

    This endpoint supports filtering by category via a URL query parameter.
    If no category is provided, it returns all records from the sheet.

    Query Parameters:
        category (str, optional): The category to filter by (e.g., 'Demographics'). 
                                  The search is case-insensitive.

    Returns:
        tuple: A JSON object containing a list of records and a 200 status code.
               Returns a 404 or 500 error with a JSON message if data is not found 
               or an error occurs.
    """
    data = get_data()
    # Check if the data cache loaded successfully.
    if isinstance(data, dict) and data.get("error"):
        return jsonify(data), 500

    # Ensure the required sheet exists in the cache.
    if "API Name and Path" not in data:
        return jsonify({"error": "Sheet 'API Name and Path' not found in cache."}), 500

    df_api_paths = data["API Name and Path"]
    category = request.args.get('category')
    api_name = request.args.get('api_name')

    results = df_api_paths

    if category:
        if 'Categorization' not in results.columns:
            return jsonify({"error": "Column 'Categorization' not found in sheet."}), 500
        results = results[results['Categorization'].str.contains(category, case=False, na=False)]

    if api_name:
        api_col = None
        for candidate in ["Dataset / Table Name", "API Name"]:
            if candidate in results.columns:
                api_col = candidate
                break
        if not api_col:
            return jsonify({"error": "API name column not found in sheet."}), 500
        results = results[results[api_col].astype(str).str.contains(api_name, case=False, na=False)]

    return jsonify(results.to_dict(orient='records'))