import os
from PIL import Image

def create_mosaic(image_folder, output_path, thumbnail_size=(100, 100), cols=5):
    """
    Creates an image mosaic from all image files in a specified folder.

    Args:
        image_folder (str): The path to the folder containing the images.
        output_path (str): The path to save the final mosaic image.
        thumbnail_size (tuple): The width and height of each thumbnail in the mosaic.
        cols (int): The number of columns in the mosaic.
    """
    # Get a list of all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    # Add a check to prevent errors with empty folders
    if not image_files:
        print(f"Error: No image files found in the folder '{image_folder}'.")
        return
        
    # Calculate the number of rows needed
    num_images = len(image_files)
    rows = (num_images + cols - 1) // cols
    
    # Create a new blank canvas for the mosaic
    mosaic_width = cols * thumbnail_size[0]
    mosaic_height = rows * thumbnail_size[1]
    mosaic = Image.new('RGB', (mosaic_width, mosaic_height), 'white')
    
    print(f"Creating a mosaic with {num_images} images...")
    
    # Iterate through the images and paste them onto the mosaic
    for index, image_name in enumerate(image_files):
        try:
            image_path = os.path.join(image_folder, image_name)
            img = Image.open(image_path)
            
            # Resize the image to the thumbnail size
            img.thumbnail(thumbnail_size)
            
            # Calculate the position to paste the thumbnail
            row = index // cols
            col = index % cols
            x_offset = col * thumbnail_size[0]
            y_offset = row * thumbnail_size[1]
            
            # Paste the thumbnail onto the mosaic
            mosaic.paste(img, (x_offset, y_offset))
            
        except Exception as e:
            print(f"Could not process image '{image_name}': {e}")
            continue

    # Save the final mosaic image
    mosaic.save(output_path)
    print(f"Mosaic successfully created and saved to '{output_path}'.")

# --- Example Usage ---
if __name__ == "__main__":
    # Specify the folder with your images and the desired output path
    image_directory = "../data/compressed_images"  # Replace with the path to your folder
    output_image = "../data/mosaic.jpg"
    
    # Call the function to create the mosaic with 8 columns
    create_mosaic(image_directory, output_image, cols=15)