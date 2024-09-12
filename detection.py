import json
import requests
from PIL import Image
import io
import base64
import os
YOLO_API_URL = os.getenv('YOLO_API_URL')
YOLO_API_KEY = os.getenv('YOLO_API_KEY')
OCR_API_KEY = os.getenv('OCR_API_KEY')
BLIP_API_URL = os.getenv('BLIP_API_URL')
BLIP_API_KEY = os.getenv('BLIP_API_KEY')
headers = {"x-api-key": YOLO_API_KEY, "Authorization": f"Bearer {BLIP_API_KEY}"}

# Function to query BLIP API for image captioning
def get_image_caption(image_bytes):
    response = requests.post(BLIP_API_URL, headers={"Authorization": f"Bearer {BLIP_API_KEY}"}, data=image_bytes)
    
    if response.status_code == 200:
        # print("BLIP API Response:", response.json())  # Print response for debugging
        
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get('generated_text', '')  # Adjust based on actual response structure
        elif isinstance(response_json, dict):
            return response_json.get('generated_text', '')
        else:
            return 'Unexpected response format'
    else:
        return 'API request failed'
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
    response = requests.post(YOLO_API_URL, headers={"x-api-key": YOLO_API_KEY}, data=data, files={"file": img_io})
    if response.status_code != 200:
        print("Ultralytics API Error:", response.text)  # Log full error message
        return {"error": "Detection failed"}

    # Parse the API response
    api_results = response.json()
    
    # Initialize objects list
    objects_list = []

    # Process the results from the API
    for image in api_results.get('images', []):
        for obj in image.get('results', []):
            box = obj.get('box', {})  # This contains the coordinates {'x1', 'x2', 'y1', 'y2'}
            label = obj.get('name', '')  # This contains the detected object's name
            confidence = obj.get('confidence', 0)  # This contains the confidence score

            # Set a confidence threshold for detection
            if confidence > 0.0001:
                # Crop the detected object from the image using the bounding box
                x1, y1, x2, y2 = box.get('x1', 0), box.get('y1', 0), box.get('x2', 0), box.get('y2', 0)
                cropped_obj = img.crop((x1, y1, x2, y2))

                # Convert the cropped object to base64 for display
                buffered = io.BytesIO()
                cropped_obj.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                # Get the caption using BLIP API
                cropped_img_io = io.BytesIO()
                cropped_obj.save(cropped_img_io, format='JPEG')
                cropped_img_bytes = cropped_img_io.getvalue()
                detected_text = get_image_caption(cropped_img_bytes)

                # Determine the specific product if OCR detects a known brand or logo
                product_label =   label

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
