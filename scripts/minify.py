import json
import os

def minify_json(input_path, output_path):
    """
    Minifies a JSON file by removing all whitespace and saves it to a new file.

    Args:
        input_path (str): The path to the source JSON file.
        output_path (str): The path where the minified JSON will be saved.
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file '{input_path}' was not found.")

        # Load the JSON data from the input file
        with open(input_path, 'r') as f:
            data = json.load(f)

        # Save the data to the output file in a compact format.
        # The separators=(',', ':') removes whitespace after commas and colons.
        with open(output_path, 'w') as f:
            json.dump(data, f, separators=(',', ':'))
        
        print(f"Successfully minified '{input_path}' and saved to '{output_path}'.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError:
        print(f"Error: The file '{input_path}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main Script Execution ---
if __name__ == "__main__":
    # Define your input and output file paths here
    input_file_path = "../data/cleaned.json"
    output_file_path = "../data/all_coins.json"

    # Call the function to minify the JSON file
    minify_json(input_file_path, output_file_path)