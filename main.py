from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
import torch

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Example torch operation
    img_tensor = torch.tensor(img).float()
    result = img_tensor.mean().item()

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # port=10000 works with render.yaml
