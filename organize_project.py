import os
import shutil
from pathlib import Path
import re # Import for regular expressions
import datetime # Import for better date display

# Import helper functions from file_helpers.py
# Ensure file_helpers.py is in the same directory as this script.
# This direct import will resolve the 'NameError'
from file_helpers import (
    get_file_hash,
    list_files_in_directory,
    compare_directories,
    copy_file,
    copy_files_to_archive,
    delete_file_with_confirmation
)

# --- Configuration for Organization Script (Paths derived directly from your input) ---
# These are the *original* folders you want to pull files FROM for organization.
SOURCE_ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR = Path(r"C:\Users\gillo\OneDrive\Documents\ChatGPT Instructions")
SOURCE_ONEDRIVE_VISTA_API_BACKEND_DIR = Path(r"C:\Users\gillo\OneDrive\Documents\ChatGPT Instructions\VISTA API Backend")

# This is your NEW, clean working directory where the GitHub repo is cloned.
DESTINATION_VISTA_PROJECT_ROOT = Path(r"C:\VISTA_Project")

# Define mapping for file extensions and keywords to target subdirectories
# This mapping is based on common project structures and your existing GitHub repo.
# You will likely need to review and adjust this after the script runs!
CATEGORY_MAPPING = {
    # Core Application & Configuration
    "app": "app",
    "main": "app", # For main application entry points
    ".py": "app",         # Default for Python, refined by keywords
    "requirements.txt": "app",
    "Dockerfile": "app",
    "config.yml": "config",
    "config.yaml": "config",

    # Scripts & Utilities
    "script": "scripts",
    "chunker": "scripts",
    "convert": "scripts",
    "unzip": "scripts",
    "etl": "scripts",
    "loader": "scripts",
    "sheets_reader": "scripts",
    "extract": "scripts",
    "restructure": "scripts",
    
    # Documentation
    "docs": "docs",
    ".md": "docs",        # Default for Markdown
    "README.md": ".",     # Goes to root of repo
    "log": "docs",
    "overview": "docs",
    "project": "docs",
    "tableau": "docs",
    "census": "docs",
    
    # Specifications & API definitions
    "specs": "specs",
    ".yaml": "specs",
    ".yml": "specs",
    ".json": "specs",     # Default for JSON, refined by keywords
    "openapi": "specs",
    "api": "specs",
    "schema": "specs",

    # Assets (Images, etc.)
    "assets": "assets",
    ".png": "assets/images",
    ".jpg": "assets/images",
    ".jpeg": "assets/images",
    ".svg": "assets/images",
    "logo": "assets/logos",
    "style-guide.md": "assets", # Specific style guide document

    # Legal Documents
    "legal": "legal",
    "terms": "legal",
    "trademark": "legal",
    "copyright": "legal",

    # Data (for smaller, non-archival test data or specific processed outputs)
    "data": "data",
    ".csv": "data/raw",
    ".txt": "data/processed", # Assume general .txt are processed docs
    "transcript": "data/transcripts", # Specific VISTA data type
    "xls": "data/raw", # Though you're processing these, they start raw
    "xlsx": "data/raw",
    
    # Tests
    "test": "tests",

    # GitHub Workflow Configuration
    ".github": ".github", # For .github/workflows etc.
}

def get_target_subdirectory(file_path):
    """
    Determines the target subdirectory based on file extension and keywords in filename/path.
    Prioritizes specific filenames, then keywords, then extensions.
    """
    file_name_lower = file_path.name.lower()
    
    # Check for specific full filenames (e.g., Dockerfile, requirements.txt)
    if file_name_lower in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[file_name_lower]

    # Check for keywords anywhere in the file's full path (including filename)
    # Iterate over sorted items to prioritize more specific matches (e.g., 'logo' before 'assets')
    for keyword, subdir in sorted(CATEGORY_MAPPING.items(), key=lambda item: len(item[0]), reverse=True):
        if len(keyword) > 2 and keyword in file_name_lower: # Avoid very short generic keywords
            return subdir
        
    # Check for file extension mapping
    if file_path.suffix.lower() in CATEGORY_MAPPING:
        return CATEGORY_MAPPING[file_path.suffix.lower()]

    # Default to a general 'misc' folder if no match
    return "misc"

