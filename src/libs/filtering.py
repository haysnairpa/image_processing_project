import flet as ft
import cv2
import numpy as np
import os
import time

def main(page: ft.Page):
    page.title = "Image Processing App - Transforms and Filtering"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = "always"

    # Create the "images" folder if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    original_image_path = None  # Store the path of the original uploaded image
    current_image_path = None  # Store the path of the current image
    previous_image_path = None  # Store the path of the previous image for undo functionality

    def on_upload(e):
        nonlocal original_image_path, current_image_path, previous_image_path
        if file_picker.result is not None and file_picker.result.files is not None:
            if len(file_picker.result.files) > 0:
                uploaded_file = file_picker.result.files[0]
                original_image_path = uploaded_file.path  # Save the path of the original image
                current_image_path = uploaded_file.path  # Initialize current image as original image
                previous_image_path = None  # Reset previous image path
                image.src = uploaded_file.path
                page.update()

    def reset_image(e):
        nonlocal current_image_path, previous_image_path
        if original_image_path:
            image.src = original_image_path  # Revert to the original image
            current_image_path = original_image_path  # Reset current image path
            previous_image_path = None  # Reset previous image path
            page.update()

    # Apply Fourier Transform (DFT/FFT)
    def apply_fourier_transform(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            f_transform = np.fft.fft2(img)
            f_shift = np.fft.fftshift(f_transform)  # Shift zero frequency to center
            magnitude_spectrum = 20 * np.log(np.abs(f_shift))  # Magnitude spectrum
            result = np.asarray(magnitude_spectrum, dtype=np.uint8)
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_fft_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # Apply Mean Filter
    def apply_mean_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path)
            kernel_mean = np.ones((5, 5), np.float32) / 25  # 5x5 mean kernel
            result = cv2.filter2D(img, -1, kernel_mean)  # Apply mean filter
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_mean_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    # Apply Gaussian Filter
    def apply_gaussian_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path)
            result = cv2.GaussianBlur(img, (5, 5), sigmaX=1)  # Apply Gaussian filter
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_gaussian_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # Apply Median Filter
    def apply_median_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path)
            result = cv2.medianBlur(img, 3)  # Apply median filter with 3x3 neighborhood
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_median_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # Apply Sobel Edge Detection
    '''def apply_sobel_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)  # Horizontal edges
            sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)  # Vertical edges
            result = cv2.magnitude(sobel_horizontal, sobel_vertical)
            result = np.asarray(result, dtype=np.uint8)
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_sobel_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()'''
    # Apply Sobel Edge Detection With Threshold
    def apply_sobel_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            ksize = 3  # Experiment with 3, 5, 7, etc.
            sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)  # Horizontal edges
            sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)  # Vertical edges
            magnitude = cv2.magnitude(sobel_horizontal, sobel_vertical)
            
            # Apply a threshold to highlight significant edges
            _, result = cv2.threshold(magnitude, 100, 255, cv2.THRESH_BINARY)

            result = np.asarray(result, dtype=np.uint8)
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_sobel_threshold_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # Apply Canny Edge Detection
    def apply_canny_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            result = cv2.Canny(img, 100, 200)  # Apply Canny edge detection
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_canny_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    # Apply Laplacian Edge Detection
    def apply_laplacian_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            result = cv2.Laplacian(img, cv2.CV_64F)  # Apply Laplacian edge detection
            result = cv2.convertScaleAbs(result)  # Convert back to uint8
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_laplacian_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # File picker to choose files
    file_picker = ft.FilePicker(on_result=on_upload)
    page.overlay.append(file_picker)

    # Image widget to display the selected image
    image = ft.Image(width=300, height=300)

    # Button to trigger file picker
    upload_button = ft.Button(text="Add Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    # Button to reset to the original image
    reset_button = ft.Button(text="Reset", on_click=reset_image)

    # Adding components to the page
    page.add(
        ft.Column(
            [
                image,
                ft.Container(
                    ft.Row(
                        [
                            upload_button, reset_button,
                            ft.Button(text="Fourier Transform", on_click=apply_fourier_transform),
                            ft.Button(text="Mean Filter", on_click=apply_mean_filter),
                            ft.Button(text="Gaussian Filter", on_click=apply_gaussian_filter),
                            ft.Button(text="Median Filter", on_click=apply_median_filter),
                            ft.Button(text="Sobel Filter", on_click=apply_sobel_filter),
                            ft.Button(text="Canny Filter", on_click=apply_canny_filter),
                            ft.Button(text="Laplacian Filter", on_click=apply_laplacian_filter)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        wrap=True  # Allow buttons to wrap if they exceed the row width
                    ),
                    height=200,
                    padding=10,
                    expand=True,
                    alignment=ft.alignment.center  # Center the container content
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
