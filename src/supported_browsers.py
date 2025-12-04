import os
from pathlib import Path
from time import sleep
import logging
import platform

import requests
from bs4 import BeautifulSoup

class Browser():
    def __init__(self, online, host_os, all_accounts = False):
        self.host_os = host_os
        self.online = online
        self.results = {}
        self.all_accounts = all_accounts
        self.users_to_enumerate = list()

        if self.host_os == "windows":
            if all_accounts:
                user_path = Path(os.environ["SYSTEMDRIVE"]).joinpath("\\Users")
                exclusion_users = ["gaia", "default", "public", "all users", "default user"]
                for dir_item in os.listdir(user_path):
                    if user_path.joinpath(dir_item).is_dir() and dir_item.lower() not in exclusion_users:
                        self.users_to_enumerate.append(user_path.joinpath(dir_item))
            else:
                self.users_to_enumerate.append(Path(os.environ["USERPROFILE"]))
        else:
            raise Exception(f"'{self.host_os}' is not supported.")
    
class Chrome(Browser):
    def __init__(self, online, host_os, all_accounts):
        super().__init__(online, host_os, all_accounts)
        for user in self.users_to_enumerate:
            self.discover_chrome_extensions(user)
            print(user)

    def discover_chrome_extensions(self, user):
        logging.info("Starting 'discover_chrome_extensions'...")
        try:
            google_profile_locs = user.joinpath("AppData","Local","Google","Chrome","User Data")
            dir_items = os.listdir(google_profile_locs)
            default_location = google_profile_locs.joinpath("Default","Extensions")
            locations_to_search = [default_location]

            for item in dir_items:
                if item.startswith("Profile"):
                    locations_to_search.append(google_profile_locs.joinpath(item,"Extensions"))

            local_results = self.search_chrome_locally(locations_to_search)
            self.results[user.name] = local_results
        except Exception as e:
            logging.error(e)
    
    def search_chrome_locally(self, locations_to_search):
        logging.info("Starting 'search_chrome_locally'...")
        try:
            findings = {}
            for profiles_extensions in locations_to_search:
                lowest_exts = os.listdir(profiles_extensions)
                profile_name = profiles_extensions.parent.name
                total_exts = {}
                for lowest_ext in lowest_exts:
                    ext_name = "offline_search_only"
                    if self.online:
                        ext_name = self.search_google_web_store(lowest_ext)
                    total_exts[lowest_ext] = ext_name
                findings[profile_name] = total_exts
            return findings
        except Exception as e:
            logging.error(e)

    def search_google_web_store(self,extension_id):
        try:
            logging.info(f"Searching '{extension_id}' on Google Web Store.")
            target = f"https://chromewebstore.google.com/detail/application-launcher-for/{extension_id}"
            response = requests.get(url=target).content
            soup = BeautifulSoup(response, "lxml")
            results = soup.h1.text
            ext_name = results
            logging.info(f"Extension ID: '{extension_id}' is Extension Name: '{ext_name}'")
        except Exception as e:
            logging.debug(e)
            logging.error("Could not access this item")
            ext_name = "unknown_extension_via_online_search"
        finally:
            sleep_time = 1
            logging.info(f"Sleeping for '{sleep_time}' seconds before sending another request.")
            sleep(sleep_time)
        return ext_name
    
class Edge(Browser):
    def __init__(self, online):
        super().__init__(online)

    def search_edge_locally(self):
        #maybe this should be like a formatting.
        pass

    def search_microsoft_edge_webstore(self, extension_id):
        target = f"https://microsoftedge.microsoft.com/addons/detail/search/{extension_id}"

    def discover_edge_extension(self, online_search=False):
        # results = {}
        # if system == "windows":
        self.results.update({"windows_results":{}})
        home_env = Path(os.environ["LOCALAPPDATA"])
        edge_profile_locs = home_env.joinpath("Microsoft","Edge","User Data","Default","Extensions")
        dir_items = os.listdir(edge_profile_locs)
        print(dir_items)
        # local_results = self.search_edge_locally(edge_profile_locs, dir_items)
        # if online_search:
        #     results["windows_results"].update({"online":{}})
        #     for profile in local_results.keys():
        #         results["windows_results"]["online"].update({profile:{}})
        #         for ext_ids in local_results[profile].keys():
        #             ext_name = self.search_microsoft_edge_webstore(extension_id=ext_ids)
        #             results["windows_results"]["online"][profile].update({ext_ids:ext_name})
        # else:
        #     results["windows_results"].update({"offline": local_results})
        
        # return results
