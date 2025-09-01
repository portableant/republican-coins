import csv
import json
import requests
from io import StringIO

def fetch_and_combine_images(id_list, output_csv):
    """
    Fetches image links for a list of IDs and combines them into a single CSV.
    """
    # Base URL for the CSV data
    base_url = "https://finds.org.uk/database/search/results/rrcID/{}/format/csv"
    
    # Base URL for the images
    image_base_url = "https://republican-coins.museologi.st/images/"
    
    # List to hold all image links
    all_image_links = []
    
    print("Starting data fetching process...")
    
    # Process the list of IDs
    for rrc_id in id_list:
        # Replace 'rrc-' in the ID for URL construction
        cleaned_id = rrc_id.replace('rrc-', '')
        url = base_url.format(cleaned_id)
        
        try:
            # Fetch the CSV data from the URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Read the CSV data from the response content
            csv_data = StringIO(response.text)
            reader = csv.DictReader(csv_data)
            
            # Loop through each row and extract the filename
            for row in reader:
                filename = row.get('filename')
                if filename:
                    image_link = image_base_url + filename
                    all_image_links.append(image_link)
            
            print(f"Successfully processed ID: {rrc_id}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for ID {rrc_id}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing ID {rrc_id}: {e}")
            
    # Write the combined image links to the output CSV file
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Image Link'])
            for link in sorted(list(set(all_image_links))): # Use set to remove duplicates and sort
                writer.writerow([link])
        
        print(f"\nSuccessfully created '{output_csv}' with {len(set(all_image_links))} unique image links.")
        
    except Exception as e:
        print(f"Error writing to the output CSV file: {e}")

