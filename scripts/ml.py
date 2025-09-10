import os
import cv2
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models

def load_images_and_labels(image_dir, df, image_size=(128, 128), target_column='rrcID'):
    """
    Loads and preprocesses images, matching them to labels from a DataFrame.
    
    Args:
        image_dir (str): Path to the directory containing images.
        df (pd.DataFrame): DataFrame with coin data and filenames.
        image_size (tuple): Desired size for resizing images.
        target_column (str): The column in the DataFrame to use for labels.
    
    Returns:
        tuple: A tuple containing (images_array, labels_array, label_encoder).
    """
    images = []
    labels = []
    
    df['filename_base'] = df['filename'].str.lower().str.replace('.jpg', '').str.replace('.jpeg', '')
    label_map = df.set_index('filename_base')[target_column].to_dict()

    for img_filename in os.listdir(image_dir):
        if '_obverse' in img_filename.lower() or '_reverse' in img_filename.lower():
            base_filename = img_filename.split('_')[0].lower()
            
            if base_filename in label_map:
                label = label_map[base_filename]
                
                if pd.isna(label):
                    continue

                img_path = os.path.join(image_dir, img_filename)
                
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                    img = cv2.resize(img, image_size)
                    images.append(img)
                    labels.append(label)
                except Exception as e:
                    print(f"Could not load image {img_filename}: {e}")
    
    images = np.array(images, dtype='float32') / 255.0
    labels = np.array(labels)
    
    return images, labels

def build_cnn_model(input_shape, num_classes):
    """
    Builds a CNN model for multi-class classification.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
                  
    return model

if __name__ == "__main__":
    # --- Configuration ---
    image_directory = "../data/split_images"
    csv_file_path = "../data/reece1.csv"
    model_output_path = "../models/coin_classifier_rrcID.keras"

    # --- Data Preprocessing and Loading ---
    try:
        df_labels = pd.read_csv(csv_file_path)
        df_labels = df_labels.dropna(subset=['rrcID'])
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file_path}' was not found.")
        exit()

    le = LabelEncoder()
    # Fit the encoder on the entire 'rrcID' column before dropping any data
    le.fit(df_labels['rrcID'])
    
    # Now, load images and map to the encoded labels
    X, y_labels = load_images_and_labels(image_directory, df_labels, target_column='rrcID')
    
    if len(X) == 0:
        print("No images found or loaded. Please check your data directory and filename format.")
        exit()
    
    # Transform the loaded labels to their numerical representation
    y_encoded = le.transform(y_labels)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # --- Model Building and Training ---
    input_shape = X_train[0].shape
    # Use the number of classes from the fitted LabelEncoder
    num_classes = len(le.classes_) 
    
    model = build_cnn_model(input_shape, num_classes)
    
    print("Starting model training...")
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
    
    # --- Evaluation and Saving ---
    print("\nEvaluating model on test data...")
    loss, accuracy = model.evaluate(X_test, y_test, verbose=2)
    print(f"\nTest Accuracy: {accuracy*100:.2f}%")

    model.save(model_output_path)
    print(f"\nModel saved to '{model_output_path}'")
    
    label_mapping = dict(zip(le.transform(le.classes_), le.classes_))
    print("\nLabel Mapping:", label_mapping)
