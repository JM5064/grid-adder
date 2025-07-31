import cv2
import numpy as np


def display_image(image):
    cv2.imshow("Image", image)

    cv2.waitKey(0)


def mask_green(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([30, 30, 20])
    upper = np.array([60, 150, 150])

    mask = cv2.inRange(hsv_image, lower, upper)

    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

    return masked_image


def mask_blue(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([90, 5, 5])
    upper = np.array([150, 240, 240])

    mask = cv2.inRange(hsv_image, lower, upper)

    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

    return masked_image


def mask_red(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    red_mask = cv2.bitwise_or(mask1, mask2)

    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=red_mask)

    return masked_image