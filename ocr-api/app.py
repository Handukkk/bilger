import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import tempfile
import pytesseract
import google.generativeai as genai
from PIL import Image
import cv2
from dotenv import load_dotenv
import base64
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
llm = genai.GenerativeModel('gemini-1.5-flash')

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            image_binary = img_file.read()
            base64_data = base64.b64encode(image_binary).decode("utf-8")
            return base64_data
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'hello'})

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    filename = secure_filename(image_file.filename)

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        image_path = tmp.name
        image_file.save(image_path)

    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        kernel = np.ones((1, 1), np.uint8)

        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        text = pytesseract.image_to_string(img)

        img = Image.open(image_path)
        prompt = f"""
            Convert this invoice into a VALID JSON format with:
            - "items" (array of objects with "name", "quantity", and "price")
            - "subtotal" (number)
            - "discount" (number, optional)
            - "tax" (number or null)
            - "total" (number)
            
            Rules:
            1. Use ONLY double quotes for JSON.
            2. Skip non-price info (notes, contacts).
            3. If a field is missing, set it to null.
            4. Respond ONLY with raw JSON (no code block markers, no explanations, no markdown). Do NOT include ```json or any text before/after the JSON.

            Invoice Text:
            {text}
        """
        
        response = llm.generate_content([
            prompt,
            img
        ])

    
        invoice_json = json.loads(response.text)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(image_path)

    return invoice_json, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
