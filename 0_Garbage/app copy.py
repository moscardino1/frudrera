from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
from torchvision import transforms
from transformers import ViTImageProcessor, ViTForImageClassification
import io
import random
import base64
import numpy as np
import easyocr

torch.cuda.empty_cache()

app = Flask(__name__)

# Load YOLOv5 model for object detection
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# Load pre-trained food image classifier from Hugging Face
food_model_name = "google/vit-base-patch16-224"
food_image_processor = ViTImageProcessor.from_pretrained(food_model_name)
food_classifier_model = ViTForImageClassification.from_pretrained(food_model_name)
food_classifier_model.eval()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Define a dictionary of common ingredients and their synonyms
ingredient_synonyms = {
    "tomato": ["tomatoes", "red tomato", "cherry tomato"],
    # ... (other ingredients)
}

# Define a list of common food brands
common_brands = [
    "Barilla", "Heinz", "Kraft", "Nestle", "Kellogg's",
    # ... (other brands)
]

def detect_objects(image_data):
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    results = yolo_model(img)
    detected_objects = []
    for det in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = det.tolist()
        if conf > 0.5:
            label = yolo_model.names[int(cls)]
            crop = img.crop((x1, y1, x2, y2))
            img_base64 = image_to_base64(crop)
            detected_objects.append((label, conf, img_base64))
    return detected_objects

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def classify_ingredient(image_base64):
    img = base64_to_image(image_base64)
    inputs = food_image_processor(images=img, return_tensors="pt")
    with torch.no_grad():
        outputs = food_classifier_model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class_idx = probabilities.argmax().item()
    class_label = food_classifier_model.config.id2label[predicted_class_idx]
    probability = probabilities[0, predicted_class_idx].item()
    return class_label, probability

def base64_to_image(image_base64):
    image_data = base64.b64decode(image_base64)
    return Image.open(io.BytesIO(image_data)).convert("RGB")

def detect_brand(image_base64):
    img = base64_to_image(image_base64)
    img_np = np.array(img)
    results = reader.readtext(img_np)
    detected_brands = []
    for (bbox, text, conf) in results:
        text = text.lower()
        for brand in common_brands:
            if brand.lower() in text:
                detected_brands.append((brand, conf))
    if detected_brands:
        detected_brands.sort(key=lambda x: x[1], reverse=True)
        return detected_brands[0][0], detected_brands[0][1]
    return None, 0.0

def find_best_match(detected_foods):
    italian_dishes = {
        "Pasta al Pomodoro": ["pasta", "tomato", "sauce"],
        # ... (other dishes)
    }
    best_match = None
    max_score = 0
    for dish, ingredients in italian_dishes.items():
        score = sum(
            1 for food, _, _ in detected_foods
            for ingredient in ingredients
            if food.lower() == ingredient or any(synonym == food.lower() for synonym in ingredient_synonyms.get(ingredient, []))
        )
        if score > max_score:
            max_score = score
            best_match = dish
    return best_match or random.choice(list(italian_dishes.keys()))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            image_data = file.read()
            detected_objects = detect_objects(image_data)
            classified_items = []
            for obj, conf, img_base64 in detected_objects:
                ingredient, ing_prob = classify_ingredient(img_base64)
                brand, brand_prob = detect_brand(img_base64)
                classified_items.append((f"{brand} {obj}" if brand else ingredient, max(brand_prob, ing_prob), img_base64))
            recipe = find_best_match(classified_items)
            return render_template('result.html', recipe=recipe, ingredients=classified_items)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
