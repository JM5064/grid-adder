import cv2
import math
import random
import numpy as np
from utils import display_image, mask_blue
from number_image import NumberImage


def get_image(file_path):
    image = cv2.imread(file_path)

    if image is None:
        print("INVALID IMAGE")

    return image


def preprocess_image(image):
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    height, width, _ = image.shape
    image = cv2.resize(image, (round(width / 4), round(height / 4)))

    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    return image


def blobify(masked_image):
    # Remove noise
    kernel = np.ones((2, 2))
    masked_image = cv2.erode(masked_image, kernel)

    # Blobify
    kernel = np.ones((9, 9))
    masked_image = cv2.dilate(masked_image, kernel, iterations=2)

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
    for number_image in number_images:
        display_image(number_image.image)


if __name__ == "__main__":
    main()
