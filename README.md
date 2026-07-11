# InternGrow_AutomationSuite

Multi-Functional OS Automation Suite — Task 3 (InternGrow Python Programming Track)

## Features

### Base Features
- **Automated File Sorting** — Scans a target folder and automatically organizes
  files into sub-folders based on type (Images, Documents, Videos, Audio,
  Archives, Scripts, Logs, Others)
- **Regex-Based Text Extraction** — Scans `.txt`/`.log` files in a folder and
  extracts pattern matches (default: email addresses) into a report file

### Upgrade Feature (Unified Automation)
- Categorizes a directory by file type
- Compresses all `.log` files into a single timestamped `.zip` archive
- Fires a **desktop notification** once the automation completes
  (falls back to a console message if desktop notifications aren't
  supported on the system)

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the script:
   ```
   python automation_suite.py
   ```
3. Choose a mode:
   - **1** → Full automation (sort files + compress logs + desktop notification)
   - **2** → Regex text extraction only (enter your own pattern, or press
     Enter to use the default email-matching pattern)
4. Enter the full path of the folder you want to process
   (e.g. `C:\Users\yourname\Desktop\TestFolder`)

## Example

```
InternGrow OS Automation Suite
--------------------------------
1. Run full automation (sort files + compress logs + notify)
2. Run regex text extraction only

Enter choice (1/2): 1
Enter the folder path to process: C:\Users\faiza\Desktop\TestFolder

Step 1: Sorting files by type...
   -> 3 file(s) moved to 'Images'
   -> 2 file(s) moved to 'Documents'
   -> 1 file(s) moved to 'Logs'

Step 2: Compressing log files...
   -> Log files compressed into: logs_backup_20260710_120000.zip

Step 3: Sending completion notification...

Automation complete!
```

## Tech Used
- Python 3
- `os`, `shutil`, `re`, `zipfile`, `datetime` (standard library)
- `plyer` library (for cross-platform desktop notifications)

## Author
Built as part of the InternGrow Python Programming Track internship.

## Demo Video
(Link to be added after recording)
