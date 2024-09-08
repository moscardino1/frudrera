import torch
from PIL import Image
import io
import base64
import easyocr
import numpy as np
import os 

import time
from urllib.error import HTTPError
import gc
gc.collect()
def load_model_with_retry(max_retries=3, delay=5):
    model_path = os.path.join(os.path.dirname(__file__), 'yolov5m.pt')
    
    for attempt in range(max_retries):
        try:
            if os.path.exists(model_path):
                # Load from local file if it exists
                model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False)
            else:
                # Download and save the model if it doesn't exist locally
                model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, trust_repo=True)
                torch.save(model.state_dict(), model_path)
            return model
        except HTTPError as e:
            if e.code == 403 and attempt < max_retries - 1:
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise

# Use the function to load the model
try:
    model = load_model_with_retry()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {str(e)}")


# Initialize OCR for detecting brand logos or text
ocr_reader = easyocr.Reader(['en'])  # Add more languages if needed

def detect_objects(file):
    # Read and process the image
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # Perform object detection with YOLO
    results = model(img)

    # Process YOLO results
    detected_objects = results.pandas().xyxy[0]
    objects_list = []

    # Loop through detected objects
    for _, obj in detected_objects.iterrows():
        x1, y1, x2, y2 = obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax']
        label = obj['name']
        confidence = obj['confidence']

        # Set a confidence threshold for YOLO detection
        if confidence > 0.0001:
            # Crop the detected object from the image
            cropped_obj = img.crop((x1, y1, x2, y2))
            
            # Convert the cropped object to base64 for display
            buffered = io.BytesIO()
            cropped_obj.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Perform OCR on the cropped object to detect logos or brand names
            cropped_np = np.array(cropped_obj)
            ocr_result = ocr_reader.readtext(cropped_np)

            # Extract the most probable text from OCR result
            detected_text = ''
            if ocr_result:
                detected_text = ocr_result[0][1]  # Get the first OCR result (most confident)

            # Determine the specific product if OCR detects a known brand or logo
            product_label = detected_text.lower() + ' ' + label

            # Append the detected object to the objects list
            objects_list.append({
                'label': product_label,
                'confidence': float(confidence),
                'cropped_image': img_str,
                'detected_text': detected_text  # For debugging/logging purposes
            })

    # Convert the original image to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    original_img_str = base64.b64encode(buffered.getvalue()).decode()

    # Categorize and order objects for display
    categorized_objects = {}
    for obj in objects_list:
        if obj['label'] not in categorized_objects:
            categorized_objects[obj['label']] = []
        categorized_objects[obj['label']].append(obj)

    return {
        'original_image': original_img_str,
        'categorized_objects': categorized_objects
    }