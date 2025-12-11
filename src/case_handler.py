import os
import platform

from src.supported_browsers import Chrome, Edge


class CaseHandler:
    """Manages how each case is worked."""
    def __init__(self, args):
        self.args = args
        self.results = dict()
        self.detective_machine_info = self.detect_detective_system()
        self.detective_os = self.detective_machine_info.system.lower()
        self.perp_os = None
        self.all_accounts = args.all_users

        if self.args.chrome:
            chrome_browser = Chrome(
                online=self.args.internet,
                host_os=self.detective_os,
                all_accounts=self.all_accounts,
            )
            self.results = chrome_browser.results

    def detect_detective_system(self):
        return platform.uname()

    def __repr__(self):
        return str(self.results)
