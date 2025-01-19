import cv2

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

def overlay_images(img1_path, img2_path):
    return