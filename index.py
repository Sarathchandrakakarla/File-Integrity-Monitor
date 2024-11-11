import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno, showinfo
import subprocess
import os
from main_code import *

dirpath = None
service_installed = False  # Check if the service has been installed

def getDir():
    global dirpath
    dirpath = askdirectory()
    setPath()

def setPath():
    global lbl
    lbl.config(text=dirpath)
    if dirpath and dirpath != "":
        baselinebtn.config(state="normal")
        monitorbtn.config(state="normal")

def CreateHashFile():
    if collect_new_baseline(dirpath):
        showinfo(title="Success", message="New Hash File Created for given directory")

def StartMonitor():
    global dirpath, service_installed

    # Ask for confirmation before starting the monitor
    if not askyesno(title="Confirmation", message="Confirm the chosen directory to proceed monitoring?"):
        return

    # Store the directory path in a config file for the service to read
    # Create the directory if it doesn't exist
    config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'FileIntegrityMonitor')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Path to the config file
    config_path = os.path.join(config_dir, 'monitor_config.txt')
    with open(config_path, "w") as f:
        f.write(dirpath)

    # Start the service if it's not already running
    if not service_installed:
        install_service()
        service_installed = True

    #start_service()
    start_monitoring_files(dirpath)

def install_service():
    # Install the service (run the service.py script with install argument)
    subprocess.run(["python", "service.py", "install"], shell=True)
    showinfo(title="Service Installed", message="Monitoring service installed successfully.")

def start_service():
    # Start the service
    subprocess.run(["python", "service.py", "start"], shell=True)
    showinfo(title="Monitoring Started", message="Monitoring service started successfully.")

root = tk.Tk()
root.iconbitmap("icon.ico")
root.title("File Integrity Monitor")
root.geometry("1500x1000")

l = Label(root, text='File Integrity Monitor', font=20, pady=20, anchor="center")
l.pack()

# Create a frame for the label and the button
label_button_frame = Frame(root)
label_button_frame.pack(pady=30)

l = Label(label_button_frame, text='Select the Folder to Monitor', font=20, anchor="w")
l.pack(side=tk.LEFT, padx=10)  # Add padding between the label and the button

btn = Button(label_button_frame, text="Select Folder", command=getDir, relief="groove", border=5, activebackground="green", background="lightgreen")
btn.pack(side=tk.LEFT, padx=10, ipadx=10)

lbl = Label(root, text='', font=3, pady=20)
lbl.pack()

# Create a frame to hold the other buttons
button_frame = Frame(root)
button_frame.pack(pady=20)

# Place buttons inside the frame, side by side
baselinebtn = Button(button_frame, text="Create New Hash File", state="disabled", command=CreateHashFile, relief="groove", border=5, activebackground="blue", background="lightblue")
baselinebtn.pack(side=tk.LEFT, padx=20)

monitorbtn = Button(button_frame, text="Start Monitoring", state="disabled", command=StartMonitor, relief="groove", border=5, activebackground="green", background="lightgreen")
monitorbtn.pack(side=tk.LEFT, padx=20)

root.mainloop()
