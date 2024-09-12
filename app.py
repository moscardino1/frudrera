from flask import Flask, render_template, request, jsonify
import io
import base64
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
from config import Config
from detection import detect_objects
from recipe import recommend_recipe

app = Flask(__name__)
app.config.from_object(Config)

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
            print(ingredients)
            recipes = recommend_recipe(ingredients)
            detection_results['recommended_recipes'] = recipes
            return jsonify(detection_results)  # Return the final response as JSON

    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
