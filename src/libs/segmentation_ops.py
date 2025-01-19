import cv2

def global_thresholding(image, threshold_value=127):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded_img = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresholded_img, cv2.COLOR_GRAY2BGR)

def adaptive_thresholding(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded_img = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return cv2.cvtColor(thresholded_img, cv2.COLOR_GRAY2BGR)