def organize_files_into_repo(source_dirs, destination_root):
    """
    Copies files from source directories to categorized subdirectories
    within the destination root.
    """
    print(f"\n--- Beginning Automated Preliminary File Organization ---")
    print(f"Source Directories: {[str(s) for s in source_dirs]}")
    print(f"Destination Root: {destination_root}")

    if not destination_root.is_dir():
        print(f"Error: Destination root directory '{destination_root}' does not exist. Please create it and clone your GitHub repo there first.")
        return

    files_processed_count = 0
    files_skipped_count = 0

    for source_dir in source_dirs:
        if not source_dir.is_dir():
            print(f"Warning: Source directory '{source_dir}' not found. Skipping.")
            continue

        print(f"\nProcessing files from: {source_dir}")
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                source_file_path = Path(root) / file_name
                
                # Determine target subdirectory
                target_subdir_name = get_target_subdirectory(source_file_path)
                
                # Handle special cases for root-level files or specific subdirectories
                if target_subdir_name == ".": # File meant for the root of the repo
                    target_dir = destination_root
                elif target_subdir_name == "app" and source_file_path.name.lower() in ["dockerfile", "requirements.txt"]:
                    target_dir = destination_root / "app" # Place in app/ for clarity
                elif target_subdir_name == ".github" and source_file_path.suffix.lower() == ".yml":
                    target_dir = destination_root / ".github" / "workflows" # Specific for GitHub Actions
                    
                # Specific rule for VISTA Transcripts based on your earlier discussions
                elif "transcript" in source_file_path.name.lower() and source_file_path.suffix.lower() == ".txt":
                    target_dir = destination_root / "data" / "Transcripts"
                
                else:
                    target_dir = destination_root / target_subdir_name

                # Ensure target directory exists
                target_dir.mkdir(parents=True, exist_ok=True)
                
                destination_file_path = target_dir / file_name

                # Compare existing files to avoid overwriting without warning
                if destination_file_path.exists():
                    source_hash = get_file_hash(str(source_file_path))
                    dest_hash = get_file_hash(str(destination_file_path))
                    if source_hash == dest_hash and source_hash is not None:
                        print(f"  Skipped (identical, already in place): {source_file_path.relative_to(source_dir)} -> {destination_file_path.relative_to(destination_root)}")
                        files_skipped_count += 1
                        continue
                    else:
                        print(f"  WARNING: File already exists with DIFFERENT content. MANUAL REVIEW REQUIRED:")
                        print(f"    Source: {source_file_path.relative_to(source_dir)}")
                        print(f"    Dest:   {destination_file_path.relative_to(destination_root)}")
                        print("  Skipping this copy to prevent accidental overwrite. Please resolve manually.")
                        files_skipped_count += 1
                        continue
                
                try:
                    shutil.copy2(source_file_path, destination_file_path)
                    print(f"  Copied: {source_file_path.relative_to(source_dir)} -> {destination_file_path.relative_to(destination_root)}")
                    files_processed_count += 1
                except Exception as e:
                    print(f"  Error copying {source_file_path}: {e}")
                    files_skipped_count += 1

    print("\n--- Preliminary Organization Complete ---")
    print(f"Files copied: {files_processed_count}")
    print(f"Files skipped (due to existing or errors): {files_skipped_count}")
    print("\nIMPORTANT: This is an *automated preliminary organization*. Manual review is CRUCIAL.")
    print("Please examine the contents of your '{destination_root}' directory carefully.")
    print("You may need to move some files to more appropriate subdirectories based on their specific purpose and context.")
    print("Also, remember to manually handle the old GitHub holographs (Step 3 in our strategy) and proceed with controlled deletion (Step 5).")


# --- NEW ADDENDUM: File Versioning and Renaming ---

