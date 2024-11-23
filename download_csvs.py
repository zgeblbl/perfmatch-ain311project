import os
import requests
import time
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

API_URL = "https://api.github.com/repos/threewisemonkeys-as/volleyball-ml/contents/data/ncaa/raw"
OUTPUT_DIR = "volleyball_csvs"
GITHUB_TOKEN = ""   # your token
TRACK_FILE = "downloaded_files.json"



def load_downloaded_files():
    """
    Load the list of already downloaded files from the JSON file.
    """
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'r') as f:
            return json.load(f)
    return []
def save_downloaded_file(file_path):
    """
    Save the downloaded file to the tracking list.
    """
    downloaded_files = load_downloaded_files()
    downloaded_files.append(file_path)
    with open(TRACK_FILE, 'w') as f:
        json.dump(downloaded_files, f)


def download_file(file_url, output_path):
    """
    Download a file from the given URL and save it locally.
    """
    print(f"Downloading: {file_url}")
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved: {output_path}")
        save_downloaded_file(output_path)
    else:
        print(f"Failed to download {file_url} (Status: {response.status_code})")


def fetch_contents(api_url, output_dir):
    """
    Fetch directory contents using the GitHub API and download CSV files.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Referer': 'https://www.google.com/'}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    #headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 429:  # Too many requests
        reset_time = int(response.headers.get('X-RateLimit-Reset'))
        sleep_duration = reset_time - int(time.time()) + 1
        print(f"Rate limit exceeded, sleeping for {sleep_duration} seconds.")
        time.sleep(sleep_duration)  # Sleep until rate limit resets
        return fetch_contents(api_url, output_dir)
    
    if response.status_code != 200:
        print(f"Failed to fetch {api_url} (Status: {response.status_code})")
        return

    items = response.json()
    downloaded_files = load_downloaded_files()
    
    for item in items:
        if item["type"] == "dir":
            # Recursive call for subdirectories
            fetch_contents(item["url"], output_dir)
        elif item["name"].endswith(".csv"):
            # Download CSV file
            file_url = item["download_url"]
            output_path = os.path.join(output_dir, item["path"].split("/", 3)[-1])
            if output_path not in downloaded_files:
                download_file(file_url, output_path)
            else:
                print(f"File {output_path} already downloaded, skipping.")


# Start downloading
print("Script started...")
fetch_contents(API_URL, OUTPUT_DIR)
