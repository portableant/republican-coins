import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pandas as pd

def predict_batch_of_images(model_path, image_dir, le, image_size=(128, 128)):
    """
    Loads a trained model and predicts the top 3 classes for all images in a folder.
    """
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    predictions = []
    
    # Define valid image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    # Get a list of all files in the directory
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(valid_extensions):
            image_path = os.path.join(image_dir, filename)
            
            # Load and preprocess the image
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: Could not read image {filename}. Skipping.")
                continue
            
            img = cv2.resize(img, image_size)
            img = np.array(img, dtype='float32') / 255.0
            img = np.expand_dims(img, axis=0)  # Add a batch dimension

            # Make a prediction
            preds_array = model.predict(img)
            
            # Get the indices of the top 3 predictions
            top3_indices = np.argsort(preds_array[0])[-3:][::-1]
            
            # Inverse transform the indices to get the original rrcIDs
            top3_labels = le.inverse_transform(top3_indices)
            
            # Get the corresponding confidence scores
            top3_confidences = preds_array[0][top3_indices]
            
            result_entry = {
                "filename": filename,
                "predictions": []
            }
            
            for label, confidence in zip(top3_labels, top3_confidences):
                result_entry['predictions'].append({
                    "rrcID": label,
                    "confidence": f"{confidence*100:.2f}%"
                })
            
            predictions.append(result_entry)
    
    return predictions

if __name__ == "__main__":
    # --- Configuration ---
    # Path to the saved model file
    model_path = "../models/coin_classifier_rrcID.keras"
    
    # Path to the folder containing the images you want to predict
    batch_image_folder = "../data/coins_to_classify"
    
    # Path to your original CSV file
    csv_file_path = "../data/reece1.csv"
    
    # --- Label Encoder Setup ---
    # The LabelEncoder must be fitted on the same data as during training.
    try:
        df_labels = pd.read_csv(csv_file_path)
        df_labels = df_labels.dropna(subset=['rrcID'])
        le = LabelEncoder()
        le.fit(df_labels['rrcID'])
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file_path}' was not found. Cannot load the label encoder.")
        exit()

    # --- Run Batch Prediction ---
    print(f"Starting prediction for images in '{batch_image_folder}'...")
    results = predict_batch_of_images(model_path, batch_image_folder, le)

    if results:
        print("\n--- Prediction Results ---")
        for result in results:
            print(f"File: {result['filename']}")
            for pred in result['predictions']:
                print(f"  - Predicted RRC ID: {pred['rrcID']} (Confidence: {pred['confidence']})")
            print() # Print a blank line for readability
    else:
        print("No eligible images found or predictions could not be made.")
