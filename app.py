from flask import Flask, render_template, request, jsonify
import io
import base64
from dotenv import load_dotenv
import os
load_dotenv()
from config import Config
from detection import detect_objects
from recipe import recommend_recipe
from io import BytesIO
import qrcode

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            detection_results = detect_objects(file)
            ingredients = list(detection_results['categorized_objects'].keys())
            
            # Extract detailed ingredients including brand information
            detailed_ingredients = []
            for category, items in detection_results['categorized_objects'].items():
                for item in items:
                    detailed_ingredients.append(item['label'])
            
            recipes = recommend_recipe(detailed_ingredients)
            detection_results['recommended_recipes'] = recipes
            return jsonify(detection_results)

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')


@app.route('/donate')
def donate():
    USDT_ADDRESS = "0xDC92534Be92780c87f232CD525D99e26892E15f7"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(USDT_ADDRESS)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO object
    buffered = BytesIO()
    img.save(buffered, format="PNG")

    # Encode the image to Base64
    qr_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return render_template('donate.html', usdt_address=USDT_ADDRESS, qr_image=qr_image)


if __name__ == '__main__':
    app.run(debug=True)