if __name__ == "__main__":
    # The original list of IDs
    rrc_ids = [
        'rrc-449.1', 'rrc-544.19', 'rrc-494.23', 'rrc-241.1a', 'rrc-305.1', 'rrc-237.1a', 'rrc-335.3a', 'rrc-412.1', 'rrc-363.1', 'rrc-270.1',
        'rrc-391.3', 'rrc-448.2', 'rrc-392.1b', 'rrc-449.2', 'rrc-433.1', 'rrc-544.14', 'rrc-303.1', 'rrc-348.1', 'rrc-321.1', 'rrc-448.1',
        'rrc-544.14', 'rrc-449.1', 'rrc-353.1a', 'rrc-494.21', 'rrc-473.1', 'rrc-374.1', 'rrc-299.1b', 'rrc-465.4', 'rrc-340.1', 'rrc-416.1',
        'rrc-318.1b', 'rrc-345.1', 'rrc-340.1', 'rrc-239.1', 'rrc-433.2', 'rrc-346.1', 'rrc-214.1', 'rrc-449.1a', 'rrc-281.1', 'rrc-379.2',
        'rrc-494.24', 'rrc-363.1', 'rrc-299.1b', 'rrc-383.1', 'rrc-449.4', 'rrc-523.1a', 'rrc-444.1a', 'rrc-465.2', 'rrc-354.1', 'rrc-361.1c',
        'rrc-494.36', 'rrc-440.1', 'rrc-261.1', 'rrc-407.2', 'rrc-410.1', 'rrc-317.3a', 'rrc-233.1', 'rrc-442.1a', 'rrc-259.1', 'rrc-297.1a',
        'rrc-348.3', 'rrc-285.2', 'rrc-453.1', 'rrc-415.1', 'rrc-317.3b', 'rrc-501.1', 'rrc-494.21', 'rrc-296.1', 'rrc-408.1a', 'rrc-302.1',
        'rrc-544.23', 'rrc-425.1', 'rrc-322.1b', 'rrc-394.1b', 'rrc-384.1', 'rrc-443.1', 'rrc-494.29', 'rrc-422.1b', 'rrc-261.1', 'rrc-344.1',
        'rrc-544.27', 'rrc-345.1', 'rrc-425.1', 'rrc-429.1', 'rrc-270.1', 'rrc-430.1', 'rrc-394.1a', 'rrc-345.1', 'rrc-349.1', 'rrc-494.23',
        'rrc-382.1a', 'rrc-344.2', 'rrc-449.1', 'rrc-432.1', 'rrc-494.23', 'rrc-344.2c', 'rrc-428.2', 'rrc-348.1', 'rrc-496.1', 'rrc-521.2',
        'rrc-544.21', 'rrc-334.1', 'rrc-364.1c', 'rrc-387.1', 'rrc-337.3', 'rrc-304.1', 'rrc-232.1', 'rrc-442.1a', 'rrc-410.7a', 'rrc-306.1',
        'rrc-464.2', 'rrc-385.4', 'rrc-458.1', 'rrc-341.1', 'rrc-304.1', 'rrc-425.1', 'rrc-543.1', 'rrc-494.25', 'rrc-404.1', 'rrc-394.1a',
        'rrc-439.1', 'rrc-233.1', 'rrc-286.1', 'rrc-238.1', 'rrc-393.1b', 'rrc-460.2', 'rrc-342.5b', 'rrc-386.1', 'rrc-282.4', 'rrc-485.2',
        'rrc-289.1', 'rrc-350A.1', 'rrc-544.26', 'rrc-544.36', 'rrc-544.14', 'rrc-523.1a', 'rrc-543.1', 'rrc-350A.2', 'rrc-543.1', 'rrc-517.2',
        'rrc-517.2', 'rrc-354.1', 'rrc-463.3', 'rrc-412.1', 'rrc-443.1', 'rrc-386.1', 'rrc-463.1a', 'rrc-544.27', 'rrc-544.27', 'rrc-544.1',
        'rrc-409.1', 'rrc-284.1a', 'rrc-187.1', 'rrc-270.1', 'rrc-546.6', 'rrc-465.4', 'rrc-453.1a', 'rrc-489.6', 'rrc-282.1', 'rrc-284.1a',
        'rrc-289.1', 'rrc-544.16', 'rrc-364.1a', 'rrc-413.1', 'rrc-382.1a', 'rrc-235.1a', 'rrc-540.2', 'rrc-408.1b', 'rrc-257.1', 'rrc-442.1a',
        'rrc-458.1', 'rrc-361.1a', 'rrc-443.1', 'rrc-443.1', 'rrc-39.5', 'rrc-494.23', 'rrc-423.1', 'rrc-425.1', 'rrc-425.1', 'rrc-259.1',
        'rrc-458.1', 'rrc-359.2', 'rrc-390.1', 'rrc-526.4', 'rrc-426.1', 'rrc-281.1', 'rrc-394.1b', 'rrc-425.1', 'rrc-442.1b', 'rrc-357.1b',
        'rrc-361.1a', 'rrc-480.10', 'rrc-282.1', 'rrc-431.1', 'rrc-270.1', 'rrc-273.1', 'rrc-337.3', 'rrc-284.1a', 'rrc-318.1b', 'rrc-385.2',
        'rrc-543.1', 'rrc-352.1a', 'rrc-345.1', 'rrc-496.1', 'rrc-257.1', 'rrc-474.1a', 'rrc-442.1a', 'rrc-414.1', 'rrc-494.25', 'rrc-378.1c',
        'rrc-416.1', 'rrc-528.3', 'rrc-522.4', 'rrc-285.2', 'rrc-443.1', 'rrc-405.4b', 'rrc-544.15', 'rrc-443.1', 'rrc-345.1', 'rrc-420.2',
        'rrc-342.5b', 'rrc-464.4', 'rrc-252.1', 'rrc-494.36', 'rrc-236.1a', 'rrc-273.1', 'rrc-352.1a', 'rrc-383.1', 'rrc-458.1', 'rrc-341.1',
        'rrc-544.30', 'rrc-544.30', 'rrc-433.1', 'rrc-301.1', 'rrc-413.1', 'rrc-464.5', 'rrc-391.2', 'rrc-276.1', 'rrc-526.4', 'rrc-337.3',
        'rrc-463.3', 'rrc-382.1a', 'rrc-280.1', 'rrc-394.1a', 'rrc-348.3', 'rrc-443.1', 'rrc-293.1', 'rrc-384.1', 'rrc-372.1', 'rrc-460.4',
        'rrc-236.1a', 'rrc-443.1', 'rrc-337.3', 'rrc-273.1', 'rrc-404.1', 'rrc-494.39a', 'rrc-422.1b', 'rrc-238.1', 'rrc-194.1', 'rrc-480.17',
        'rrc-215.1', 'rrc-337.3', 'rrc-415.1', 'rrc-304.1', 'rrc-313.1b', 'rrc-494.18', 'rrc-421.1', 'rrc-270.1', 'rrc-369.1', 'rrc-544.24',
        'rrc-241.1a', 'rrc-442.1a', 'rrc-255.1', 'rrc-468.1', 'rrc-382.1a', 'rrc-308.1b', 'rrc-348.1', 'rrc-206.1', 'rrc-464.3a', 'rrc-494.21',
        'rrc-544.15', 'rrc-374.2', 'rrc-316.1', 'rrc-546.2a', 'rrc-367.3', 'rrc-187.1', 'rrc-495.1', 'rrc-544.16', 'rrc-348.1', 'rrc-337.3',
        'rrc-544.19', 'rrc-299.1b', 'rrc-385.3', 'rrc-379.2', 'rrc-340.1', 'rrc-289.1', 'rrc-385.4', 'rrc-544.18', 'rrc-352.1a', 'rrc-340.1',
        'rrc-353.1a', 'rrc-442.1a', 'rrc-463.3', 'rrc-468.2', 'rrc-463.2', 'rrc-494.23', 'rrc-464.2', 'rrc-544.1', 'rrc-278.1', 'rrc-354.1',
        'rrc-302.1', 'rrc-415.1', 'rrc-278.1', 'rrc-464.4', 'rrc-453.1a', 'rrc-484.1', 'rrc-544.30', 'rrc-494.36', 'rrc-544.20', 'rrc-449.1a',
        'rrc-458.1', 'rrc-517.2', 'rrc-422.1b', 'rrc-420.1b', 'rrc-302.1', 'rrc-392.1b', 'rrc-286.1', 'rrc-544.26', 'rrc-544.18', 'rrc-544.13',
        'rrc-426.3', 'rrc-378.1a', 'rrc-385.1', 'rrc-463.3', 'rrc-444.1a', 'rrc-540.2', 'rrc-280.1', 'rrc-324.1', 'rrc-187.1', 'rrc-344.4a',
        'rrc-465.2a', 'rrc-444.1a', 'rrc-239.1', 'rrc-455.2a', 'rrc-336.1b', 'rrc-333.1', 'rrc-465.2b', 'rrc-512.2', 'rrc-406.1', 'rrc-496.1',
        'rrc-281.1', 'rrc-544.18', 'rrc-494.23', 'rrc-342.5b', 'rrc-497.3', 'rrc-443.1', 'rrc-544.20', 'rrc-458.1', 'rrc-352.1a', 'rrc-407.1',
        'rrc-219.1e', 'rrc-289.1', 'rrc-319.1', 'rrc-286.1', 'rrc-544.35', 'rrc-463.1a', 'rrc-306.1', 'rrc-544.15', 'rrc-392.1a', 'rrc-544.26',
        'rrc-544.25', 'rrc-462.1', 'rrc-544.13', 'rrc-425.1', 'rrc-544.24', 'rrc-544.32', 'rrc-464.2', 'rrc-281.1', 'rrc-286.1', 'rrc-344.4a',
        'rrc-342.5', 'rrc-386.1', 'rrc-517.2', 'rrc-383.1', 'rrc-344.1a', 'rrc-519.2', 'rrc-346.1a', 'rrc-320.1', 'rrc-342.5a', 'rrc-494.23',
        'rrc-544.20', 'rrc-379.1', 'rrc-254.1', 'rrc-364.1d', 'rrc-322.1a', 'rrc-544.25', 'rrc-449.1a', 'rrc-420.1a', 'rrc-538.1', 'rrc-317.3b',
        'rrc-299.1a', 'rrc-480.5a', 'rrc-544.35', 'rrc-544.15', 'rrc-379.1', 'rrc-443.1', 'rrc-544.31', 'rrc-362.1', 'rrc-480.8', 'rrc-544.24',
        'rrc-544.25', 'rrc-544.19', 'rrc-343.1b', 'rrc-341.2', 'rrc-316.1', 'rrc-322.1a', 'rrc-206.1', 'rrc-544.18', 'rrc-544.14', 'rrc-422.1b',
        'rrc-443.1', 'rrc-72.3', 'rrc-322.1a', 'rrc-363.1a', 'rrc-544.26', 'rrc-321.1', 'rrc-544.1', 'rrc-382.1b', 'rrc-348.2', 'rrc-412.1',
        'rrc-393.1a', 'rrc-253.1', 'rrc-388.1b', 'rrc-409.2', 'rrc-544.33', 'rrc-494.23', 'rrc-374.2', 'rrc-432.1', 'rrc-391.3', 'rrc-544.1',
        'rrc-440.1', 'rrc-393.1b', 'rrc-517.2', 'rrc-463.3', 'rrc-346.2b', 'rrc-383.1', 'rrc-426.3', 'rrc-494.21', 'rrc-480.4', 'rrc-544.19',
        'rrc-384.1', 'rrc-345.1', 'rrc-464.5', 'rrc-364.1c', 'rrc-452.2', 'rrc-394.1a', 'rrc-474.2a', 'rrc-382.1a', 'rrc-367.3', 'rrc-458.1',
        'rrc-544.16', 'rrc-385.1', 'rrc-496.1', 'rrc-274.1', 'rrc-443.1', 'rrc-544.25', 'rrc-382.1b', 'rrc-242.1', 'rrc-307.1a', 'rrc-544.37',
        'rrc-544.37', 'rrc-391.3', 'rrc-494.23', 'rrc-442.1a', 'rrc-494.39b', 'rrc-221.1', 'rrc-219.1e', 'rrc-384.1', 'rrc-350A.2', 'rrc-245.1',
        'rrc-348.2', 'rrc-348.1', 'rrc-337.3', 'rrc-544.30', 'rrc-544.8', 'rrc-202.1a', 'rrc-290.1', 'rrc-252.1', 'rrc-428.3', 'rrc-544.36',
        'rrc-458.1', 'rrc-337.3', 'rrc-353.1a', 'rrc-422.1b', 'rrc-472.2', 'rrc-422.1b', 'rrc-370.1b', 'rrc-522.1', 'rrc-494.23', 'rrc-352.1c',
        'rrc-406.1', 'rrc-543.1', 'rrc-384.1', 'rrc-265.1', 'rrc-354.3a', 'rrc-480.19', 'rrc-342.4a', 'rrc-494.40', 'rrc-300.1', 'rrc-544.31',
        'rrc-393.1a', 'rrc-416.1a', 'rrc-494.40', 'rrc-275.1', 'rrc-523.1a', 'rrc-256.1', 'rrc-238.1', 'rrc-287.1', 'rrc-281.1', 'rrc-544.30',
        'rrc-464.3c', 'rrc-497.3', 'rrc-494.38', 'rrc-311.1c', 'rrc-450.2', 'rrc-259.1', 'rrc-342.5b', 'rrc-256.1', 'rrc-270.1', 'rrc-494.21',
        'rrc-374.1', 'rrc-300.1', 'rrc-270.1', 'rrc-544.23', 'rrc-443.1', 'rrc-464.3a', 'rrc-401.1', 'rrc-416.1a', 'rrc-422.1b', 'rrc-517.2',
        'rrc-442.1a', 'rrc-544.33', 'rrc-465.1a', 'rrc-458.1', 'rrc-363.1c', 'rrc-316.1', 'rrc-197.1a', 'rrc-281.1', 'rrc-401.1', 'rrc-341.3',
        'rrc-323.1', 'rrc-443.1', 'rrc-395.1', 'rrc-507.2', 'rrc-340.1', 'rrc-544.20', 'rrc-464.5', 'rrc-284.1b', 'rrc-431.1', 'rrc-474.1a',
        'rrc-442.1a', 'rrc-284.1b', 'rrc-392.1b', 'rrc-517.2', 'rrc-433.1', 'rrc-284.1a', 'rrc-344.1b', 'rrc-362.1', 'rrc-517.2', 'rrc-511.2a',
        'rrc-526.2', 'rrc-415.1', 'rrc-448.1a', 'rrc-336.1c', 'rrc-544.15', 'rrc-544.14', 'rrc-539.1', 'rrc-455.2a', 'rrc-494.43a', 'rrc-348.1',
        'rrc-463.1a', 'rrc-343.2b', 'rrc-412.1', 'rrc-365.1a', 'rrc-367.5', 'rrc-301.1', 'rrc-279.1', 'rrc-344.3', 'rrc-308.1b', 'rrc-395.1',
        'rrc-494.23', 'rrc-341.1', 'rrc-293.1', 'rrc-311.1a', 'rrc-544.18', 'rrc-285.2', 'rrc-416.1a', 'rrc-342.4a', 'rrc-442.1b', 'rrc-342.5b',
        'rrc-275.1', 'rrc-279.1', 'rrc-544.13', 'rrc-443.1', 'rrc-286.1', 'rrc-285.2', 'rrc-453.1a', 'rrc-392.1b', 'rrc-544.15', 'rrc-335.1a',
        'rrc-464.2', 'rrc-508.3', 'rrc-443.1', 'rrc-353.1a', 'rrc-512.2', 'rrc-494.23', 'rrc-544.24', 'rrc-306.1', 'rrc-425.1', 'rrc-443.1',
        'rrc-544.20', 'rrc-448.3', 'rrc-544.13', 'rrc-480.9', 'rrc-342.5b', 'rrc-408.1a', 'rrc-335.3a', 'rrc-494.24', 'rrc-480.13', 'rrc-453.1a',
        'rrc-544.26', 'rrc-344.1a', 'rrc-544.1', 'rrc-544.19', 'rrc-545.1', 'rrc-468.1', 'rrc-544.1', 'rrc-544.25', 'rrc-337.3', 'rrc-214.1b',
        'rrc-382.1b', 'rrc-291.1', 'rrc-340.1', 'rrc-53.1', 'rrc-328.1', 'rrc-353.1a', 'rrc-495.2a', 'rrc-382.1b', 'rrc-281.1', 'rrc-544.19',
        'rrc-464.5', 'rrc-275.1', 'rrc-494.23', 'rrc-385.4', 'rrc-494.23', 'rrc-494.23', 'rrc-345.1', 'rrc-280.1', 'rrc-464.3a', 'rrc-412.1',
        'rrc-416.1a', 'rrc-282.4', 'rrc-458.1', 'rrc-544.29', 'rrc-394.1a', 'rrc-494.23', 'rrc-264.1', 'rrc-544.37', 'rrc-416.1a', 'rrc-345.1',
        'rrc-448.2a', 'rrc-415.1', 'rrc-442.1a', 'rrc-432.1', 'rrc-416.1a', 'rrc-544.14', 'rrc-428.2', 'rrc-494.25', 'rrc-494.23', 'rrc-464.2',
        'rrc-362.1', 'rrc-364.1a', 'rrc-259.1', 'rrc-464.5', 'rrc-344.3', 'rrc-341.2', 'rrc-282.4', 'rrc-544.9', 'rrc-235.1a', 'rrc-294.1',
        'rrc-53.2', 'rrc-236.1a', 'rrc-544.13', 'rrc-372.1', 'rrc-379.1', 'rrc-273.1', 'rrc-317.2', 'rrc-317.3b', 'rrc-422.1b', 'rrc-260.1',
        'rrc-544.32', 'rrc-306.1', 'rrc-361.1a', 'rrc-302.1', 'rrc-450.2', 'rrc-442.1a', 'rrc-497.3', 'rrc-415.1', 'rrc-544.38', 'rrc-324.1',
        'rrc-465.1a', 'rrc-364.1a', 'rrc-372.2', 'rrc-283.1a', 'rrc-463.3', 'rrc-337.3', 'rrc-320.1', 'rrc-372.2', 'rrc-544.1', 'rrc-431.1',
        'rrc-289.1', 'rrc-244.1', 'rrc-544.21', 'rrc-544.14', 'rrc-443.1', 'rrc-384.1', 'rrc-227.1d', 'rrc-337.2e', 'rrc-348.1', 'rrc-463.3',
        'rrc-494.23', 'rrc-383.1', 'rrc-449.1a', 'rrc-407.1', 'rrc-494.23', 'rrc-429.2a', 'rrc-364.1d', 'rrc-238.1', 'rrc-297.1a', 'rrc-289.1',
        'rrc-406.1', 'rrc-544.24', 'rrc-408.1a', 'rrc-328.1', 'rrc-422.1b', 'rrc-336.1a', 'rrc-277.1', 'rrc-393.1a', 'rrc-442.1a', 'rrc-463.3',
        'rrc-406.1', 'rrc-540.2', 'rrc-341.1', 'rrc-385.3', 'rrc-542.2', 'rrc-421.1', 'rrc-352.1a', 'rrc-468.1', 'rrc-340.1', 'rrc-263.1a',
        'rrc-449.1a', 'rrc-337.2f', 'rrc-262.1', 'rrc-379.2', 'rrc-422.1a', 'rrc-387.1', 'rrc-318.1b', 'rrc-286.1', 'rrc-231.1', 'rrc-458.1',
        'rrc-468.1', 'rrc-443.1', 'rrc-342.5b', 'rrc-507.2', 'rrc-386.1', 'rrc-364.1d', 'rrc-324.1', 'rrc-350a.2', 'rrc-424.1', 'rrc-393.1a',
        'rrc-489.6', 'rrc-416.1a', 'rrc-458.1', 'rrc-393.1a', 'rrc-442.1a', 'rrc-380.1', 'rrc-322.1b', 'rrc-544.1', 'rrc-483.2', 'rrc-448.3',
        'rrc-422.1b', 'rrc-360.1a', 'rrc-428.3', 'rrc-372.2', 'rrc-249.1', 'rrc-271.1', 'rrc-511.3a', 'rrc-449.1a', 'rrc-387.1', 'rrc-316.1',
        'rrc-350A.1a', 'rrc-311.1a', 'rrc-416.1a', 'rrc-443.1', 'rrc-276.1', 'rrc-425.1', 'rrc-367.3', 'rrc-415.1', 'rrc-281.1', 'rrc-383.1',
        'rrc-463.1a', 'rrc-353.1a', 'rrc-280.1', 'rrc-342.1', 'rrc-494.43b', 'rrc-544.27', 'rrc-468.1', 'rrc-413.1', 'rrc-464.1', 'rrc-344.1b',
        'rrc-433.1', 'rrc-544.20', 'rrc-247.1', 'rrc-380.1', 'rrc-517.2', 'rrc-281.1', 'rrc-446.1', 'rrc-328.1', 'rrc-449.2', 'rrc-494.23',
        'rrc-463.1a', 'rrc-544.14', 'rrc-544.25', 'rrc-544.36', 'rrc-308.1a', 'rrc-544.15', 'rrc-304.1', 'rrc-391.1a', 'rrc-443.1', 'rrc-544.16',
        'rrc-340.1', 'rrc-279.1', 'rrc-544.14', 'rrc-222.1', 'rrc-445.1a', 'rrc-421.1', 'rrc-480.2a', 'rrc-382.1a', 'rrc-56.3', 'rrc-479.1',
        'rrc-335.10a', 'rrc-319.1', 'rrc-462.1a', 'rrc-463.1a', 'rrc-281.1', 'rrc-341.1', 'rrc-319.1', 'rrc-443.1', 'rrc-494.23', 'rrc-204.1',
        'rrc-342.5a', 'rrc-384.1', 'rrc-443.1', 'rrc-464.1', 'rrc-343.2a', 'rrc-444.1a', 'rrc-458.1', 'rrc-458.1', 'rrc-468.1', 'rrc-494.23',
        'rrc-494.17', 'rrc-442.1b', 'rrc-385.1', 'rrc-416.1a', 'rrc-468.1', 'rrc-289.1', 'rrc-345.1', 'rrc-352.1a', 'rrc-282.4', 'rrc-448.3',
        'rrc-281.1', 'rrc-270.1', 'rrc-449.1a', 'rrc-344.3', 'rrc-342.5b', 'rrc-544.29', 'rrc-114.1', 'rrc-282.4', 'rrc-465.3', 'rrc-454.1',
        'rrc-443.1', 'rrc-354.1', 'rrc-410.1', 'rrc-330.1a', 'rrc-422.1a', 'rrc-544.18', 'rrc-544.24', 'rrc-544.27', 'rrc-390.1', 'rrc-428.1',
        'rrc-428.2', 'rrc-407.1', 'rrc-407.2', 'rrc-245.1', 'rrc-382.1a', 'rrc-379.2', 'rrc-316.1', 'rrc-443.1', 'rrc-464.2', 'rrc-544.14',
        'rrc-544.17', 'rrc-425.1', 'rrc-335.9', 'rrc-342.1', 'rrc-297.1a', 'rrc-544.39', 'rrc-443.1', 'rrc-214.1a', 'rrc-289.1', 'rrc-388.1a',
        'rrc-364.1e', 'rrc-410.8', 'rrc-393.1a', 'rrc-291.1', 'rrc-326.1', 'rrc-401.1', 'rrc-412.1', 'rrc-421.1', 'rrc-494.23', 'rrc-299.1b',
        'rrc-341.2', 'rrc-449.1a', 'rrc-487.2a', 'rrc-245.1', 'rrc-449.1b', 'rrc-443.1', 'rrc-226.1a', 'rrc-340.1', 'rrc-348.1', 'rrc-361.1c',
        'rrc-441.1', 'rrc-452.2', 'rrc-449.1a', 'rrc-494.23', 'rrc-544.21', 'rrc-544.23', 'rrc-544.27', 'rrc-544.27', 'rrc-544.36', 'rrc-544.36',
        'rrc-544.36', 'rrc-286.1', 'rrc-416.1a', 'rrc-39.4', 'rrc-480.6', 'rrc-444.1a', 'rrc-319.1', 'rrc-340.1', 'rrc-412.1', 'rrc-336.1a',
        'rrc-544.27', 'rrc-352.1a', 'rrc-382.1a', 'rrc-544.35', 'rrc-354.1', 'rrc-367.1', 'rrc-342.4a', 'rrc-458.1', 'rrc-463.1a', 'rrc-544.19',
        'rrc-544.21', 'rrc-544.26', 'rrc-544.35', 'rrc-494.23', 'rrc-464.5', 'rrc-517.2', 'rrc-443.1', 'rrc-442.1a', 'rrc-366.1a', 'rrc-544.14',
        'rrc-323.1', 'rrc-353.1d', 'rrc-544.18', 'rrc-383.1', 'rrc-412.1', 'rrc-364.1c', 'rrc-140.1', 'rrc-350a.2', 'rrc-280.1', 'rrc-486.1',
        'rrc-494.42a', 'rrc-465.5', 'rrc-282.4', 'rrc-281.1', 'rrc-340.1', 'rrc-201.1', 'rrc-407.2', 'rrc-444.1a', 'rrc-56.5', 'rrc-494.37',
        'rrc-302.1', 'rrc-319.1', 'rrc-464.5', 'rrc-341.1', 'rrc-546.2a', 'rrc-525.4c', 'rrc-374.1', 'rrc-382.1b', 'rrc-406.1', 'rrc-485.1',
        'rrc-341.1', 'rrc-443.1', 'rrc-357.1a', 'rrc-206.1', 'rrc-544.27', 'rrc-382.1a', 'rrc-512.2', 'rrc-273.1', 'rrc-57.2', 'rrc-320.1',
        'rrc-415.1', 'rrc-286.1', 'rrc-453.1a', 'rrc-291.1', 'rrc-495.2a', 'rrc-393.1a', 'rrc-313.1b', 'rrc-519.2', 'rrc-328.1', 'rrc-453.1a',
        'rrc-380.1', 'rrc-316.1', 'rrc-415.1', 'rrc-544.21', 'rrc-232.1', 'rrc-443.1', 'rrc-207.1', 'rrc-341.1', 'rrc-464.1', 'rrc-444.1a',
        'rrc-341.2', 'rrc-340.1', 'rrc-286.1', 'rrc-447.1a', 'rrc-544.1', 'rrc-412.1', 'rrc-494.23', 'rrc-544.1', 'rrc-364.1a', 'rrc-323.1',
        'rrc-337.3', 'rrc-372.1', 'rrc-544.24', 'rrc-357.1a', 'rrc-534.1', 'rrc-393.1a', 'rrc-464.5', 'rrc-463.1b', 'rrc-428.1', 'rrc-364.1d',
        'rrc-425.1', 'rrc-443.1', 'rrc-393.1a', 'rrc-463.1a', 'rrc-443.1', 'rrc-408.1a', 'rrc-393.1b', 'rrc-407.1', 'rrc-458.1', 'rrc-540.2',
        'rrc-391.2', 'rrc-544.24', 'rrc-305.1', 'rrc-453.1d', 'rrc-464.5', 'rrc-480.10', 'rrc-206.1', 'rrc-367.1', 'rrc-357.1b', 'rrc-292.1',
        'rrc-450.2', 'rrc-544.20', 'rrc-464.2', 'rrc-429.2a', 'rrc-392.1b', 'rrc-354.1', 'rrc-308.1b', 'rrc-344.2a', 'rrc-465.2b', 'rrc-544.8',
        'rrc-353.1a', 'rrc-340.1', 'rrc-520.1', 'rrc-353.1d', 'rrc-443.1', 'rrc-340.1', 'rrc-450.1a', 'rrc-335.9', 'rrc-463.1a', 'rrc-324.1',
        'rrc-461.1', 'rrc-544.19', 'rrc-494.23', 'rrc-452.2', 'rrc-386.1', 'rrc-451.1', 'rrc-314.1a', 'rrc-544.30', 'rrc-345.1', 'rrc-281.1',
        'rrc-314.1d', 'rrc-311.1c', 'rrc-463.3', 'rrc-449.1b', 'rrc-352.1a', 'rrc-544.10', 'rrc-357.1b', 'rrc-384.1', 'rrc-544.35', 'rrc-382.1b',
        'rrc-494.43b', 'rrc-341.2', 'rrc-273.1', 'rrc-443.1', 'rrc-408.1b', 'rrc-378.1c', 'rrc-285.2', 'rrc-237.1a', 'rrc-302.1', 'rrc-337.3',
        'rrc-204.1', 'rrc-458.1', 'rrc-494.23', 'rrc-454.1', 'rrc-544.30', 'rrc-337.3', 'rrc-403.1', 'rrc-544.1', 'rrc-412.1', 'rrc-380.1',
        'rrc-449.1a', 'rrc-337.3', 'rrc-495.2d', 'rrc-540.2', 'rrc-459.1', 'rrc-299.1a', 'rrc-354.1', 'rrc-473.1', 'rrc-285.1', 'rrc-303.1',
        'rrc-458.1', 'rrc-344.2a', 'rrc-494.23', 'rrc-421.1', 'rrc-448.3', 'rrc-544.35', 'rrc-468.2', 'rrc-544.35', 'rrc-511.3a', 'rrc-383.1',
        'rrc-544.21', 'rrc-519.2', 'rrc-468.1', 'rrc-544.1', 'rrc-494.23', 'rrc-544.20', 'rrc-494.30', 'rrc-544.21', 'rrc-349.1', 'rrc-494.23',
        'rrc-544.1', 'rrc-366.1a', 'rrc-274.1', 'rrc-544.31', 'rrc-340.1', 'rrc-517.2', 'rrc-544.30', 'rrc-349.1', 'rrc-341.2', 'rrc-464.5',
        'rrc-444.1a', 'rrc-203.1a', 'rrc-464.3a', 'rrc-367.3', 'rrc-250.1', 'rrc-234.1', 'rrc-352.1a', 'rrc-463.1a', 'rrc-544.37', 'rrc-286.1',
        'rrc-382.1b', 'rrc-403.1', 'rrc-393.1b', 'rrc-384.1', 'rrc-219.1d', 'rrc-291.1', 'rrc-210.1', 'rrc-474.5', 'rrc-468.1', 'rrc-250.1',
        'rrc-361.1c', 'rrc-393.1a', 'rrc-465.1a', 'rrc-459.1', 'rrc-425.1', 'rrc-262.1', 'rrc-282.4', 'rrc-405.5', 'rrc-238.1', 'rrc-382.1a',
        'rrc-372.2', 'rrc-342.5a', 'rrc-433.1', 'rrc-384.1', 'rrc-468.1', 'rrc-363.1a', 'rrc-286.1', 'rrc-454.1', 'rrc-285.1', 'rrc-344.1a',
        'rrc-433.1', 'rrc-494.38', 'rrc-285.1', 'rrc-413.1', 'rrc-517.2', 'rrc-374.1', 'rrc-345.3', 'rrc-386.1', 'rrc-431.1', 'rrc-237.1a',
        'rrc-443.1', 'rrc-494.26a', 'rrc-458.1', 'rrc-449.1a', 'rrc-296.1a', 'rrc-353.1a', 'rrc-379.2', 'rrc-462.2', 'rrc-362.1', 'rrc-516.3',
        'rrc-539.1', 'rrc-539.1', 'rrc-539.1', 'rrc-539.1', 'rrc-539.1', 'rrc-544.14', 'rrc-539.1', 'rrc-367.3', 'rrc-205.1', 'rrc-326.1',
        'rrc-361.1a', 'rrc-280.1', 'rrc-308.1b', 'rrc-289.1', 'rrc-428.3', 'rrc-289.1', 'rrc-443.1', 'rrc-425.1', 'rrc-544.32', 'rrc-232.1',
        'rrc-312.1', 'rrc-354.1', 'rrc-472.1', 'rrc-289.1', 'rrc-274.1', 'rrc-544.30', 'rrc-281.1', 'rrc-464.4', 'rrc-296.1f', 'rrc-487.1',
        'rrc-364.1d', 'rrc-298.1', 'rrc-382.1b', 'rrc-352.1b', 'rrc-537.1', 'rrc-544.14', 'rrc-304.1', 'rrc-443.1', 'rrc-383.1', 'rrc-458.1',
        'rrc-510.1', 'rrc-345.1', 'rrc-361.1a', 'rrc-316.1', 'rrc-348.1', 'rrc-292.1', 'rrc-415.1', 'rrc-382.1b', 'rrc-274.1', 'rrc-333.1',
        'rrc-348.1', 'rrc-427.1', 'rrc-442.1a', 'rrc-345.1', 'rrc-494.38', 'rrc-422.1b', 'rrc-443.1', 'rrc-348.2', 'rrc-383.1', 'rrc-337.2a',
        'rrc-409.1', 'rrc-443.1', 'rrc-442.1a', 'rrc-544.24', 'rrc-344.2b', 'rrc-462.1a', 'rrc-350A.2', 'rrc-458.1', 'rrc-449.1a', 'rrc-461.1',
        'rrc-365.1a', 'rrc-286.1', 'rrc-337.3', 'rrc-237.1b', 'rrc-423.1', 'rrc-464.2', 'rrc-340.1', 'rrc-415.1', 'rrc-363.1d', 'rrc-453.1d',
        'rrc-158.1', 'rrc-344.2a', 'rrc-370.1a', 'rrc-422.1b', 'rrc-393.1a', 'rrc-544.19', 'rrc-253.1', 'rrc-282.1', 'rrc-340.1', 'rrc-472.1',
        'rrc-353.1c', 'rrc-343.1b', 'rrc-408.1a', 'rrc-238.1', 'rrc-217.1', 'rrc-544.36', 'rrc-422.1a', 'rrc-285.1', 'rrc-465.3', 'rrc-290.1',
        'rrc-321.1', 'rrc-300.1', 'rrc-344.1b', 'rrc-422.1b', 'rrc-361.1a', 'rrc-286.1', 'rrc-511.4a', 'rrc-442.1a', 'rrc-136.1', 'rrc-239.1',
        'rrc-544.29', 'rrc-407.1', 'rrc-544.15', 'rrc-204.1', 'rrc-433.1', 'rrc-443.1', 'rrc-458.1', 'rrc-462.1a', 'rrc-544.36', 'rrc-300.1',
        'rrc-422.1a', 'rrc-342.5b', 'rrc-473.2a', 'rrc-523.1a', 'rrc-450.1a', 'rrc-337.3', 'rrc-422.1a', 'rrc-544.1', 'rrc-247.1', 'rrc-216.1',
        'rrc-285.2', 'rrc-414.1', 'rrc-544.1', 'rrc-422.1a', 'rrc-244.1', 'rrc-426.4a', 'rrc-235.1a', 'rrc-306.1', 'rrc-468.1', 'rrc-480.3',
        'rrc-500.3', 'rrc-342.1', 'rrc-257.1', 'rrc-494.23', 'rrc-458.1'
    ]
    
    # Run the function
    output_file = "../data/republican_coin_images.csv"
    fetch_and_combine_images(rrc_ids, output_file)
