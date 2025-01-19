import flet as ft
import cv2
import numpy as np
import os
import time

def main(page: ft.Page):
    page.title = "Image Enhancement App"
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

    def apply_histogram_equalization(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            result = cv2.equalizeHist(img)  # Apply histogram equalization
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_histogram_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    def apply_contrast_stretching(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            min_val, max_val = np.min(img), np.max(img)
            result = ((img - min_val) / (max_val - min_val) * 255).astype(np.uint8)  # Apply contrast stretching
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_contrast_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    def apply_gamma_correction(e, gamma=1.0):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path)
            inv_gamma = 1.0 / gamma
            table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype(np.uint8)
            result = cv2.LUT(img, table)  # Apply gamma correction
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_gamma_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    def apply_sharpening_filter(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path)
            sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening kernel
            result = cv2.filter2D(img, -1, sharpening_kernel)  # Apply sharpening filter
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_sharpen_{timestamp}.png")
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
                            ft.Button(text="Histogram Equalization", on_click=apply_histogram_equalization),
                            ft.Button(text="Contrast Stretching", on_click=apply_contrast_stretching),
                            ft.Button(text="Gamma Correction", on_click=lambda e: apply_gamma_correction(e, gamma=1.5)),
                            ft.Button(text="Sharpening", on_click=apply_sharpening_filter)
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
