from flask import Flask, jsonify, request
import gspread
import pandas as pd
import os

app = Flask(__name__)

# --- Global Cache ---
# We will store the data here after it's loaded once.
_spreadsheet_data_cache = None

def get_data():
    """
    This function gets the spreadsheet data. It checks a global cache first.
    If the cache is empty, it loads the data from Google Sheets and populates the cache.
    """
    global _spreadsheet_data_cache
    if _spreadsheet_data_cache is not None:
        return _spreadsheet_data_cache

    print("--- First request received. Loading data from Google Sheets into cache... ---")
    try:
        key_file = 'vista-api-backend-6578a1a1c769.json'
        spreadsheet_title = 'Open VA Data APIs'
        worksheet_names = [
            "API Name and Path", "VA Data Census Bureau APIs",
            "Census Bureau APIs - Full List", "VISTA Custom GPT Actions", "Utilities"
        ]

        gc = gspread.service_account(filename=key_file)
        spreadsheet = gc.open(spreadsheet_title)
        all_data = {}
        for sheet_name in worksheet_names:
            worksheet = spreadsheet.worksheet(sheet_name)
            records = worksheet.get_all_records()
            if records:
                df = pd.DataFrame(records)
                all_data[sheet_name] = df
        
        _spreadsheet_data_cache = all_data
        print("--- Caching complete. ---")
        return _spreadsheet_data_cache

    except Exception as e:
        error_info = {"error": "Failed to load data on first request", "message": str(e)}
        _spreadsheet_data_cache = error_info
        print(f"--- ERROR during data load: {str(e)} ---")
        return _spreadsheet_data_cache

@app.route('/')
def home():
    data = get_data()
    if isinstance(data, dict) and data.get("error"):
        return jsonify(data), 500
    return "VA Data Backend API is running."

@app.route('/query_api_paths')
def query_api_paths():
    data = get_data()
    if isinstance(data, dict) and data.get("error"):
        return jsonify(data), 500

    if "API Name and Path" not in data:
        return jsonify({"error": "Sheet 'API Name and Path' not found in cache."}), 500

    # This logic assumes the columns from our previous successful tests
    df_api_paths = data["API Name and Path"]
    category = request.args.get('category')
    
    if not category:
        return jsonify(df_api_paths.to_dict(orient='records'))

    results = df_api_paths[df_api_paths['Categorization'].str.contains(category, case=False, na=False)]
    return jsonify(results.to_dict(orient='records'))