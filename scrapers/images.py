import os
import cloudscraper
import pandas as pd
import time
from requests.exceptions import HTTPError

# Create a scraper instance to handle Cloudflare
scraper = cloudscraper.create_scraper()

# Define the base URL and the local directory for images
base_url = 'https://finds.org.uk/images/'
output_dir = 'downloaded_images'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Read the CSV file
try:
    df = pd.read_csv('reece1.csv')
    print(f"Loaded {len(df)} records from reece1.csv.")
except FileNotFoundError:
    print("Error: The file 'reece1.csv' was not found. Please ensure it's in the same directory.")
    exit()

# Initialize an empty DataFrame to store 404 errors
error_log_df = pd.DataFrame(columns=['old_findID', 'imagedir', 'filename', 'error_message'])

# Get the list of all unique image directories and filenames
images_to_download = df[['old_findID', 'imagedir', 'filename']].dropna().drop_duplicates()

print(f"Found {len(images_to_download)} unique images to download.")

# Loop through the unique image paths and download each file
for index, row in images_to_download.iterrows():
    old_findID = row['old_findID']
    imagedir = row['imagedir']
    filename = row['filename']
    
    # Construct the full image URL
    full_url = os.path.join(base_url, imagedir, filename).replace("\\", "/")

    # Define the local path to save the image
    local_path = os.path.join(output_dir, filename)

    # Skip if the file already exists
    if os.path.exists(local_path):
        print(f"Skipping: {filename} (already exists)")
        continue

    print(f"Downloading: {filename}")
    try:
        # Get the image content
        response = scraper.get(full_url, stream=True)
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Save the image to the local file
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}.")
        
    except HTTPError as e:
        if e.response.status_code == 404:
            new_row = pd.DataFrame([{'old_findID': old_findID, 'imagedir': imagedir, 'filename': filename, 'error_message': '404 - Not Found'}])
            error_log_df = pd.concat([error_log_df, new_row], ignore_index=True)
            print(f"Failed to download {filename} (404 Not Found). Logged to CSV.")
        else:
            print(f"Failed to download {filename} from {full_url}. Reason: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred with {filename}: {e}")
        
    # Be a polite scraper and add a short delay between requests
    time.sleep(1)

# Save the 404 error log to a CSV file
if not error_log_df.empty:
    error_log_df.to_csv('404_errors.csv', index=False)
    print("\n404 errors have been logged to '404_errors.csv'.")
else:
    print("\nNo 404 errors were found during the download process.")

print("\nDownload process complete.")