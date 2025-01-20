import cv2
import numpy as np

def remove_background_threshold(myimage):
    myimage =cv2.imread(myimage)

    # Convert to Grayscale
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)

    # Apply threshold segmentation
    _, baseline = cv2.threshold(myimage_grey, 127, 255, cv2.THRESH_TRUNC)
    _, background = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY)
    _, foreground = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY_INV)

    # Update foreground with bitwise_and to extract real foreground
    foreground = cv2.bitwise_and(myimage, myimage, mask=foreground)  

    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)


    # Combine the background and foreground to obtain our final image
    finalimage = background+foreground
    finalimage = cv2.cvtColor(finalimage, cv2.COLOR_BGR2RGB)

    return finalimage

def remove_background_kmeans(myimage):
    # Read the image
    myimage = cv2.imread(myimage)
    myimage = cv2.cvtColor(myimage, cv2.COLOR_BGR2RGB)  # convert to RGB

    # Reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = myimage.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Define the criteria and number of clusters (k)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 2  

    # Apply KMeans clustering
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert centers to uint8 (pixel values)
    centers = np.uint8(centers)
    labels = labels.flatten()

    # Map labels to the center colors
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(myimage.shape)

    # Separate the clusters into foreground and background
    mask = labels.reshape(myimage.shape[:2])
    background = np.zeros_like(myimage)
    foreground = np.zeros_like(myimage)

    # Assume the cluster with the lower mean intensity is the background
    if np.mean(centers[0]) > np.mean(centers[1]):
        background[mask == 0] = [255, 255, 255]  
        foreground[mask == 1] = myimage[mask == 1]
    else:
        background[mask == 1] = [255, 255, 255]  
        foreground[mask == 0] = myimage[mask == 0]

    # Combine background and foreground to form the final image
    finalimage = background + foreground

    return finalimage
