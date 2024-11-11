import os
import hashlib
import time
from tkinter.messagebox import showerror,showinfo
import smtplib
from email.message import EmailMessage
msg = EmailMessage()
msg['Subject'] = 'Regarding Unusual Activity in Monitoring Directory by File Integrity Monitor'
msg['From'] = 'kakarlanani4@gmail.com'
msg['To'] = 'kakarlasarath4@gmail.com'
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login("kakarlanani4@gmail.com","jrfbqoiqqiukslnr")

def calculate_file_checksum(filepath):
    hash_sha512 = hashlib.sha512()
    with open(filepath, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_sha512.update(byte_block)
    return filepath, hash_sha512.hexdigest()

def remove_existing_baseline(filepath):
    if os.path.exists(filepath + '/Hash/baseline.txt'):
        os.remove(filepath + '/Hash/baseline.txt')

def collect_new_baseline(filepath):
    remove_existing_baseline(filepath)
    files = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
    if len(files) == 0:
        showerror(title="Error", message="No Files Found in the given directory to monitor")
        return False
    if not os.path.exists(filepath + "/Hash"):
        os.makedirs(filepath + "/Hash")
    with open(filepath + '/Hash/baseline.txt', 'a') as baseline_file:
        for filename in files:
            path = os.path.join(filepath, filename).replace("\\", "/")
            checksum = calculate_file_checksum(path)
            baseline_file.write(f"{checksum[0]}|{checksum[1]}\n")
        return True

def start_monitoring_files(filepath):
    file_checksum_dict = {}
    if not os.path.exists(filepath + "/Hash/baseline.txt"):
        showerror(title="Error", message="Create Hash File to Start Monitoring")
        return False

    try:
        with open(filepath + '/Hash/baseline.txt', 'r') as baseline_file:
            for line in baseline_file:
                path, checksum = line.strip().split('|')
                file_checksum_dict[path] = checksum
    except Exception as e:
        showerror(title="Error", message="Error reading baseline file: " + str(e))
        return False

    while True:
        time.sleep(1)
        current_files = {f: os.path.join(filepath, f).replace("\\", "/") for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))}
        
        # Check for new files and changes
        for filename, path in current_files.items():
            checksum = calculate_file_checksum(path)
            if path not in file_checksum_dict:
                msg.set_content("Hello Sarath, this is regarding unusual activity in your monitoring directory.\n A File has been 'Created' from the directory. Please Verify this. Thank You")
                server.send_message(msg)
                print(f"{path} has been created!")
                file_checksum_dict[path] = checksum[1]
            elif file_checksum_dict[path] != checksum[1]:
                msg.set_content("Hello Sarath, this is regarding unusual activity in your monitoring directory.\n A File has been 'Modified' from the directory. Please Verify this. Thank You")
                server.send_message(msg)
                print(f"{path} has changed!!!")

        # Check for deleted files
        for key in list(file_checksum_dict.keys()):
            if not os.path.exists(key):
                msg.set_content("Hello Sarath, this is regarding unusual activity in your monitoring directory.\n A File has been 'Deleted' from the directory. Please Verify this. Thank You")
                server.send_message(msg)
                print(f"{key} has been deleted!")
                del file_checksum_dict[key]
