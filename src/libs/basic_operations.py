from PIL import Image as PILImage, ImageOps
import cv2
import numpy as np
from scipy.signal import convolve2d

def apply_grayscale(image):
    return ImageOps.grayscale(image)

def apply_negative(image):
    image = apply_grayscale(image)
    return ImageOps.invert(image)

def apply_color_manipulation(image, r_factor, g_factor, b_factor):
    img_array = np.array(image, dtype=np.float32)
    r, g, b = img_array[..., 0], img_array[..., 1], img_array[..., 2]
    r = np.clip(r * r_factor, 0, 255)
    g = np.clip(g * g_factor, 0, 255)
    b = np.clip(b * b_factor, 0, 255)
    adjusted_img = np.stack((r, g, b), axis=-1).astype(np.uint8)
    return PILImage.fromarray(adjusted_img)

def apply_scaling(image, new_width, new_height, maintain_aspect=True):    
    if maintain_aspect:
        result = image.thumbnail((new_width, new_height), PILImage.LANCZOS)  # Maintain aspect ratio
    else:
        result = image.resize((new_width, new_height), PILImage.LANCZOS)  # Ignore aspect ratio
    
    return result

def apply_translation(image, dx, dy):
    # translated_image = PILImage.new("RGB", (image.width, image.height), (0,0,0))
    # translated_image.paste(image, (dx, dy))
    # Create a new blank image with the same mode and increased size
    new_width = image.width + abs(dx)
    new_height = image.height + abs(dy)
    translated_image = PILImage.new(image.mode, (new_width, new_height))
    
    # Calculate the paste position
    paste_x = max(0, dx)
    paste_y = max(0, dy)
    
    # Paste the original image onto the new canvas
    translated_image.paste(image, (paste_x, paste_y))
    return translated_image

def apply_crop_image(image, start_row, start_col, num_rows, num_cols):
    image = np.array(image)
    if len(image.shape) == 3: # for RGB or BGR
        out = image[start_row:start_row + num_rows, start_col:start_col + num_cols, :]
    elif len(image.shape) == 2: # for grayscale image
        out = image[start_row:start_row + num_rows, start_col:start_col + num_cols]
    return PILImage.fromarray(out).astype(np.uint8)

def apply_flip(image, flip_type):
    if flip_type == "Horizontal":
        return ImageOps.mirror(image)
    elif flip_type == "Vertical":
        return ImageOps.flip(image)
    elif flip_type == "Diagonal":
        return ImageOps.mirror(ImageOps.flip(image))
    return image

def apply_rotation(image, angle):
    return image.rotate(angle, expand=True)

def apply_brightness(image, brightness_factor):
    img_array = np.array(image)
    adjusted = img_array * brightness_factor
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    return PILImage.fromarray(adjusted)

def apply_contrast(image, contrast_factor):
    img_array = np.array(image)
    mean = np.mean(img_array)
    adjusted = (img_array - mean) * contrast_factor + mean
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    return PILImage.fromarray(adjusted)

def apply_border(image, thickness, color):
    return ImageOps.expand(image, border=thickness, fill=color)

def apply_color_filter(image, filter_type):
    if filter_type == "Sepia":
        return ImageOps.colorize(image.convert("L"), "#704214", "#C0A080")
    elif filter_type == "Cyanotype":
        return ImageOps.colorize(image.convert("L"), "#002B5B", "#8CF0E8")
    return image

def apply_mean_filter(image):
    img_array = np.array(image)
    kernel = np.ones((5,5), np.float32)/25
    filtered = cv2.filter2D(img_array, -1, kernel)
    return PILImage.fromarray(filtered)

def apply_gaussian_filter(image):
    img_array = np.array(image)
    filtered = cv2.GaussianBlur(img_array, (5,5), 0)
    return PILImage.fromarray(filtered)

def apply_median_filter(image):
    img_array = np.array(image)
    filtered = cv2.medianBlur(img_array, 3)
    return PILImage.fromarray(filtered)

def apply_sobel_filter(image):
    img_array = np.array(image.convert('L'))
    sobelx = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    return PILImage.fromarray(np.uint8(magnitude))

def apply_canny_filter(image):
    img_array = np.array(image.convert('L'))
    edges = cv2.Canny(img_array, 100, 200)
    return PILImage.fromarray(edges)

def apply_laplacian_filter(image):
    img_array = np.array(image.convert('L'))
    laplacian = cv2.Laplacian(img_array, cv2.CV_64F)
    return PILImage.fromarray(np.uint8(np.absolute(laplacian)))

def apply_low_pass_filter(image, radius=30):
    img_array = np.array(image.convert('L'))
    rows, cols = img_array.shape
    crow, ccol = rows // 2, cols // 2  
    
    f_transform = np.fft.fft2(img_array)
    f_shift = np.fft.fftshift(f_transform)
    
    mask = np.zeros((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)
    
    f_shift_filtered = f_shift * mask
    f_ishift = np.fft.ifftshift(f_shift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return PILImage.fromarray(np.uint8(img_back))

def apply_high_pass_filter(image, radius=30):
    img_array = np.array(image.convert('L'))
    rows, cols = img_array.shape
    crow, ccol = rows // 2, cols // 2 
    
    f_transform = np.fft.fft2(img_array)
    f_shift = np.fft.fftshift(f_transform)
    
    mask = np.ones((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), radius, 0, thickness=-1)
    
    f_shift_filtered = f_shift * mask
    f_ishift = np.fft.ifftshift(f_shift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return PILImage.fromarray(np.uint8(img_back))

def apply_wiener_filter(image):
    kernel_size = 5
    noise_est = 25
    signal_est = 100
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)

    gray_image = apply_grayscale(image)
    img_array = np.array(gray_image)
    _, binary_image = cv2.threshold(img_array, 127, 255, cv2.THRESH_BINARY)

    blurred_image = convolve2d(binary_image, kernel, mode='same', boundary='symm')
    ratio = signal_est / (signal_est + noise_est)
    filtered_image = blurred_image * ratio
    result = np.clip(filtered_image, 0, 255).astype(np.uint8)
    return PILImage.fromarray(result)

def apply_histogram_equalization(image):
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_yuv = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    else:
        result = cv2.equalizeHist(img_array)
    return PILImage.fromarray(result)

def apply_contrast_stretching(image):
    img_array = np.array(image)
    p2, p98 = np.percentile(img_array, (2, 98))
    result = np.clip(((img_array - p2) / (p98 - p2) * 255), 0, 255).astype(np.uint8)
    return PILImage.fromarray(result)

def apply_gamma_correction(image, gamma=1.0):
    img_array = np.array(image, dtype=np.float32) / 255.0  
    corrected = np.power(img_array, gamma)
    corrected = (corrected * 255).astype(np.uint8)
    return PILImage.fromarray(corrected)

def apply_morphological_operation(image, operation_type):
    img_array = np.array(image)
    kernel = np.ones((5, 5), np.uint8)

    if len(img_array) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    if operation_type == "dilation":
        result = cv2.dilate(img_array, kernel, iterations=1)
    elif operation_type == "erosion":
        result = cv2.erode(img_array, kernel, iterations=1)
    elif operation_type == "opening":
        result = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, kernel)
    elif operation_type == "closing":
        result = cv2.morphologyEx(img_array, cv2.MORPH_CLOSE, kernel)
    else:
        return image
        
    return PILImage.fromarray(result)

