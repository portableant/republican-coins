import json
import os

def clean_json_data(data):
    """
    Recursively removes keys with null, empty string, or empty list values
    from a dictionary or list of dictionaries.
    
    Args:
        data (dict or list): The data structure to be cleaned.
        
    Returns:
        dict or list: The cleaned data structure.
    """
    if isinstance(data, dict):
        return {
            key: clean_json_data(value)
            for key, value in data.items()
            if value not in ["", None, [], {}]
        }
    elif isinstance(data, list):
        return [clean_json_data(item) for item in data if item not in ["", None, [], {}]]
    else:
        return data

# --- Main Script Execution ---
if __name__ == "__main__":
    # Define your input and output file paths here
    input_filepath = "../data/all_coins.geojson"
    output_filepath = "../data/cleaned.json"

    # Check if the input file exists
    if not os.path.exists(input_filepath):
        print(f"Error: The file '{input_filepath}' was not found.")
    else:
        try:
            # Load the JSON data from the input file
            with open(input_filepath, 'r') as f:
                data = json.load(f)
            
            # Check for the 'features' key and ensure it's a list
            if isinstance(data, dict) and "features" in data and isinstance(data["features"], list):
                # Clean the data within the 'features' array
                cleaned_features = clean_json_data(data["features"])
                
                # Update the original data structure with the cleaned features
                data["features"] = cleaned_features

                # Save the entire updated data structure to the output file
                with open(output_filepath, 'w') as f:
                    json.dump(data, f, indent=4)
                
                print(f"Successfully cleaned '{input_filepath}' and saved to '{output_filepath}'.")

            else:
                print("Error: The file does not contain the expected 'features' array within a JSON object.")

        except json.JSONDecodeError:
            print(f"Error: The file '{input_filepath}' is not a valid JSON file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")