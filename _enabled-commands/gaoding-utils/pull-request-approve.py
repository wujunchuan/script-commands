#!/usr/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title gd pull-request approve
# @raycast.mode fullOutput
# @raycast.packageName Raycast Scripts
#
# Optional parameters:
# @raycast.icon 🤖
# @raycast.currentDirectoryPath ~
# @raycast.needsConfirmation false
# @#raycast.argument1 { "type": "text", "placeholder": "Pull Request ID" }
#
# Documentation:
# @raycast.description 自我实现 pull request 的 approve
# @raycast.author John Trump
# @raycast.authorURL https://github.com/wujunchuan

import sys
from pathlib import Path
from urllib.parse import urlparse, quote
from http.client import HTTPSConnection

def read_env_file(env_path):
    """Read .env file and return a dictionary of environment variables."""
    env_vars = {}
    try:
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading .env file: {e}")
        sys.exit(1)
    return env_vars

def load_token():
    # Get the directory of the current script
    script_dir = Path(__file__).parent.parent.parent
    print(f"Script directory: {script_dir}")
    env_path = script_dir / '.env.local'
    
    if not env_path.exists():
        print("Error: .env.local file not found")
        sys.exit(1)
        
    env_vars = read_env_file(env_path)
    token = env_vars.get('GITLAB_TOKEN')
    print(f"Token: {token}")
    if not token:
        print("Error: GITLAB_TOKEN not found in .env.local")
        sys.exit(1)
    return token

def main():
    if len(sys.argv) != 2:
        print("Usage: python pull-request-approve.py <pull_request_url>")
        sys.exit(1)

    """ Parse query string """
    clipboard_content = sys.argv[1]
    parsed_url = urlparse(clipboard_content)
    path_parts = parsed_url.path.split("/")
    project_id = path_parts[1] + quote("/", safe='') + path_parts[2]
    merge_request_iid = path_parts[5]
    # print(f"Project ID: {project_id}")
    # print(f"Merge Request IID: {merge_request_iid}")
    if project_id == "" or merge_request_iid == "":
        print("Invalid URL format. Please provide a valid merge request URL.")
        sys.exit(1)

    """ Post the Approve Merge Request """
    api_host = "git.intra.gaoding.com"
    api_path = f"/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/approve"
    headers = {
        "Accept": "application/json",
        "PRIVATE-TOKEN": f"{load_token()}",
        "Content-Type": "application/json",
    }

    try:
        conn = HTTPSConnection(api_host)
        conn.request("POST", api_path, headers=headers)
        response = conn.getresponse()
        if response.status == 201:
            print("Merge request approved successfully.")
        else:
            print(f"Request failed with status code {response.status}")
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
