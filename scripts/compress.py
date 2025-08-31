
from PIL import Image
import os

def compress_and_save(input_img_path, output_img_path, quality):
    """
    Opens an image, compresses it to the specified quality, and saves it.
    """
    try:
        image = Image.open(input_img_path)
        image.save(output_img_path, "JPEG", quality=quality)
        print(f"Compressed: {os.path.basename(input_img_path)}")
    except Exception as e:
        print(f"Error compressing {input_img_path}: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # Set the compression quality to 75%
    quality = 75

    # Set your source and output directories
    # The output directory will be created if it doesn't exist.
    source_path = "/Users/dejp3/codeAndProjects/republican-peripleo/docs/images"
    output_path = os.path.join(source_path, "compressed_images")
    # ---------------------

    # Create the output directory if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created new directory: {output_path}")

    # List of valid image extensions to process
    valid_extensions = ('.jpg', '.jpeg', '.JPG')

    # Iterate through all files in the source directory
    for filename in os.listdir(source_path):
        # Check if the file is a valid image type
        if filename.endswith(valid_extensions):
            input_img = os.path.join(source_path, filename)
            output_img = os.path.join(output_path, filename)

            # Call the compression function
            compress_and_save(input_img, output_img, quality)

    print("\nAll eligible images have been processed.")