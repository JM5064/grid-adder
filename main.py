from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import numpy as np
import time
import cv2
import torch

from utils import display_image, mask_blue
from number_image import NumberImage
from number_model import preprocess_image, crop_bbox, blobify, extract_bboxes, create_number_images, draw_bboxes

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
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    bbox_data = data['boundingBox']

    result = get_sum(image, bbox_data)

    return jsonify({'result': result})


def get_sum(image, bbox):
    # TODO: cache model
    model = Model()
    state = torch.load("model/runs/10epochs/best.pt")
    model.load_state_dict(state["state_dict"])
    model.eval()

    print("Image dimensions:", image.shape)

    cropped_image = crop_bbox(image, bbox)

    preprocessed_image = preprocess_image(cropped_image)

    blue_image = mask_blue(preprocessed_image)

    blue_image_blobified = blobify(blue_image)

    bboxes = extract_bboxes(blue_image_blobified)
    bbox_image = draw_bboxes(preprocessed_image, bboxes)

    # cv2.imwrite(f"debug_images/preprocessed{time.time()}.png", preprocessed_image)
    # cv2.imwrite(f"debug_images/blue{time.time()}.png", blue_image)
    # cv2.imwrite(f"debug_images/blob{time.time()}.png", blue_image_blobified)
    # cv2.imwrite(f"debug_images/bbox{time.time()}.png", bbox_image)

    number_images = create_number_images(preprocessed_image, bboxes)
    total = 0
    for number_image in number_images:
        bbox_image = number_image.get_bounding_box(number_image.image)
        if bbox_image.shape[0] == 0 or bbox_image.shape[1] == 0:
            print("Bbox has invalid dimensions", bbox_image.shape)
            continue

        mnist_image = number_image.mnistify(bbox_image)
        # cv2.imwrite(f"debug_images/mnist{time.time()}.png", mnist_image)

        input_image = number_image.transform_input(mnist_image)
        
        with torch.no_grad():
            output = model(input_image)

        prediction = output.argmax(1).item()

        total += prediction


    print("TOTAL:", total)
    return total


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

