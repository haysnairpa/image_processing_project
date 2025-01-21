import cv2
import numpy as np

def blend_images(img1_path, img2_path, alpha, beta, gamma):
    # Read the images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Resize images to be the same size if they are different
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Blend the images
    blended_img = cv2.addWeighted(img1, alpha, img2, beta, gamma)
    
    return blended_img

def overlay_images(background_path, overlay_path, alpha, x, y):
    background = cv2.imread(background_path)
    overlay = cv2.imread(overlay_path)

    if overlay.shape[0] > background.shape[0] or overlay.shape[1] > background.shape[1]:
        overlay = cv2.resize(overlay, (background.shape[1], background.shape[0]))
    
    # Split overlay into color channels and alpha channel
    overlay_b, overlay_g, overlay_r = cv2.split(overlay)
    
    # Ensure the ROI stays within background dimensions
    h, w = overlay.shape[:2]
    roi_h = min(h, background.shape[0] - y)
    roi_w = min(w, background.shape[1] - x)

    # Adjust overlay dimensions to match the ROI
    overlay_b = overlay_b[:roi_h, :roi_w]
    overlay_g = overlay_g[:roi_h, :roi_w]
    overlay_r = overlay_r[:roi_h, :roi_w]

    # Extract the corresponding ROI from the background
    roi = background[y:y + roi_h, x:x + roi_w]

    # Alpha blending
    result_b = (1.0 - alpha) * roi[:, :, 0] + alpha * overlay_b
    result_g = (1.0 - alpha) * roi[:, :, 1] + alpha * overlay_g
    result_r = (1.0 - alpha) * roi[:, :, 2] + alpha * overlay_r

    # Combine blended channels
    result = cv2.merge((result_b, result_g, result_r)).astype(np.uint8)
    # Place the blended result back into the background
    background[y:y + roi_h, x:x + roi_w] = result
    # Resize the result for display (scale down to 50%)
    scale_factor = 0.5

    return cv2.resize(background, (int(background.shape[1] * scale_factor), int(background.shape[0] * scale_factor)))
