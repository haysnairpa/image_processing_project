import flet as ft
from PIL import Image, ImageChops, ImageOps
import cv2
import numpy as np
import os
import time

def main(page: ft.Page):
    page.title = "Image Processing App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = "always"

    # Create the "images" folder if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    original_image_path = None  # Store the path of the original uploaded image
    current_image_path = None  # Store the path of the current image
    previous_image_path = None  # Store the path of the previous image for undo functionality
    second_image_path = None  # Store the path of the second image for operations
    current_operation = None  # Track the current operation

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

    def add_second_image(e):
        file_picker_second.pick_files(allow_multiple=False)

    def on_upload_second(e):
        nonlocal second_image_path, current_operation
        if file_picker_second.result is not None and file_picker_second.result.files is not None:
            if len(file_picker_second.result.files) > 0:
                uploaded_file = file_picker_second.result.files[0]
                second_image_path = uploaded_file.path  # Save the path of the second image
                
                # Perform the chosen operation
                if current_operation:
                    current_operation()
                current_operation = None  # Reset current operation

    def reset_image(e):
        nonlocal current_image_path, previous_image_path
        if original_image_path:
            image.src = original_image_path  # Revert to the original image
            current_image_path = original_image_path  # Reset current image path
            previous_image_path = None  # Reset previous image path
            page.update()

    # Resize second image to match the size of the first image
    def resize_image(image1, image2):
        return cv2.resize(image2, (image1.shape[1], image1.shape[0]))


    # Define functions for mathematical and bitwise operations
    def add_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path)
            img2 = cv2.imread(second_image_path)
            img2 = resize_image(img1, img2)
            result = cv2.add(img1, img2)  # Perform the addition operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_add_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()

    def subtract_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path)
            img2 = cv2.imread(second_image_path)
            img2 = resize_image(img1, img2)

            # Ensure both images have the same number of channels
            if len(img1.shape) == 2:  # Grayscale to RGB
                img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
            if len(img2.shape) == 2:  # Grayscale to RGB
                img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

            result = cv2.subtract(img1, img2)  # Perform the subtraction operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_subtract_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def multiply_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path)
            img2 = cv2.imread(second_image_path)
            img2 = resize_image(img1, img2)

            # Ensure both images have the same number of channels
            if len(img1.shape) == 2:  # Grayscale to RGB
                img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
            if len(img2.shape) == 2:  # Grayscale to RGB
                img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

            result = cv2.multiply(img1, img2)  # Perform the multiplication operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_multiply_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def divide_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path)
            img2 = cv2.imread(second_image_path)
            img2 = resize_image(img1, img2)

            # Convert to float32 and add epsilon to avoid division by zero
            img1 = img1.astype(np.float32)
            img2 = img2.astype(np.float32) + 1e-5

            result = cv2.divide(img1, img2)  # Perform the division operation

            # Normalize the result to the range [0, 255]
            result = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            
            # Optional: Adjust the brightness
            brightness_factor = 3  # Adjust this factor to increase brightness
            result = cv2.convertScaleAbs(result, alpha=brightness_factor, beta=0)

            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_divide_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def bitwise_and_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(second_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = resize_image(img1, img2)
            result = cv2.bitwise_and(img1, img2)  # Perform the bitwise AND operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_and_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def bitwise_or_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(second_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = resize_image(img1, img2)
            result = cv2.bitwise_or(img1, img2)  # Perform the bitwise OR operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_or_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def bitwise_xor_images():
        nonlocal current_image_path, previous_image_path
        if current_image_path and second_image_path:
            img1 = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(second_image_path, cv2.IMREAD_GRAYSCALE)
            img2 = resize_image(img1, img2)
            result = cv2.bitwise_xor(img1, img2)  # Perform the bitwise XOR operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_xor_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    def bitwise_not_image(e):
        nonlocal current_image_path, previous_image_path
        if current_image_path:
            img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
            result = cv2.bitwise_not(img)  # Perform the bitwise NOT operation
            timestamp = str(int(time.time()))
            result_path = os.path.join("images", f"result_not_{timestamp}.png")
            cv2.imwrite(result_path, result)
            previous_image_path = current_image_path  # Update previous image path
            current_image_path = result_path  # Update current image path
            image.src = result_path  # Update the image source
            page.update()


    # File picker to choose files
    file_picker = ft.FilePicker(on_result=on_upload)
    file_picker_second = ft.FilePicker(on_result=on_upload_second)
    page.overlay.append(file_picker)
    page.overlay.append(file_picker_second)

    # Image widget to display the selected image
    image = ft.Image(width=300, height=300)

    # Button to trigger file picker
    upload_button = ft.Button(text="Add Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    # Button to reset to the original image
    reset_button = ft.Button(text="Reset", on_click=reset_image)

    # Buttons for operations
    add_button = ft.Button(text="Add", on_click=lambda _: set_operation(add_images))
    subtract_button = ft.Button(text="Subtract", on_click=lambda _: set_operation(subtract_images))
    multiply_button = ft.Button(text="Multiply", on_click=lambda _: set_operation(multiply_images))
    divide_button = ft.Button(text="Divide", on_click=lambda _: set_operation(divide_images))
    and_button = ft.Button(text="AND", on_click=lambda _: set_operation(bitwise_and_images))
    or_button = ft.Button(text="OR", on_click=lambda _: set_operation(bitwise_or_images))
    xor_button = ft.Button(text="XOR", on_click=lambda _: set_operation(bitwise_xor_images))
    not_button = ft.Button(text="NOT", on_click=bitwise_not_image)

    # Adding components to the page
    page.add(
        ft.Column(
            [
                image,
                ft.Container(
                    ft.Row(
                        [
                            upload_button, reset_button,
                            add_button, subtract_button, multiply_button, divide_button,
                            and_button, or_button, xor_button, not_button
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

    def set_operation(operation):
        nonlocal current_operation
        current_operation = operation
        add_second_image(None)

ft.app(target=main)
