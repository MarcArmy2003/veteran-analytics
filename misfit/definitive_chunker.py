import os
import pandas as pd
import glob
import re
import time
import pyexcel as p 

# --- CONFIGURATION ---
XLS_INPUT_FOLDER = "C:\VISTA_TEMP\data\XLS_TO_PROCESS"
MARKDOWN_OUTPUT_FOLDER = "C:\VISTA_Repository\ABR Excel Table Markdowns"
MAX_BYTES = 2000000 # 2MB to be safe

def preprocess_and_convert_files(input_folder):
    """
    Scans for .xls files that are unreadable by pandas and converts them
    into the modern .xlsx format using pyexcel.
    """
    print("--- Starting Pre-processing Step: Checking for problematic .xls files... ---")
    xls_files = glob.glob(os.path.join(input_folder, '*.xls'))
    
    for xls_path in xls_files:
        try:
            # Try to open with pandas. If it fails, we convert it.
            pd.ExcelFile(xls_path).close()
        except Exception as e:
            original_filename = os.path.basename(xls_path)
            print(f"  -> Found problematic file: '{original_filename}'. Attempting conversion to .xlsx...")
            
            new_xlsx_path = xls_path.replace('.xls', '.preprocessed.xlsx')
            
            try:
                # Use pyexcel to save the file in the .xlsx format
                p.save_book_as(file_name=xls_path, dest_file_name=new_xlsx_path)
                os.remove(xls_path) # Delete the old problematic file
                print(f"     - Successfully converted to: '{os.path.basename(new_xlsx_path)}'")
            except Exception as convert_e:
                print(f"     - ERROR: Failed to convert file '{original_filename}'. Reason: {convert_e}")
    print("--- Pre-processing Finished. ---\n")


def process_and_chunk_excel(input_folder, output_folder):
    """
    Main processing function to read, chunk, and delete Excel files.
    Now handles both .xls and .xlsx files.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    print("--- Starting Main Processing Step: Chunking all Excel files... ---")
    all_excel_files = glob.glob(os.path.join(input_folder, '*.xls*'))

    if not all_excel_files:
        print("No Excel files found to process.")
        return

    for excel_path in all_excel_files:
        original_filename = os.path.basename(excel_path)
        print(f"Processing file: {original_filename}")
        try:
            with pd.ExcelFile(excel_path) as xls:
                for sheet_name in xls.sheet_names:
                    print(f"  -> Processing sheet: '{sheet_name}'")
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    if df.empty:
                        print("     - Sheet is empty. Skipping.")
                        continue

                    # The deep chunking logic from before
                    rows_for_chunk = []
                    part_num = 1
                    for _, row in df.iterrows():
                        rows_for_chunk.append(row)
                        temp_chunk_df = pd.DataFrame(rows_for_chunk, columns=df.columns)
                        markdown_size = len(temp_chunk_df.to_markdown(index=False).encode('utf-8'))

                        if markdown_size > MAX_BYTES and len(rows_for_chunk) > 1:
                            chunk_to_write = pd.DataFrame(rows_for_chunk[:-1], columns=df.columns)
                            write_chunk_to_file(chunk_to_write, original_filename, sheet_name, part_num, output_folder)
                            rows_for_chunk = [row]
                            part_num += 1
                    
                    if rows_for_chunk:
                        final_chunk_df = pd.DataFrame(rows_for_chunk, columns=df.columns)
                        write_chunk_to_file(final_chunk_df, original_filename, sheet_name, part_num, output_folder)
            
            time.sleep(0.1)
            os.remove(excel_path)
            print(f"  -> Successfully processed and deleted: {original_filename}")

        except Exception as e:
            print(f"  -> ERROR: Could not process file '{original_filename}'. Reason: {e}")

def write_chunk_to_file(df, original_filename, sheet_name, part_num, output_path):
    """Helper function to write a dataframe chunk to a text file."""
    if df.empty:
        return
    
    original_filename_without_ext, _ = os.path.splitext(original_filename)
    safe_sheet_name = re.sub(r'[\\/*?:"<>|]', "", sheet_name).strip()
    part_str = f" - part_{part_num}" if part_num > 1 or len(df.index) > 0 else "" # Check logic for part_str

    txt_filename = os.path.join(output_path, f"{original_filename_without_ext} - {safe_sheet_name}{part_str}.txt")
    header = f"# Data from {original_filename}\n## Sheet: {sheet_name}{part_str.replace('_', ' ').title()}\n\n"
    final_markdown = df.to_markdown(index=False)

    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(header + final_markdown)
    print(f"     - Wrote chunk to: {os.path.basename(txt_filename)}")


if __name__ == "__main__":
    print("--- Starting Excel to Markdown Conversion (v5 with Pre-processing) ---")
    preprocess_and_convert_files(XLS_INPUT_FOLDER)
    process_and_chunk_excel(XLS_INPUT_FOLDER, MARKDOWN_OUTPUT_FOLDER)
    print("\n--- Script Finished ---")