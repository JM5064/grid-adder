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
    # image = cv2.resize(image, (720, 1280))
    
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    alpha = 1.25  # Contrast control (1.0-3.0)
    beta = 0     # Brightness control (0-100)

    img_contrast = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Convert to HSV color space
    hsv = cv2.cvtColor(img_contrast, cv2.COLOR_BGR2HSV)

    # Split channels
    h, s, v = cv2.split(hsv)

    # Increase saturation
    s = np.clip(s * 1.5, 0, 255).astype(np.uint8)  # 1.5x saturation

    # Merge channels back
    hsv_vibrant = cv2.merge([h, s, v])

    # Convert back to BGR
    img_vibrant = cv2.cvtColor(hsv_vibrant, cv2.COLOR_HSV2BGR)

    print("Image preprocessed", image.shape)

    return img_vibrant


def crop_bbox(image, bbox):
    height, width, _ = image.shape

    # Convert normalized coordinates to pixel coordinates
    x = int(bbox['x'] * width)
    y = int(bbox['y'] * height)
    w = int(bbox['width'] * width)
    h = int(bbox['height'] * height)

    # Make sure bbox is not out of bounds
    x_end = min(x + w, width)
    y_end = min(y + h, height)

    return image[y:y_end, x:x_end]


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
    MIN_SIZE = 5
    MAX_SIZE = 500
    for countour in contours:
        x, y, width, height = cv2.boundingRect(countour)
        if MIN_SIZE < width < MAX_SIZE and MIN_SIZE < height < MAX_SIZE:
            bboxes.append((x, y, width, height))

    return bboxes


def draw_bboxes(image, bboxes):
    image_copy = image.copy()

    for x, y, width, height in bboxes:
        cv2.rectangle(image_copy, (x, y), (x + width, y + height), (0, 0, 255), 2)

    return image_copy


def create_number_images(image, bboxes) -> list[NumberImage]:
    number_images: list[NumberImage] = []

    for x, y, width, height in bboxes:
        if width == 0 or height == 0:
            print("Invalid number image dimensions", width, height)
            continue

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
