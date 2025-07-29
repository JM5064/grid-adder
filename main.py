from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import cv2
import torch

from utils import display_image, mask_blue
from number_image import NumberImage
from number_model import preprocess_image, blobify, extract_bboxes, create_number_images

from model.model import Model


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running!"


@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    print("Process image starting!", img)

    result = get_sum(img)

    return jsonify({'result': result})


def get_sum(image):
    # TODO: cache model
    model = Model()
    state = torch.load("model/runs/10epochs/best.pt")
    model.load_state_dict(state["state_dict"])
    model.eval()

    preprocessed_image = preprocess_image(image)

    blue_image = mask_blue(preprocessed_image)

    blue_image_blobified = blobify(blue_image)

    bboxes = extract_bboxes(blue_image_blobified)

    number_images = create_number_images(image, bboxes)
    total = 0
    for number_image in number_images:
        bbox_image = number_image.get_bounding_box(number_image.image)
        mnist_image = number_image.mnistify(bbox_image)

        input_image = number_image.transform_input(mnist_image)
        
        with torch.no_grad():
            output = model(input_image)

        prediction = output.argmax(1).item()

        total += prediction

        print(prediction)
        display_image(mnist_image)

    print("TOTAL:", total)
    return total
