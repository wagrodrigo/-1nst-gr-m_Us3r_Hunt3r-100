
import os
import sys
import json
import requests

# Objects created
WHITELIST_FILE = "whitelist.txt"
QUERY_KEYS_FILE = "keywords.txt"

base_url = "https://www.instagram.com/%s"
base_url_search = "https://www.instagram.com/web/search/topsearch/?context=blended&query=%s&rank_token=0.879513604327528&include_reel=true"

client = requests.Session()
client.headers.update({'referer': "https://www.instagram.com/instagram/"})


def load_list_from_file(filename: str) -> list:
    """Load contents of <filename> line by line to python list"""
    if os.path.isfile(filename):
        try:
            with open(filename, "r") as file_handle:
                data = [line.strip() for line in file_handle.readlines()]
                return data
        except Exception as ex:
            print(ex)
    return []   


# Whitelist load
def load_whitelist() -> list:
    return load_list_from_file(WHITELIST_FILE)


# Query_keys load
def load_query_keys() -> list:
    return load_list_from_file(QUERY_KEYS_FILE)


if __name__ == "__main__":
    query_keys = load_query_keys()

    #search using query
    for entry in query_keys:
        # receive the raw response from API
        result = client.get(base_url_search % entry).text
    
        # Convert the result to a dictionary
        result_json = json.loads(result)

    # Reading of whitelist.txt that contains que whitelist user
    whitelist_accounts = load_whitelist()

    # Comparing the result with whitelist and verified users and returning results
    for user in result_json["users"]:
        if not user["user"]["is_verified"] and user["user"]["username"] not in whitelist_accounts:
                print(base_url % user["user"]["username"])
