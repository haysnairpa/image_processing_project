import cv2
import numpy as np

def resize_image(image1, image2):
    resized_image = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    return resized_image

def add_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img2 = resize_image(img1, img2)
    result = cv2.add(img1, img2)
    return result

def subtract_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img2 = resize_image(img1, img2)

    if len(img1.shape) == 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
    if len(img2.shape) == 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)

    result = cv2.subtract(img1, img2)
    return result

def multiply_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    img2 = resize_image(img1, img2)

    if len(img1.shape) == 2:
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
    if len(img2.shape) == 2:
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)

    result = cv2.multiply(img1, img2)
    return result

def divide_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path).astype(np.float32)
    img2 = cv2.imread(img2_path).astype(np.float32)
    img2 = resize_image(img1, img2)

    img2 += 1e-5  # Avoid division by zero
    result = cv2.divide(img1, img2)
    result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Optional: Adjust the brightness
    brightness_factor = 3  # Adjust this factor to increase brightness
    result = cv2.convertScaleAbs(result, alpha=brightness_factor, beta=0)
    return result

def bitwise_and_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    img2 = resize_image(img1, img2)
    result = cv2.bitwise_and(img1, img2)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def bitwise_or_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    img2 = resize_image(img1, img2)
    result = cv2.bitwise_or(img1, img2)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def bitwise_xor_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    img2 = resize_image(img1, img2)
    result = cv2.bitwise_xor(img1, img2)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result

def bitwise_not_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.bitwise_not(img)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    return result
