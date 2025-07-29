import cv2
import math
import random
import numpy as np
import time

from utils import display_image, mask_blue
from number_image import NumberImage

from model.model import Model
import torch



def get_image(file_path):
    image = cv2.imread(file_path)

    if image is None:
        print("INVALID IMAGE")

    return image


def preprocess_image(image):
    height, width, _ = image.shape
    image = cv2.resize(image, (720, 1280))
    
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    return image


def blobify(masked_image):
    # Remove noise
    kernel = np.ones((3, 3))
    masked_image = cv2.erode(masked_image, kernel)

    # Blobify
    kernel = np.ones((11, 11))
    masked_image = cv2.dilate(masked_image, kernel, iterations=3)

    return masked_image


def extract_bboxes(blobified_image):
    # Convert image to grayscale
    gray = cv2.cvtColor(blobified_image, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and collect bounding boxes
    bboxes = []
    for countour in contours:
        x, y, width, height = cv2.boundingRect(countour)
        if width > 5 and height > 5:
            bboxes.append((x, y, width, height))

    # Remove bbox most near the bottom of the image 
    bottommost_idx = max(range(len(bboxes)), key=lambda i: bboxes[i][1])
    sum_bbox = bboxes.pop(bottommost_idx)

    return bboxes


def draw_bboxes(image, bboxes):
    image_copy = image.copy()

    for x, y, width, height in bboxes:
        cv2.rectangle(image_copy, (x, y), (x + width, y + height), (0, 0, 255), 2)

    return image_copy


def create_number_images(image, bboxes) -> list[NumberImage]:
    number_images: list[NumberImage] = []

    for x, y, width, height in bboxes:
        x_end = x + width
        y_end = y + height
        cropped_image = image[y:y_end, x:x_end]

        number_image = NumberImage(cropped_image)
        number_images.append(number_image)

    return number_images


def main():
    model = Model()
    state = torch.load("model/runs/10epochs/best.pt")
    model.load_state_dict(state["state_dict"])
    model.eval()

    image = get_image("example.JPG")
    image = preprocess_image(image)
    display_image(image)

    blue_image = mask_blue(image)
    display_image(blue_image)

    blue_image_blobified = blobify(blue_image)
    display_image(blue_image_blobified)

    bboxes = extract_bboxes(blue_image_blobified)
    bbox_image = draw_bboxes(image, bboxes)
    display_image(bbox_image)

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


if __name__ == "__main__":
    main()
