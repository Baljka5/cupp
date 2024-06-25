import os
import time
from pathlib import Path
from importlib.metadata import distributions

# Define the date you are interested in
date_of_interest = "2024-06-25"
formatted_date = time.strptime(date_of_interest, "%Y-%m-%d")

# Function to get the site-packages directory
def get_site_packages():
    # This function will return the site-packages directory based on the first found distribution
    for dist in distributions():
        return dist._path.parent

# Get the path to the site-packages directory
site_packages = get_site_packages()

# List all distributions and their metadata path
for dist in distributions():
    metadata_path = Path(dist._path, 'METADATA')
    if metadata_path.exists():
        mod_time = time.localtime(os.stat(metadata_path).st_mtime)
        if (mod_time.tm_year == formatted_date.tm_year and
            mod_time.tm_mon == formatted_date.tm_mon and
            mod_time.tm_mday == formatted_date.tm_mday):
            print(f"{dist.metadata['Name']} {dist.version} installed or updated on {date_of_interest}")
