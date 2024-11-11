import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import os
from main_code import start_monitoring_files
from tkinter.messagebox import showerror,showinfo

class FileMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FileMonitorService"
    _svc_display_name_ = "File Integrity Monitoring Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True
        showinfo(title="Test",message="Running")

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.main()

    def main(self):
        try:
            config_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'FileIntegrityMonitor')
            config_file = os.path.join(config_dir, 'monitor_config.txt')
            if not os.path.exists(config_file):
                servicemanager.LogErrorMsg("No directory configured for monitoring.")
                return

            with open(config_file, "r") as f:
                folder_to_monitor = f.read().strip()

            if not folder_to_monitor:
                servicemanager.LogErrorMsg("No directory configured for monitoring.")
                return

            while self.running:
                start_monitoring_files(folder_to_monitor)
                time.sleep(1)
        except Exception as e:
            servicemanager.LogErrorMsg(f"An error occurred while running the service: {str(e)}")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(FileMonitorService)
