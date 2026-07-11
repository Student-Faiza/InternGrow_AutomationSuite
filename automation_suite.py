"""
InternGrow Python Programming Track - Task 3
Multi-Functional OS Automation Suite

Base Features:
- Automated file sorting: scans a target directory and organizes files
  into sub-folders based on their file type (extension)
- Regex-based text extraction: scans .txt/.log files in a directory and
  extracts pattern matches (e.g., emails, dates) into a report file

UPGRADE Feature:
- Unified automation: categorizes a directory by file type AND
  compresses all .log files into a single timestamped zip archive AND
  fires a desktop notification once everything is done
"""

import os
import re
import shutil
import zipfile
from datetime import datetime

try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False


# ---------- Configuration: extension -> folder name ----------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".html", ".css", ".java", ".cpp"],
    "Logs": [".log"],
}


def get_category(file_extension):
    """Return the folder category name for a given file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"


# ---------- Feature 1: Automated File Sorting ----------
def sort_files_by_type(target_dir):
    """
    Scans target_dir (non-recursively) and moves each file into a
    sub-folder named after its category (Images, Documents, Videos, etc.)
    Returns a summary dict of {category: count}.
    """
    summary = {}

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return summary

    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)

        # Skip directories - only sort files
        if os.path.isdir(file_path):
            continue

        _, extension = os.path.splitext(filename)
        category = get_category(extension)

        category_folder = os.path.join(target_dir, category)
        os.makedirs(category_folder, exist_ok=True)

        destination = os.path.join(category_folder, filename)

        # Avoid overwriting a file that already exists in the destination
        if os.path.exists(destination):
            name, ext = os.path.splitext(filename)
            destination = os.path.join(category_folder, f"{name}_copy{ext}")

        shutil.move(file_path, destination)
        summary[category] = summary.get(category, 0) + 1

    return summary


# ---------- Feature 2: Regex-Based Text Extraction ----------
def extract_patterns_from_text_files(target_dir, pattern, report_name="extraction_report.txt"):
    """
    Scans all .txt and .log files in target_dir for matches of `pattern`
    (a regex string) and writes all matches to a report file.
    """
    compiled_pattern = re.compile(pattern)
    report_path = os.path.join(target_dir, report_name)
    total_matches = 0

    with open(report_path, "w", encoding="utf-8") as report:
        for filename in os.listdir(target_dir):
            if filename.endswith((".txt", ".log")):
                file_path = os.path.join(target_dir, filename)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                except (IOError, OSError):
                    continue

                matches = compiled_pattern.findall(content)
                if matches:
                    report.write(f"--- Matches in {filename} ---\n")
                    for match in matches:
                        report.write(f"{match}\n")
                    report.write("\n")
                    total_matches += len(matches)

    return total_matches, report_path


# ---------- Feature 3 (Upgrade): Compress Log Files into a Zip Archive ----------
def compress_log_files(target_dir):
    """
    Finds all .log files inside the 'Logs' sub-folder (created by sorting)
    or directly in target_dir, and compresses them into a single
    timestamped zip archive. Returns the path to the created zip file,
    or None if there were no log files to compress.
    """
    logs_folder = os.path.join(target_dir, "Logs")
    search_dir = logs_folder if os.path.isdir(logs_folder) else target_dir

    log_files = [f for f in os.listdir(search_dir) if f.endswith(".log")]

    if not log_files:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(target_dir, f"logs_backup_{timestamp}.zip")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for log_file in log_files:
            file_path = os.path.join(search_dir, log_file)
            zipf.write(file_path, arcname=log_file)

    return zip_filename


# ---------- Feature 4 (Upgrade): Desktop Notification ----------
def send_notification(title, message):
    """Fires a desktop notification. Falls back to a console print if
    the plyer library / OS notification service is unavailable."""
    if NOTIFICATIONS_AVAILABLE:
        try:
            notification.notify(title=title, message=message, timeout=6)
            return
        except Exception:
            pass
    # Fallback: just print to console
    print(f"\n[NOTIFICATION] {title}: {message}")


# ---------- Unified Automation Workflow ----------
def run_automation_suite(target_dir):
    print("=" * 55)
    print("   INTERNGROW OS AUTOMATION SUITE")
    print("=" * 55)
    print(f"\nTarget directory: {target_dir}\n")

    # Step 1: Sort files by type
    print("Step 1: Sorting files by type...")
    summary = sort_files_by_type(target_dir)
    if summary:
        for category, count in summary.items():
            print(f"   -> {count} file(s) moved to '{category}'")
    else:
        print("   No files found to sort.")

    # Step 2: Compress log files
    print("\nStep 2: Compressing log files...")
    zip_path = compress_log_files(target_dir)
    if zip_path:
        print(f"   -> Log files compressed into: {os.path.basename(zip_path)}")
    else:
        print("   No .log files found to compress.")

    # Step 3: Desktop notification
    print("\nStep 3: Sending completion notification...")
    total_sorted = sum(summary.values())
    send_notification(
        "InternGrow Automation Suite",
        f"Done! Sorted {total_sorted} file(s)."
        + (f" Logs zipped: {os.path.basename(zip_path)}" if zip_path else "")
    )

    print("\nAutomation complete!")


def main():
    print("InternGrow OS Automation Suite")
    print("--------------------------------")
    print("1. Run full automation (sort files + compress logs + notify)")
    print("2. Run regex text extraction only")

    choice = input("\nEnter choice (1/2): ").strip()

    target_dir = input("Enter the folder path to process: ").strip()

    if choice == "1":
        run_automation_suite(target_dir)
    elif choice == "2":
        pattern = input(
            "Enter a regex pattern (or press Enter for default email pattern): "
        ).strip()
        if not pattern:
            pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        count, report_path = extract_patterns_from_text_files(target_dir, pattern)
        print(f"\nFound {count} match(es). Report saved to: {report_path}")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
