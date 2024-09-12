import json
import requests
from PIL import Image
import io
import base64
import numpy as np

# Load configuration
with open('config.json') as f:
    config = json.load(f)

YOLO_API_URL = config['YOLO_API_URL']
YOLO_API_KEY = config['YOLO_API_KEY']
OCR_API_KEY = config['OCR_API_KEY']  # Add your OCR.space API key to config
OCR_API_URL = 'https://api.ocr.space/parse/image'

headers = {"x-api-key": YOLO_API_KEY}

# Function to perform OCR using OCR.space API
def perform_ocr(image_bytes):
    ocr_headers = {
        'apikey': OCR_API_KEY
    }
    ocr_data = {
        'isOverlayRequired': 'false',
        'language': 'eng'
    }
    response = requests.post(OCR_API_URL, headers=ocr_headers, data=ocr_data, files={'file': image_bytes})
    
    if response.status_code != 200:
        return []  # Handle error or return empty list

    ocr_results = response.json()
    text_detected = []
    for result in ocr_results.get('ParsedResults', []):
        text_detected.append(result['ParsedText'])
    return text_detected

# Function to detect objects using Ultralytics API
def detect_objects(file):
    # Read the image bytes
    img_bytes = file.read()

    # Save the image temporarily in memory to send as a file
    img = Image.open(io.BytesIO(img_bytes))

    # Convert RGBA to RGB to avoid errors when saving as JPEG
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')  # Save image as JPEG after conversion
    img_io.seek(0)

    # Ultralytics API request for object detection
    data = {
        "imgsz": 640,   # Image size for YOLOv5 model
        "conf": 0.25,   # Confidence threshold
        "iou": 0.45     # Intersection over Union threshold
    }

    # Sending request to the Ultralytics API
    response = requests.post(YOLO_API_URL, headers=headers, data=data, files={"file": img_io})

    # Check if the API call was successful
    if response.status_code != 200:
        return {"error": "Detection failed"}

    # Parse the API response
    api_results = response.json()
    
    # Initialize objects list
    objects_list = []

    # Process the results from the API
    for image in api_results['images']:
        for obj in image['results']:
            box = obj['box']  # This contains the coordinates {'x1', 'x2', 'y1', 'y2'}
            label = obj['name']   
            confidence = obj['confidence']   

            # Set a confidence threshold for detection
            if confidence > 0.0001:
                # Crop the detected object from the image using the bounding box
                x1, y1, x2, y2 = box['x1'], box['y1'], box['x2'], box['y2']
                cropped_obj = img.crop((x1, y1, x2, y2))

                # Convert the cropped object to base64 for display
                buffered = io.BytesIO()
                cropped_obj.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # Perform OCR on the cropped object using OCR.space
                buffered.seek(0)  # Reset buffer position
                ocr_result = perform_ocr(buffered)

                # Extract the most probable text from OCR result
                detected_text = ' '.join(ocr_result)  # Combine all detected texts

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
