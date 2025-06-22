import os
import pandas as pd

source_dir = r"C:\VISTA_TEMP\data\XLS_TO_PROCESS"
output_dir = r"C:\VISTA_TEMP\data\XLS_TO_PROCESS/CSV_Output"
os.makedirs(output_dir, exist_ok=True)

for file_name in os.listdir(source_dir):
    if file_name.lower().endswith((".xls", ".xlsx")):
        file_path = os.path.join(source_dir, file_name)
        try:
            excel_file = pd.ExcelFile(file_path)
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                safe_sheet_name = "".join(c if c.isalnum() else "_" for c in sheet_name)
                output_file = f"{os.path.splitext(file_name)[0]}__{safe_sheet_name}.csv"
                output_path = os.path.join(output_dir, output_file)
                df.to_csv(output_path, index=False, encoding="utf-8")
                print(f"Converted: {file_name} [{sheet_name}] -> {output_file}")
        except Exception as e:
            print(f"Failed to convert {file_name}: {e}")
