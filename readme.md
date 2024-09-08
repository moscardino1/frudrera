# FRUDRERA - AI Recipe Recommender

## Overview
FRUDRERA is an AI-powered recipe recommender that suggests recipes based on the ingredients detected in a photo of your fridge. It utilizes object detection and OCR to identify ingredients and recommend recipes accordingly.

## Features
- Upload an image of your fridge to detect ingredients.
- Get recipe recommendations based on detected ingredients.
- View detailed recipe information including ingredients, steps, and cooking time.

## Technologies Used
- **Flask**: Web framework for building the application.
- **YOLOv5**: Object detection model for identifying ingredients.
- **EasyOCR**: Optical Character Recognition for detecting text in images.
- **FuzzyWuzzy**: For matching ingredients with recipe names.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/moscardino1/frudrera.git
   cd frudrera
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application in development mode:
python frudrera/app.py
Visit `http://127.0.0.1:5000` in your web browser to access the application.

## Deployment

To deploy the application:
1. Navigate to the `frudrera` directory:
   ```bash
   cd frudrera
   ```

2. Deploy using Vercel:
   ```bash
   vercel deploy
   ```

3. For production deployment:
   ```bash
   vercel --prod
   ```

## Additional Notes
- Ensure to add charts and results interacting with input for better user experience.
- The layout should be user-friendly for easier navigation and understanding.
- Costs and rent expenses should be monthly and autopopulated.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the contributors and libraries that made this project possible.