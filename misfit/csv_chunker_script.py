import os
import pandas as pd
import glob
import re
import time

# --- CONFIGURATION ---
CSV_INPUT_FOLDER = r"C:\VISTA_TEMP\data\XLS_TO_PROCESS\CSV_Output"
MARKDOWN_OUTPUT_FOLDER = r"C:\VISTA_Repository\ABR Excel Table Markdowns"
MAX_BYTES = 2000000  # 2MB to be safe

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
    part_str = f" - part_{part_num}" if part_num > 1 or len(df.index) > 0 else ""
    txt_filename = os.path.join(output_path, f"{base_name}{part_str}.txt")

    header = f"# Data from {original_filename}\n## CSV File{part_str.replace('_', ' ').title()}\n\n"
    final_markdown = df.to_markdown(index=False)

    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(header + final_markdown)
    print(f"     - Wrote chunk to: {os.path.basename(txt_filename)}")

if __name__ == "__main__":
    print("--- Starting CSV to Markdown Conversion ---")
    process_and_chunk_csv(CSV_INPUT_FOLDER, MARKDOWN_OUTPUT_FOLDER)
    print("--- Script Finished ---")
