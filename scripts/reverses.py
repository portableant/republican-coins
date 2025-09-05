import json
import csv
import os
import cloudscraper

def scrape_and_save_reverses(url, output_dir, output_filename):
    """
    Scrapes Roman reverses data from a single JSON endpoint, combines the
    'reverses' and 'uncommonreverses' lists, and saves the data to a CSV file.

    Args:
        url (str): The URL of the API endpoint.
        output_dir (str): The directory to save the output file.
        output_filename (str): The name of the CSV file.
    """
    scraper = cloudscraper.create_scraper()
    all_reverses = []

    try:
        print(f"Fetching data from {url}")

        # Make a single request to the URL
        response = scraper.get(url)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract and combine the two lists of reverses
        reverses_data = data.get("reverses", [])
        uncommon_reverses_data = data.get("uncommonreverses", [])
        all_reverses.extend(reverses_data)
        all_reverses.extend(uncommon_reverses_data)

        if not all_reverses:
            print("Error: No reverses data found in the JSON response.")
            return

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        # Get the keys from the first dictionary to use as CSV headers
        csv_headers = all_reverses[0].keys()

        # Save the combined data to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            writer.writerows(all_reverses)
        
        print("-" * 50)
        print(f"Successfully scraped {len(all_reverses)} records and saved to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    api_url = "https://finds.org.uk/romancoins/reversetypes/index/format/json"
    output_directory = "../data"
    output_filename = "roman_reverses.csv"

    scrape_and_save_reverses(api_url, output_directory, output_filename)