def get_canonical_base_name(file_path: Path): # Corrected to expect Path object
    """
    Extracts a canonical base name from a filename by stripping common versioning suffixes.
    This helps group files that are logically the same document.
    Example: "report_v2.txt" -> "report"
             "document (1).pdf" -> "document"
             "my_script_copy.py" -> "my_script"
    """
    stem = file_path.stem # This will now work
    # Patterns for common versioning suffixes (case-insensitive)
    patterns = [
        r'[_ ]v\d+$',      # _v1, V2, _v3, etc.
        r' \(\d+\)$',      # (1), (2), etc.
        r' - Copy$',       # - Copy
        r' copy$',         # copy
        r' \(copy\)$',     # (copy)
        r'_final$',        # _final
        r'_old$',          # _old
        r'-\d{8}$'         # -YYYYMMDD style suffix (e.g., -20250620)
    ]
    
    # Repeatedly strip patterns until no more changes or no patterns apply
    original_stem = stem
    while True:
        current_stem = original_stem
        for pattern in patterns:
            # Use re.sub to remove the matched pattern
            new_stem = re.sub(pattern, '', current_stem, flags=re.IGNORECASE).strip()
            if new_stem != current_stem:
                current_stem = new_stem
                break # A pattern was applied, re-check all patterns
        if current_stem == original_stem: # No patterns applied in this pass
            break
        original_stem = current_stem
        
    return original_stem.strip()


def version_and_rename_conflicts(target_directory: Path):
    """
    Scans a directory for files that appear to be different versions of the same
    document (based on canonical base name). It sorts them by modification date
    and proposes renaming them with a _vX suffix. Requires user confirmation.
    """
    print(f"\n--- Starting File Versioning and Renaming for '{target_directory}' ---")
    if not target_directory.is_dir():
        print(f"Error: Target directory '{target_directory}' does not exist. Aborting.")
        return

    file_groups = {} # Dictionary to store groups of logically identical files
                     # Key: canonical_base_name, Value: list of (file_path_obj, mtime)

    # Step 1: Group files by their canonical base name
    for file_path in target_directory.rglob("*"): # rglob for recursive walk
        if file_path.is_file():
            canonical_name = get_canonical_base_name(file_path) # Corrected: Pass Path object
            
            # Exclude this script itself or helper scripts from versioning
            if canonical_name.lower() in ["organize_project", "file_helpers"]:
                continue

            mtime = file_path.stat().st_mtime # Last modification time
            
            if canonical_name not in file_groups:
                file_groups[canonical_name] = []
            file_groups[canonical_name].append((file_path, mtime))

    # Step 2: Process each group with more than one file
    renamed_count = 0
    for canonical_name, files_info in file_groups.items():
        if len(files_info) > 1: # Only process groups with more than one file
            print(f"\nFound potential version conflicts for: '{canonical_name}'")
            
            # Sort files in this group by modification time (oldest first)
            files_info.sort(key=lambda x: x[1])

            print("Current files (oldest to newest):")
            for i, (f_path, f_mtime) in enumerate(files_info):
                print(f"  {i+1}. {f_path.name} (Modified: {datetime.datetime.fromtimestamp(f_mtime).strftime('%Y-%m-%d %H:%M:%S')})")

            print("\nProposed renames:")
            proposed_changes = []
            for i, (old_path, _) in enumerate(files_info):
                # Check if the file already has a version suffix like _vX, but is not the correct one in sequence
                # This makes it more robust against already partially-versioned files
                current_stem_without_v = re.sub(r'[_ ]v\d+$', '', old_path.stem, flags=re.IGNORECASE).strip()
                if current_stem_without_v.lower() != canonical_name.lower():
                     # If the base stem after removing _vX doesn't match canonical_name, something is off,
                     # this case might need more complex logic or manual intervention.
                     # For simplicity, we'll force the canonical name + vX logic here.
                     pass # Fall through to the default renaming
                
                new_stem = f"{canonical_name}_v{i+1}"
                new_name = f"{new_stem}{old_path.suffix}"
                new_path = old_path.parent / new_name
                
                # Check if proposed new name is already the current name, skip if so
                if old_path.name == new_name:
                    print(f"  (No change needed for {old_path.name})")
                    continue

                proposed_changes.append((old_path, new_path))
                print(f"  - Rename '{old_path.name}' to '{new_path.name}'")
            
            if not proposed_changes:
                print("  No effective renames proposed for this group.")
                continue

            confirmation = input(f"Proceed with renaming these {len(proposed_changes)} files? (yes/no): ").strip().lower()

            if confirmation == 'yes':
                for old_path, new_path in proposed_changes:
                    try:
                        # Ensure the target name isn't already taken by another file that's not part of this group logic
                        if new_path.exists() and new_path != old_path:
                            print(f"    WARNING: Proposed new path '{new_path.name}' already exists. Skipping '{old_path.name}'. Manual intervention needed.")
                            continue

                        old_path.rename(new_path)
                        print(f"    Renamed: '{old_path.name}' -> '{new_path.name}'")
                        renamed_count += 1
                    except Exception as e:
                        print(f"    Error renaming '{old_path.name}': {e}")
            else:
                print("  Renaming cancelled for this group.")

    print(f"\n--- File Versioning and Renaming Complete. Total files renamed: {renamed_count} ---")
    print("Please review your '{target_directory}' for the changes.")


