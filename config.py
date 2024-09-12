import os

class Config:
    YOLO_API_URL = os.getenv('YOLO_API_URL')
    YOLO_API_KEY = os.getenv('YOLO_API_KEY')
    OCR_API_KEY = os.getenv('OCR_API_KEY')
    BLIP_API_URL = os.getenv('BLIP_API_URL')
    BLIP_API_KEY = os.getenv('BLIP_API_KEY')
