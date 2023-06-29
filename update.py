import requests
import zipfile
import shutil
import subprocess

# Step 1: Define your current version
current_version = '1.0'

# Step 2: Get the latest release from GitHub
repo_owner = 'your_username'
repo_name = 'your_repository'
api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest'
response = requests.get(api_url)
latest_release = response.json()
latest_version = latest_release['tag_name']

# Step 3: Compare versions
if latest_version > current_version:
    # Step 4: Download the update ZIP file
    asset_url = latest_release['assets'][0]['browser_download_url']
    response = requests.get(asset_url, stream=True)
    with open('update_files.zip', 'wb') as file:
        shutil.copyfileobj(response.raw, file)

    # Step 5: Update process
    with zipfile.ZipFile('update_files.zip', 'r') as zip_ref:
        zip_ref.extractall('update_files')

    # Replace the existing files with the updated ones
    shutil.rmtree('existing_files')
    shutil.move('update_files', 'existing_files')

    # Step 6: Restart the application
    subprocess.call('python start.py', shell=True)
