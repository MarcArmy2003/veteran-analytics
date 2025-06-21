import os
import pandas as pd
import glob
import re
import time

# --- CONFIGURATION ---
XLS_INPUT_FOLDER = r"C:\VISTA_TEMP\data\XLS_TO_PROCESS"
CSV_OUTPUT_FOLDER = os.path.join(XLS_INPUT_FOLDER, "CSV_Output")
MARKDOWN_OUTPUT_FOLDER = r"C:\VISTA_Repository\ABR Excel Table Markdowns"
MAX_BYTES = 2000000  # 2MB

# --- STEP 1: XLS/XLSX to Multi-sheet CSV Conversion ---
def convert_xls_to_csv(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    print("--- Starting Excel to CSV Conversion ---")
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith((".xls", ".xlsx")):
            file_path = os.path.join(input_folder, file_name)
            try:
                excel_file = pd.ExcelFile(file_path)
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    if df.empty:
                        continue
                    safe_sheet = "".join(c if c.isalnum() else "_" for c in sheet_name)
                    csv_name = f"{os.path.splitext(file_name)[0]}__{safe_sheet}.csv"
                    csv_path = os.path.join(output_folder, csv_name)
                    df.to_csv(csv_path, index=False, encoding="utf-8")
                    print(f"  -> Saved: {csv_name}")
            except Exception as e:
                print(f"  -> ERROR converting {file_name}: {e}")
    print("--- Excel to CSV Conversion Complete ---\n")

# --- STEP 2: Chunk CSVs into Markdown Files ---
def process_and_chunk_csv(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    print("--- Starting CSV Chunking ---")
    
    all_csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    if not all_csv_files:
        print("No CSV files found to process.")
        return

    for csv_path in all_csv_files:
        original_filename = os.path.basename(csv_path)
        print(f"Processing file: {original_filename}")
        try:
            df = pd.read_csv(csv_path)
            if df.empty:
                print("  -> File is empty. Skipping.")
                continue

            rows_for_chunk = []
            part_num = 1
            for _, row in df.iterrows():
                rows_for_chunk.append(row)
                temp_chunk_df = pd.DataFrame(rows_for_chunk, columns=df.columns)
                markdown_size = len(temp_chunk_df.to_markdown(index=False).encode('utf-8'))

                if markdown_size > MAX_BYTES and len(rows_for_chunk) > 1:
                    chunk_to_write = pd.DataFrame(rows_for_chunk[:-1], columns=df.columns)
                    write_chunk_to_file(chunk_to_write, original_filename, part_num, output_folder)
                    rows_for_chunk = [row]
                    part_num += 1

            if rows_for_chunk:
                final_chunk_df = pd.DataFrame(rows_for_chunk, columns=df.columns)
                write_chunk_to_file(final_chunk_df, original_filename, part_num, output_folder)

            time.sleep(0.1)
            os.remove(csv_path)
            print(f"  -> Successfully processed and deleted: {original_filename}")

        except Exception as e:
            print(f"  -> ERROR: Could not process file '{original_filename}'. Reason: {e}")

def write_chunk_to_file(df, original_filename, part_num, output_path):
    if df.empty:
        return

    base_name, _ = os.path.splitext(original_filename)
    part_str = f" - part_{part_num}" if part_num > 1
