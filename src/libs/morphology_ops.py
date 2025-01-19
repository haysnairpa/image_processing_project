import cv2
import numpy as np

def morphological_operations(image, operation_type="dilation"):
    kernel = np.ones((5, 5), np.uint8)
    if operation_type == "dilation":
        return cv2.dilate(image, kernel, iterations=1)
    elif operation_type == "erosion":
        return cv2.erode(image, kernel, iterations=1)
    elif operation_type == "opening":
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    elif operation_type == "closing":
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image
