from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
import torch

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"


@app.route('/process', methods=['POST'])
def process_image():
    print("Process image starting!")
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Example torch operation
    img_tensor = torch.tensor(img).float()
    result = img_tensor.mean().item()

    return jsonify({'result': 1})
