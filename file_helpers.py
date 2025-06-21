import os
import shutil
import hashlib
from pathlib import Path

# --- Configuration for Helper Script (Paths derived directly from your input) ---
# These paths point to your original, local OneDrive directories.
ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR = Path(r"C:\Users\gillo\OneDrive\Documents\ChatGPT Instructions")
ONEDRIVE_VISTA_API_BACKEND_DIR = ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR / "VISTA API Backend"
ONEDRIVE_XLS_TO_PROCESS_DIR = ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR / "XLS_TO_PROCESS"
ONEDRIVE_VETERAN_ANALYTICS_BACKUP_DIR = Path(r"C:\Users\gillo\OneDrive\Documents\veteran-analytics - backup")
ONEDRIVE_VETERAN_ANALYTICS_DIR = Path(r"C:\Users\gillo\OneDrive\Documents\veteran-analytics")

# This is your NEW, clean working directory where the GitHub repo is cloned.
# This should be the directory you created previously (e.g., C:\VISTA_Project).
NEW_VISTA_PROJECT_ROOT = Path(r"C:\VISTA_Project")

# This is the LOCAL archive destination for large source files.
LOCAL_ARCHIVE_DESTINATION_DIR = Path(r"D:\VISTA_Data_Archive")

# --- Helper Functions ---