# --- Main Execution Block ---
if __name__ == "__main__":
    print("--- VISTA Project File Management Script ---")
    print("This script helps organize your project files and manage file versions.")
    print("\nWhat would you like to do?")
    print("1. Perform initial preliminary file organization (copy from OneDrive to C:\\VISTA_Project)")
    print("2. Version and rename conflicting files within C:\\VISTA_Project")
    print("3. (Advanced) Run a custom helper function directly (e.g., compare_directories)")
    print("4. Exit")

    choice = input("Enter your choice (1, 2, 3, or 4): ").strip()

    if choice == '1':
        source_directories_to_organize = [
            SOURCE_ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR,
            SOURCE_ONEDRIVE_VISTA_API_BACKEND_DIR
        ]
        organize_files_into_repo(source_directories_to_organize, DESTINATION_VISTA_PROJECT_ROOT)
    elif choice == '2':
        # Automatically target the NEW_VISTA_PROJECT_ROOT for versioning
        version_and_rename_conflicts(DESTINATION_VISTA_PROJECT_ROOT)
    elif choice == '3':
        print("\n--- Advanced Helper Function Execution ---")
        print("You can call any function from file_helpers.py directly here.")
        print("Example: compare_directories(ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR, NEW_VISTA_PROJECT_ROOT)")
        print("Or: list_files_in_directory(NEW_VISTA_PROJECT_ROOT)")
        print("Or: copy_file('C:\\source\\file.txt', 'C:\\dest\\file.txt')")
        print("Or: delete_file_with_confirmation('C:\\file\\to\\delete.txt')")
        
        try:
            # IMPORTANT: BE CAREFUL WHEN TYPING COMMANDS HERE. THIS RUNS ARBITRARY CODE.
            # Example: eval("compare_directories(ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR, NEW_VISTA_PROJECT_ROOT)")
            # You would type the function call at the prompt like:
            # compare_directories(Path(r'C:\Users\gillo\OneDrive\Documents\ChatGPT Instructions'), Path(r'C:\VISTA_Project'))
            print("\nType the function call to execute (e.g., compare_directories(ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR, NEW_VISTA_PROJECT_ROOT)):")
            advanced_command = input(">>> ")
            # Provide access to Path objects for convenience in eval
            _globals = globals()
            _globals['Path'] = Path # Make Path available in eval context
            _globals['ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR'] = SOURCE_ONEDRIVE_CHATGPT_INSTRUCTIONS_DIR # Use SOURCE_ for consistency
            _globals['NEW_VISTA_PROJECT_ROOT'] = DESTINATION_VISTA_PROJECT_ROOT # Use DESTINATION_ for consistency
            _globals['ONEDRIVE_VETERAN_ANALYTICS_DIR'] = Path(r"C:\Users\gillo\OneDrive\Documents\veteran-analytics") # Directly use Path object
            _globals['ONEDRIVE_VETERAN_ANALYTICS_BACKUP_DIR'] = Path(r"C:\Users\gillo\OneDrive\Documents\veteran-analytics - backup") # Directly use Path object
            _globals['LOCAL_ARCHIVE_DESTINATION_DIR'] = Path(r"D:\VISTA_Data_Archive") # Directly use Path object
            
            # Make the imported helper functions available in the eval context
            _globals['get_file_hash'] = get_file_hash
            _globals['list_files_in_directory'] = list_files_in_directory
            _globals['copy_file'] = copy_file
            _globals['copy_files_to_archive'] = copy_files_to_archive
            _globals['delete_file_with_confirmation'] = delete_file_with_confirmation
            _globals['compare_directories'] = compare_directories


            eval(advanced_command, _globals)
        except Exception as e:
            print(f"Error executing advanced command: {e}")
    elif choice == '4':
        print("Exiting script. Goodbye!")
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")