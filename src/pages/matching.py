from flet import ElevatedButton, View, Column, Row, Image, FilePicker, Text, Page
from PIL import Image as PILImage
import numpy as np
import cv2
import io
import base64

def matching_page(page: Page):
    uploaded_image = None
    secondary_image = None
    processed_image = None

    def upload_image(e):
        nonlocal uploaded_image, processed_image
        if e.files:
            file_path = e.files[0].path
            uploaded_image = PILImage.open(file_path)
            processed_image = uploaded_image.copy()
            show_image(processed_image, "Uploaded Image")

    def upload_secondary(e):
        nonlocal secondary_image
        if e.files:
            file_path = e.files[0].path
            secondary_image = PILImage.open(file_path)
            show_image(secondary_image, "Secondary Image")

    def show_image(img, title):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        image_display.src_base64 = img_base64
        image_title.value = title
        page.update()

    def apply_feature_matching(e):
        nonlocal processed_image
        if processed_image and secondary_image:
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(np.array(processed_image), None)
            kp2, des2 = orb.detectAndCompute(np.array(secondary_image), None)

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)

            result = cv2.drawMatches(
                np.array(processed_image), kp1, np.array(secondary_image), kp2, matches[:10], None, flags=2
            )
            processed_image = PILImage.fromarray(result)
            show_image(processed_image, "Feature Matching Applied")

    file_picker = FilePicker(on_result=upload_image)
    secondary_picker = FilePicker(on_result=upload_secondary)
    page.overlay.extend([file_picker, secondary_picker])

    image_display = Image(width=300, height=300)
    image_title = Text("No image uploaded")

    return View(
        controls=[
            Column(
                [
                    ElevatedButton("Upload Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    ElevatedButton("Upload Secondary Image", on_click=lambda _: secondary_picker.pick_files(allow_multiple=False)),
                    ElevatedButton("Apply Feature Matching", on_click=apply_feature_matching),
                    image_display,
                    image_title,
                ],
                spacing=20,
            )
        ]
    )
