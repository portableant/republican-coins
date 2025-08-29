import cloudscraper
import json
import pandas as pd
import time

# Create a scraper instance
# This handles the Cloudflare challenges automatically
scraper = cloudscraper.create_scraper()

# Define the base URL
url_base = 'https://finds.org.uk/database/search/results/broadperiod/ROMAN/reeceID/1/format/json'

# Set a user-agent to mimic a real browser
# Cloudscraper will add other necessary headers automatically
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

# Make the initial request and get the total number of pages
print("Fetching metadata from the first page...")
response = scraper.get(url_base, headers=headers)
json_data = json.loads(response.text)

total_results = json_data['meta']['totalResults']
results_per_page = json_data['meta']['resultsPerPage']
pagination = (total_results + results_per_page - 1) // results_per_page

print(f"Total records: {total_results}")
print(f"Total pages to scrape: {pagination}")

all_data = []

# Process the first page
records = json_data['results']
df = pd.DataFrame(records)
all_data.append(df)

# Loop through the remaining pages
for i in range(2, pagination + 1):
    url_download = f"{url_base}/page/{i}"
    print(f"Scraping page {i}/{pagination}...")
    
    try:
        response_paged = scraper.get(url_download, headers=headers)
        paged_json = json.loads(response_paged.text)
        records_paged = paged_json['results']
        df_paged = pd.DataFrame(records_paged)
        all_data.append(df_paged)
    except Exception as e:
        print(f"An error occurred on page {i}: {e}")
        time.sleep(5)
    
    time.sleep(1)

# Concatenate all dataframes and save to CSV
final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv('../data/reece1.csv', index=False, na_rep='')

print("Data successfully scraped and saved to ../data/reece1.csv")