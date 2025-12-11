import os
from pathlib import Path
from time import sleep
import logging
import platform
import json

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
    
            self.results[user.name] = self.search_chrome_locally(locations_to_search)
        except Exception as e:
            logging.error(e)
    

    def search_chrome_locally(self, locations_to_search):
        logging.info("Starting 'search_chrome_locally'...")
        try:
            final_results = {}

            for location in locations_to_search:
                profile_name = location.parent.name
                browser_type = location.parent.parent.parent.name
                if browser_type not in final_results:
                    final_results[browser_type] = {}

                ext_results = []
                for ext_id_in_filepath in location.iterdir():
                    for version_num_in_filepath in ext_id_in_filepath.iterdir():
                         
                        ext_manifest_contents = version_num_in_filepath.joinpath("manifest.json")

                        if ext_manifest_contents.exists():

                            with open(ext_manifest_contents, "r") as file:
                                try:
                                    data = json.load(file)
                                    results_object = {
                                        "ext_name": data.get("name", None),
                                        "author": data.get("author", None),
                                        "ext_id": ext_id_in_filepath.name,
                                        "description": data.get("description", None),
                                        "version": data.get("version", None),
                                        "online_info":None,
                                    }
                                    if self.online:
                                        results_object["online_info"] = self.search_google_web_store(results_object["ext_id"])
                                    ext_results.append(results_object)
                                except json.JSONDecodeError:
                                    logging.warn("Could not decode JSON")

                final_results[browser_type][profile_name] = ext_results

        except Exception as e:
            logging.error(e)

        return final_results

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
