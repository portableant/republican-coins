import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
import os

# Define the input and output filenames
input_file = '../data/reece1.csv'
output_file = '../data/geocoded.csv'

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: The file '{input_file}' was not found. Please ensure it's in the same directory.")
    exit()

# Load the data
try:
    # Use a common encoding like 'utf-8' or 'latin1'
    df = pd.read_csv(input_file, encoding='utf-8')
    print(f"Loaded {len(df)} records from '{input_file}'.")
except Exception as e:
    print(f"Error reading the CSV file: {e}")
    exit()

# Initialize the geocoder with a custom user agent
# A user agent is required by many services for proper identification
geolocator = Nominatim(user_agent="geocoding_script_for_roman_coins")

# Find records that are missing both latitude and longitude
missing_coords_df = df[(df['fourFigureLat'].isnull()) | (df['fourFigureLon'].isnull())]
print(f"Found {len(missing_coords_df)} records missing geocoordinates.")

# Check if there are records to geocode
if len(missing_coords_df) == 0:
    print("No missing coordinates to geocode. Saving the original file as 'geocoded.csv'.")
    df.to_csv(output_file, index=False)
    exit()

# Iterate through the records with missing coordinates, using knownas for parish or further details
records_geocoded = 0
for index, row in missing_coords_df.iterrows():
    parish = str(row['knownas']).strip() if pd.notnull(row['knownas']) else ''
    county = str(row['county']).strip() if pd.notnull(row['county']) else ''
    
    # Construct the query string. Adding 'United Kingdom' improves accuracy.
    query = f"{parish}, {county}, United Kingdom"

    if not parish and not county:
        print(f"Skipping record at index {index}: No parish or county information available.")
        continue

    try:
        location = geolocator.geocode(query, timeout=10)
        
        if location:
            # Update the original DataFrame with the new coordinates
            df.loc[index, 'fourFigureLat'] = location.latitude
            df.loc[index, 'fourFigureLon'] = location.longitude
            records_geocoded += 1
            print(f"Geocoded record {index+1}: Found coordinates for '{query}' - Lat: {location.latitude}, Lon: {location.longitude}")
        else:
            print(f"Could not find coordinates for '{query}'.")

    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Geocoding service error for '{query}': {e}. Retrying after a short delay.")
        time.sleep(5)  # Pause to avoid rate limiting
        location = geolocator.geocode(query) # Try one more time
        if location:
            df.loc[index, 'fourFigureLat'] = location.latitude
            df.loc[index, 'fourFigureLon'] = location.longitude
            records_geocoded += 1
            print(f"Geocoded record {index+1}: Found coordinates for '{query}' - Lat: {location.latitude}, Lon: {location.longitude}")
        else:
            print(f"Retry failed. Could not find coordinates for '{query}'.")

    # Be polite and add a short delay between requests to avoid rate limiting
    time.sleep(1)

print(f"\nGeocoding complete. Successfully geocoded {records_geocoded} records.")

# Save the final, updated DataFrame to a new CSV file
df.to_csv(output_file, index=False)
print(f"Updated data saved to '{output_file}'.")