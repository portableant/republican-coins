import json
import csv
import os
import time
import cloudscraper

def scrape_and_save_to_csv(base_url, output_dir, output_filename):
    """
    Paginates through a JSON API endpoint, collects all results, and saves them
    to a single CSV file in a specified directory.

    Args:
        base_url (str): The base URL of the API endpoint.
        output_dir (str): The directory to save the output file.
        output_filename (str): The name of the CSV file.
    """
    scraper = cloudscraper.create_scraper()
    all_moneyers = []
    current_page = 1
    total_pages = 1

    try:
        print(f"Starting to scrape data from {base_url}")
        
        while current_page <= total_pages:
            # Construct the URL for the current page
            url = f"{base_url}?page={current_page}"
            print(f"Fetching page {current_page} of {total_pages}...")

            # Make the request using cloudscraper
            response = scraper.get(url)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Extract data and meta information
            moneyers_data = data.get("romanRepublicanMoneyers", [])
            meta_data = data.get("meta", {})
            total_pages = meta_data.get("totalPages", 1)

            # Add the moneyers from the current page to the list
            all_moneyers.extend(moneyers_data)

            # Move to the next page
            current_page += 1
            
            # Add a small delay
            time.sleep(1)

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        if not all_moneyers:
            print("No data found to save.")
            return

        # Get the keys from the first dictionary to use as CSV headers
        csv_headers = all_moneyers[0].keys()

        # Save the combined data to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(all_moneyers)
        
        print("-" * 50)
        print(f"Successfully scraped {len(all_moneyers)} records and saved to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_url = "https://finds.org.uk/romancoins/moneyers/index/format/json"
    output_directory = "../data"
    output_filename = "roman_moneyers.csv"

    scrape_and_save_to_csv(api_url, output_directory, output_filename)