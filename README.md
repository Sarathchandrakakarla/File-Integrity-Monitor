File Integrity Monitor
The File Integrity Monitor is a security tool designed to ensure the integrity of files within a specified directory. It detects unauthorized modifications, deletions, or additions to files by comparing current file hash values against a stored baseline. When discrepancies are detected, it sends an email notification alerting the user to potential security issues, making it a valuable tool for safeguarding critical files.

Features
Monitors file integrity in real-time or at set intervals
Detects unauthorized changes, additions, or deletions of files
Alerts users via email with details of detected changes
Simple setup and user-friendly interface for easy integration
Requirements
Software
Operating System: Windows (recommended)
Python: Version 3.10 or compatible (if using the source files)
Python Libraries
If using the Python scripts directly, install the following libraries:

```bash
pip install tkinter smtplib
```
Email Configuration
An SMTP-enabled email account (e.g., Gmail) is required to send email notifications. Ensure the account allows SMTP connections and configure the email and password in the tool’s settings.

Directory Permissions
The tool requires read and write access to the directory being monitored to calculate file hashes and create baseline files.

Installation
Executable: Download and run FIle Integrity Monitor.exe (Windows).
Source Code: If using the source files:
Download or clone the repository.
Install the required Python packages (see above).
Configure email settings in main_code.py.
Usage
Running the Tool
```bash
python index.py
```
Run the executable or start the tool with main_code.py if using source files.
Specify the directory to be monitored.
The tool will create a baseline hash for each file in the directory.
The tool begins monitoring and alerts you via email if any file changes are detected.
Resetting the Baseline
To update the baseline for legitimate file changes, run the baseline setup again. This will replace existing baseline values with the current state of files.

File Structure
main_code.py: Main script for file monitoring and hashing.
index.py: Auxiliary script, possibly for user interface functions.
service.py: Contains service-related functions.
FIle Integrity Monitor.exe: Executable file for Windows users.
