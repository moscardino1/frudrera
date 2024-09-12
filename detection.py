import json
import requests
from PIL import Image
import io
import base64
import os
import logging
from fuzzywuzzy import fuzz

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

YOLO_API_URL = os.getenv('YOLO_API_URL')
YOLO_API_KEY = os.getenv('YOLO_API_KEY')
OCR_API_KEY = os.getenv('OCR_API_KEY')
BLIP_API_URL = os.getenv('BLIP_API_URL')
BLIP_API_KEY = os.getenv('BLIP_API_KEY')
OCR_API_URL = "https://api.ocr.space/parse/image"  # OCR.space API URL

headers = {"x-api-key": YOLO_API_KEY, "Authorization": f"Bearer {BLIP_API_KEY}"}

def get_image_caption(image_bytes):
    try:
        response = requests.post(BLIP_API_URL, headers={"Authorization": f"Bearer {BLIP_API_KEY}"}, data=image_bytes)
        response.raise_for_status()
        
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get('generated_text', '')
        elif isinstance(response_json, dict):
            return response_json.get('generated_text', '')
        else:
            logger.warning("Unexpected BLIP API response format")
            return 'Unexpected response format'
    except requests.RequestException as e:
        logger.error(f"BLIP API request failed: {str(e)}")
        return 'API request failed'


def perform_ocr(image_bytes):
    try:
        # Convert image bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert image to RGB mode if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save image as JPEG in memory
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        payload = {
            "apikey": OCR_API_KEY,
            "language": "eng",
            "isOverlayRequired": False,
            "iscreatesearchablepdf": False,
            "issearchablepdfhidetextlayer": False,
            "filetype": "jpg",  # Explicitly specify the file type
        }
        files = {"file": ("image.jpg", img_byte_arr, "image/jpeg")}  # Specify filename, content, and MIME type
        
        response = requests.post(OCR_API_URL, files=files, data=payload)
        response.raise_for_status()
        
        result = response.json()
        
        if result.get("IsErroredOnProcessing") == False:
            parsed_text = result.get("ParsedResults", [{}])[0].get("ParsedText", "")
            return parsed_text
        else:
            error_message = result.get("ErrorMessage", "Unknown error")
            return ""
    except requests.RequestException as e:
        return ""
    except Exception as e:
        return ""

def detect_objects(file):
    img_bytes = file.read()
    
    # Open the image and resize it if necessary
    img = Image.open(io.BytesIO(img_bytes))
    
    # Resize the image if it is larger than a specified threshold (e.g., 1024x1024 pixels)
    max_size = (1024, 1024)
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
    
    # Convert to RGB if necessary
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Save the resized image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)


    try:
        data = {
            "imgsz": 640,
            "conf": 0.25,
            "iou": 0.45
        }
        response = requests.post(YOLO_API_URL, headers={"x-api-key": YOLO_API_KEY}, data=data, files={"file": img_io})
        response.raise_for_status()
        api_results = response.json()
    except requests.RequestException as e:
        return {"error": "Object detection failed"}

    objects_list = []
    detection_count = 0

    for image in api_results.get('images', []):
        for obj in image.get('results', []):
            if detection_count >= 10:
                break
            box = obj.get('box', {})
            label = obj.get('name', '')
            confidence = obj.get('confidence', 0)

            if confidence > 0.0001:
                x1, y1, x2, y2 = box.get('x1', 0), box.get('y1', 0), box.get('x2', 0), box.get('y2', 0)
                cropped_obj = img.crop((x1, y1, x2, y2))

                buffered = io.BytesIO()
                cropped_obj.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                cropped_img_io = io.BytesIO()
                cropped_obj.save(cropped_img_io, format='JPEG')
                cropped_img_bytes = cropped_img_io.getvalue()
                
                detected_text = get_image_caption(cropped_img_bytes)
                ocr_text = perform_ocr(cropped_img_bytes)

                product_label = label

                product_label = f"{ocr_text} {label}"

                objects_list.append({
                    'label': product_label,
                    'confidence': float(confidence),
                    'cropped_image': img_str,
                    'detected_text': detected_text,
                    'ocr_text': ocr_text
                })
                print(product_label)
                detection_count += 1


    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    original_img_str = base64.b64encode(buffered.getvalue()).decode()

    categorized_objects = {}
    for obj in objects_list:
        if obj['label'] not in categorized_objects:
            categorized_objects[obj['label']] = []
        categorized_objects[obj['label']].append(obj)

    return {
        'original_image': original_img_str,
        'categorized_objects': categorized_objects
    }