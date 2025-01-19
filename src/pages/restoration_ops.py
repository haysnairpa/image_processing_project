from flet import ElevatedButton, View, Column, Row, Image, FilePicker, Text, Page
from PIL import Image as PILImage
import numpy as np
import scipy.signal
import io
import base64

def restoration_page(page: Page):
    uploaded_image = None
    processed_image = None
    mask_image = None

    def upload_image(e):
        nonlocal uploaded_image, processed_image
        if e.files:
            file_path = e.files[0].path
            uploaded_image = PILImage.open(file_path)
            processed_image = uploaded_image.copy()
            show_image(processed_image, "Uploaded Image")

    def upload_mask(e):
        nonlocal mask_image
        if e.files:
            file_path = e.files[0].path
            mask_image = PILImage.open(file_path).convert("L")
            show_image(mask_image, "Mask Image")

    def show_image(img, title):
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        image_display.src_base64 = img_base64
        image_title.value = title
        page.update()

    def apply_gaussian_filter(e):
        nonlocal processed_image
        if processed_image:
            processed_image = processed_image.filter(PILImage.Filter.GaussianBlur(radius=2))
            show_image(processed_image, "Gaussian Filter Applied")

    def apply_wiener_filter(e):
        nonlocal processed_image
        if processed_image:
            arr = np.array(processed_image)
            restored = scipy.signal.wiener(arr, mysize=5, noise=0.1)
            processed_image = PILImage.fromarray(np.uint8(restored))
            show_image(processed_image, "Wiener Filter Applied")

    def apply_inpainting(e):
        nonlocal processed_image
        if processed_image and mask_image:
            import cv2
            inpainted = cv2.inpaint(
                np.array(processed_image), np.array(mask_image), inpaintRadius=3, flags=cv2.INPAINT_TELEA
            )
            processed_image = PILImage.fromarray(inpainted)
            show_image(processed_image, "Inpainting Applied")

    file_picker = FilePicker(on_result=upload_image)
    mask_picker = FilePicker(on_result=upload_mask)
    page.overlay.extend([file_picker, mask_picker])

    image_display = Image(width=300, height=300)
    image_title = Text("No image uploaded")

    return View(
        controls=[
            Column(
                [
                    ElevatedButton("Upload Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    ElevatedButton("Upload Mask", on_click=lambda _: mask_picker.pick_files(allow_multiple=False)),
                    Row(
                        [
                            ElevatedButton("Gaussian Filter", on_click=apply_gaussian_filter),
                            ElevatedButton("Wiener Filter", on_click=apply_wiener_filter),
                        ]
                    ),
                    ElevatedButton("Apply Inpainting", on_click=apply_inpainting),
                    image_display,
                    image_title,
                ],
                spacing=20,
            )
        ]
    )