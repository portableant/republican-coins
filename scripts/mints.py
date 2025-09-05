import json
import csv
import os
import cloudscraper

def scrape_and_save_mints(url, output_dir, output_filename):
    """
    Scrapes Roman mint data from a single JSON endpoint and saves it to a CSV file.

    Args:
        url (str): The URL of the API endpoint.
        output_dir (str): The directory to save the output file.
        output_filename (str): The name of the CSV file.
    """
    scraper = cloudscraper.create_scraper()
    
    try:
        print(f"Fetching data from {url}")

        # Make a single request to the URL
        response = scraper.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the list of mints from the "mints" key
        mints_data = data.get("mints", [])

        if not mints_data:
            print("Error: No mints data found in the JSON response.")
            return

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        # Get the keys from the first dictionary to use as CSV headers
        csv_headers = mints_data[0].keys()

        # Save the data to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(mints_data)
        
        print("-" * 50)
        print(f"Successfully scraped {len(mints_data)} records and saved to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_url = "https://finds.org.uk/romancoins/mints/index/format/json"
    output_directory = "../data"
    output_filename = "roman_mints.csv"

    scrape_and_save_mints(api_url, output_directory, output_filename)