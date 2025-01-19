import cv2
import numpy as np

def run_length_encoding(image):
    encoded_channels = []
    for channel in cv2.split(image):
        flattened = channel.flatten()
        encoded = []
        prev_pixel = flattened[0]
        count = 1
        for pixel in flattened[1:]:
            if pixel == prev_pixel:
                count += 1
            else:
                encoded.append((prev_pixel, count))
                prev_pixel = pixel
                count = 1
        encoded.append((prev_pixel, count))
        encoded_channels.append(encoded)
    return encoded_channels

def run_length_decoding(encoded_channels, shape):
    decoded_channels = []
    for encoded in encoded_channels:
        decoded = []
        for pixel, count in encoded:
            decoded.extend([pixel] * count)
        decoded_array = np.array(decoded, dtype=np.uint8)
        decoded_channels.append(decoded_array.reshape(shape[:2]))
    return cv2.merge(decoded_channels)

def compress_image_rle(image):
    encoded = run_length_encoding(image)
    return run_length_decoding(encoded, image.shape)

def compress_image_dct(image):
    channels = cv2.split(image)
    dct_channels = []
    for channel in channels:
        dct = cv2.dct(np.float32(channel) / 255.0)
        h, w = dct.shape
        mask = np.zeros((h, w), dtype=np.float32)
        mask[:h // 4, :w // 4] = 1
        dct_simplified = dct * mask
        idct = cv2.idct(dct_simplified) * 255.0
        dct_channels.append(np.uint8(np.clip(idct, 0, 255)))
    return cv2.merge(dct_channels)
