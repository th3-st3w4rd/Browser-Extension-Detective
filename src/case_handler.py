import os
import platform
import subprocess

from src.supported_browsers import Chrome, Edge


class CaseHandler:
    """Manages how each case is worked."""
    def __init__(self, args):
        self.args = args
        self.results = dict()
        self.detective_machine_info = self.detect_detective_system()
        self.detective_os = self.detective_machine_info.system.lower()
        self.available_drive = self.locate_drives(self.detective_os)
        self.target_drive = args.target_drive
        self.all_accounts = args.all_users
        # print(self.target_drive)

        if self.args.chrome:
            chrome_browser = Chrome(
                online=self.args.internet,
                host_os=self.detective_os,
                all_accounts=self.all_accounts,
            )
            self.results = chrome_browser.results

    def __repr__(self):
        return str(self.results)

    @staticmethod
    def detect_detective_system():
        return platform.uname()

    @staticmethod
    def locate_drives(os_name: str):
        os_command = {
                "windows": ["fsutil", "fsinfo","drives"],
        }
        result = subprocess.run(os_command[os_name], capture_output=True, text=True)
        available_drives = result.stdout.lower().split(" ")[1:-1]
        return [drive.split(":")[0] for drive in available_drives]
