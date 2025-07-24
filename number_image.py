import cv2
import numpy as np
import math
from utils import display_image, mask_blue
from torchvision.transforms import v2
import time


class NumberImage:

    def __init__(self, image):
        self.image = self.preprocess(image)

        height, width = self.image.shape
        self.aspect_ratio = width / height

    
    def preprocess(self, image):
        # Get blue pixels
        blue_image = mask_blue(image)

        # Convert to grayscale
        grayscale_image = cv2.cvtColor(blue_image, cv2.COLOR_BGR2GRAY)

        # Apply binary threshold
        _, binary_image = cv2.threshold(grayscale_image, 1, 255, cv2.THRESH_BINARY)

        # Thiccify
        kernel = np.ones((2, 2))
        dilated_image = cv2.dilate(binary_image, kernel, iterations=2)

        blurred_image = cv2.blur(dilated_image, (3, 3))

        return blurred_image
        

    def get_bounding_box(self, image):
        # Find all white (foreground) pixels
        coords = np.argwhere(image >= 10)

        x, y, width, height = cv2.boundingRect(coords)

        return image[x:x+width, y:y+height]
    

    def mnistify(self, image):
        height, width = image.shape

        # Apply letterbox crop with max size 20 x 20
        image_size = 28
        number_size = 20
        scale = number_size / max(width, height)

        new_width = math.ceil(width * scale)
        new_height = math.ceil(height * scale)

        resized_image = cv2.resize(image, (new_width, new_height))

        # Finish letterbox crop padding and add 4 pixel padding on all sides to make 28 x 28
        pad_top = (image_size - new_height) // 2
        pad_bottom = image_size - new_height - pad_top
        pad_left = (image_size - new_width) // 2
        pad_right = image_size - new_width - pad_left

        mnist_image = cv2.copyMakeBorder(resized_image, pad_top, pad_bottom, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT)

        return mnist_image
    

    def transform_input(self, mnist_image):
        transform = v2.Compose([
            v2.Resize((28, 28)),
            v2.ToTensor(),
            v2.Normalize(mean=[0.1307], std=[0.3081]),
        ])

        input_image = transform(mnist_image).unsqueeze(0)

        return input_image
    

    