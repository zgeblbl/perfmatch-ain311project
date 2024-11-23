import os
import requests

# GitHub API base URL for the repository
API_URL = "https://api.github.com/repos/threewisemonkeys-as/volleyball-ml/contents/data/ncaa/raw"

# Output directory
OUTPUT_DIR = "volleyball_csvs"

# Optional: Add your GitHub token for higher rate limits
GITHUB_TOKEN = None  # Replace with your token, or leave as None

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
    else:
        print(f"Failed to download {file_url} (Status: {response.status_code})")


def fetch_contents(api_url, output_dir):
    """
    Fetch directory contents using the GitHub API and download CSV files.
    """
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {api_url} (Status: {response.status_code})")
        return

    items = response.json()
    for item in items:
        if item["type"] == "dir":
            # Recursive call for subdirectories
            fetch_contents(item["url"], output_dir)
        elif item["name"].endswith(".csv"):
            # Download CSV file
            file_url = item["download_url"]
            output_path = os.path.join(output_dir, item["path"].split("/", 3)[-1])
            download_file(file_url, output_path)


# Start downloading
print("Script started...")
fetch_contents(API_URL, OUTPUT_DIR)
