import os
import cv2

# --- Configuration ---
# The folder where your combined coin images are located
input_folder = '../docs/data/images'
# The folder where the split images will be saved
output_folder = '../data/split_images'

# --- Main Script ---
# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created output folder: '{output_folder}'")

# Get a list of all files in the input folder
all_files = os.listdir(input_folder)

print(f"Found {len(all_files)} files in '{input_folder}'. Starting to process...")

for filename in all_files:
    # Check if the file is a common image format
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(input_folder, filename)
        
        # Read the image
        img = cv2.imread(file_path)

        # Check if the image was loaded correctly
        if img is None:
            print(f"Warning: Could not read image '{filename}'. Skipping.")
            continue
        
        # Get the dimensions of the image
        height, width, _ = img.shape
        
        # Check if the image is wide enough to be split
        if width <= 10:  # A small threshold to prevent errors on tiny files
            print(f"Warning: Image '{filename}' is too narrow to split. Skipping.")
            continue

        # Split the image into two halves
        split_point = width // 2
        obverse_img = img[:, :split_point]
        reverse_img = img[:, split_point:]
        
        # Create new filenames for the split images
        base_name, ext = os.path.splitext(filename)
        obverse_filename = f"{base_name}_obverse{ext}"
        reverse_filename = f"{base_name}_reverse{ext}"
        
        # Define the full paths to save the new images
        obverse_path = os.path.join(output_folder, obverse_filename)
        reverse_path = os.path.join(output_folder, reverse_filename)

        # Save the new images
        cv2.imwrite(obverse_path, obverse_img)
        cv2.imwrite(reverse_path, reverse_img)
        
        print(f"Successfully split and saved '{filename}' into '{obverse_filename}' and '{reverse_filename}'.")

print("\nImage splitting process complete.")