def get_file_hash(filepath, block_size=65536):
    """Generates an MD5 hash for a given file to check for content identity."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except Exception as e:
        print(f"  ERROR: Could not hash file {filepath}: {e}")
        return None

def list_files_in_directory(directory_path):
    """
    Lists all files in a given directory and its subdirectories.
    Returns a dictionary with file paths (as strings) as keys and a dict of metadata as values.
    """
    if not directory_path.is_dir():
        print(f"Error: Directory not found or is not a directory: {directory_path}")
        return {}

    file_list = {}
    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = Path(root) / filename
            try:
                stat_info = filepath.stat()
                file_list[str(filepath)] = { # Store as string for consistency with os.path
                    "size_bytes": stat_info.st_size,
                    "mod_time": stat_info.st_mtime, # Last modification time
                    "hash": get_file_hash(filepath) # Get hash for content comparison
                }
            except Exception as e:
                print(f"  WARNING: Could not get info for {filepath}: {e}")
                file_list[str(filepath)] = {"size_bytes": 0, "mod_time": 0, "hash": None}
    return file_list

def compare_directories(dir1, dir2):
    """
    Compares files in two directories and identifies unique and common files.
    Compares based on relative path and content hash.
    """
    print(f"\n--- Comparing {dir1} and {dir2} ---")
    files1 = list_files_in_directory(dir1)
    files2 = list_files_in_directory(dir2)

    unique_to_dir1 = []
    unique_to_dir2 = []
    common_identical = []
    common_different_content = []

    # Helper to get relative path
    def get_relative_path(full_path_str, base_path_obj):
        full_path = Path(full_path_str)
        try:
            return str(full_path.relative_to(base_path_obj))
        except ValueError:
            # Handle cases where full_path is not a child of base_path_obj
            return str(full_path) # Return full path if relative path cannot be determined

    # Check files in dir1
    for path1_str, info1 in files1.items():
        rel_path1 = get_relative_path(path1_str, dir1)
        found_in_dir2 = False
        for path2_str, info2 in files2.items():
            rel_path2 = get_relative_path(path2_str, dir2)
            if rel_path1 == rel_path2:
                found_in_dir2 = True
                if info1["hash"] == info2["hash"] and info1["hash"] is not None:
                    common_identical.append(rel_path1)
                else:
                    common_different_content.append(rel_path1)
                break
        if not found_in_dir2:
            unique_to_dir1.append(rel_path1)

    # Check files in dir2 that were not in dir1 (to find truly unique to dir2)
    for path2_str, info2 in files2.items():
        rel_path2 = get_relative_path(path2_str, dir2)
        found_in_dir1 = False
        for path1_str, info1 in files1.items():
            rel_path1 = get_relative_path(path1_str, dir1)
            if rel_path2 == rel_path1: # Already processed this as common
                found_in_dir1 = True
                break
        if not found_in_dir1:
            unique_to_dir2.append(rel_path2)

    print("\nFiles Unique to Directory 1 (Source):")
    if unique_to_dir1:
        for f in unique_to_dir1:
            print(f"- {f}")
    else:
        print("  None")

    print("\nFiles Unique to Directory 2 (Target):")
    if unique_to_dir2:
        for f in unique_to_dir2:
            print(f"- {f}")
    else:
        print("  None")

    print("\nFiles Common to Both (Identical Content):")
    if common_identical:
        for f in common_identical:
            print(f"- {f}")
    else:
        print("  None")

    print("\nFiles Common to Both (Different Content - review needed):")
    if common_different_content:
        for f in common_different_content:
            print(f"- {f}")
    else:
        print("  None")

    return {
        "unique_to_dir1": unique_to_dir1,
        "unique_to_dir2": unique_to_dir2,
        "common_identical": common_identical,
        "common_different_content": common_different_content
    }

def copy_file(source_path_str, destination_path_str):
    """Copies a single file, creating destination directories if necessary."""
    source_path = Path(source_path_str)
    destination_path = Path(destination_path_str)

    if not source_path.exists():
        print(f"Error: Source file does not exist: {source_path}")
        return False
    
    # Create destination directory if it doesn't exist
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Copied: {source_path} -> {destination_path}")
        return True
    except Exception as e:
        print(f"Error copying {source_path} to {destination_path}: {e}")
        return False

def copy_files_to_archive(source_directory_str, archive_destination_directory_str):
    """
    Copies all files and subdirectories from a source to an archive destination.
    Creates the destination directory if it doesn't exist.
    """
    source_directory = Path(source_directory_str)
    archive_destination_directory = Path(archive_destination_directory_str)

    if not source_directory.is_dir():
        print(f"Error: Source directory for archive not found: {source_directory}")
        return

    archive_destination_directory.mkdir(parents=True, exist_ok=True)
    
    print(f"\n--- Archiving files from {source_directory} to {archive_destination_directory} ---")
    try:
        # Handle case where source_directory might be empty
        if not list(source_directory.iterdir()):
            print(f"  Source directory '{source_directory}' is empty. Nothing to archive.")
            return

        for item in source_directory.iterdir():
            s = item
            d = archive_destination_directory / item.name
            if s.is_dir():
                shutil.copytree(s, d, dirs_exist_ok=True)
                print(f"  Copied directory: {item.name}/")
            else:
                shutil.copy2(s, d)
                print(f"  Copied file: {item.name}")
        print("Archiving complete.")
    except Exception as e:
        print(f"Error during archiving from {source_directory}: {e}")

def delete_file_with_confirmation(file_path_str):
    """Deletes a single file after explicit user confirmation."""
    file_path = Path(file_path_str)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return False

    print(f"\nATTENTION: You are about to DELETE the following file:")
    print(f"  Path: {file_path}")
    confirmation = input("Are you absolutely sure you want to delete this file? Type 'yes' to confirm: ").strip().lower()

    if confirmation == 'yes':
        try:
            file_path.unlink() # Use Path.unlink() for file deletion
            print(f"SUCCESS: Deleted {file_path}")
            return True
        except Exception as e:
            print(f"ERROR: Could not delete {file_path}: {e}")
            return False
    else:
        print(f"Deletion cancelled for {file_path}.")
        return False

# --- Main Execution Block (Example Usage for direct execution) ---
if __name__ == "__main__":
    print("--- VISTA File Reorganization Helpers ---")
    print("This script provides utility functions for managing your project files.")
    print("It is primarily designed to be imported by other scripts, like organize_project.py.")
    print("You can also use its functions directly from a Python interpreter or PowerShell.")

    print("\nExample: Listing files in your ChatGPT Instructions folder:")
    files_in_chatgpt = list_files_in_directory(ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR)
    for filepath, info in files_in_chatgpt.items():
        print(f'- {filepath} (Size: {info["size_bytes"]} bytes)')

    print("\n--- Helpers loaded. Use them with caution and specific commands. ---")

