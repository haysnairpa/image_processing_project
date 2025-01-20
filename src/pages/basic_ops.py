from flet import (
    ElevatedButton,
    View,
    Text,
    FilePicker,
    FilePickerResultEvent,
    Column,
    Row,
    Image,
    Slider,
    TextField,
    Page,
    Dropdown,
    Checkbox,
    dropdown,
    ScrollMode,
    Container,
    IconButton,
    Icons,
    Stack,
    FloatingActionButtonLocation,
    animation,
    transform,
    GestureDetector,
    MouseCursor,
    border,
    alignment,
)
from PIL import Image as PILImage, ImageOps, ImageEnhance, ImageDraw
import io
import base64
import cv2
import numpy as np
import os
import time
import scipy.signal


def basic_operations_page(page: Page, on_back=None):
    page.title = "Photo Editor"
    page.bgcolor = "#1a1a1a"
    page.padding = 0
    uploaded_image = None  # Original image
    processed_image = None  # Processed image (stateful)

    # State variables for cropping
    is_cropping = False
    crop_start_x = 0
    crop_start_y = 0
    crop_end_x = 0
    crop_end_y = 0

    # Definisi fungsi upload terlebih dahulu
    def upload_image(e: FilePickerResultEvent):
        nonlocal uploaded_image, processed_image
        if e.files:
            file_path = e.files[0].path
            uploaded_image = PILImage.open(file_path)
            processed_image = uploaded_image.copy()  # Initialize processed image
            show_image(processed_image, "Uploaded Image")

    def handle_save_result(e: FilePickerResultEvent):
        if e.path:
            try:
                processed_image.save(e.path)
                image_title.value = f"Image saved to: {e.path}"
                image_title.update()
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                if image_title:
                    image_title.value = f"Error saving image: {str(e)}"
                    image_title.update()

    # Kemudian inisialisasi FilePicker
    file_picker = FilePicker(on_result=upload_image)
    page.overlay.append(file_picker)

    save_file_dialog = FilePicker(
        on_result=handle_save_result
    )
    page.overlay.append(save_file_dialog)

    # Definisikan semua fungsi processing di sini, sebelum UI components
    def apply_fourier_transform(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image.convert('L'))
            f_transform = np.fft.fft2(img_array)
            f_shift = np.fft.fftshift(f_transform)
            magnitude_spectrum = 20 * np.log(np.abs(f_shift))
            processed_image = PILImage.fromarray(np.uint8(magnitude_spectrum))
            show_image(processed_image, "Fourier Transform Applied")

    def apply_mean_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image)
            kernel = np.ones((5,5), np.float32)/25
            filtered = cv2.filter2D(img_array, -1, kernel)
            processed_image = PILImage.fromarray(filtered)
            show_image(processed_image, "Mean Filter Applied")

    def apply_gaussian_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image)
            filtered = cv2.GaussianBlur(img_array, (5,5), 0)
            processed_image = PILImage.fromarray(filtered)
            show_image(processed_image, "Gaussian Filter Applied")

    def apply_median_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image)
            filtered = cv2.medianBlur(img_array, 3)
            processed_image = PILImage.fromarray(filtered)
            show_image(processed_image, "Median Filter Applied")

    def apply_sobel_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image.convert('L'))
            sobelx = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
            magnitude = np.sqrt(sobelx**2 + sobely**2)
            processed_image = PILImage.fromarray(np.uint8(magnitude))
            show_image(processed_image, "Sobel Filter Applied")

    def apply_canny_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image.convert('L'))
            edges = cv2.Canny(img_array, 100, 200)
            processed_image = PILImage.fromarray(edges)
            show_image(processed_image, "Canny Edge Detection Applied")

    def apply_laplacian_filter(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image.convert('L'))
            laplacian = cv2.Laplacian(img_array, cv2.CV_64F)
            processed_image = PILImage.fromarray(np.uint8(np.absolute(laplacian)))
            show_image(processed_image, "Laplacian Filter Applied")

    def apply_histogram_equalization(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image)
            if len(img_array.shape) == 3:
                img_yuv = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
                img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
                result = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
            else:
                result = cv2.equalizeHist(img_array)
            processed_image = PILImage.fromarray(result)
            show_image(processed_image, "Histogram Equalization Applied")

    def apply_contrast_stretching(e):
        nonlocal processed_image
        if processed_image:
            img_array = np.array(processed_image)
            p2, p98 = np.percentile(img_array, (2, 98))
            result = np.clip(((img_array - p2) / (p98 - p2) * 255), 0, 255).astype(np.uint8)
            processed_image = PILImage.fromarray(result)
            show_image(processed_image, "Contrast Stretching Applied")

    def reset_image(e):
        nonlocal processed_image
        if uploaded_image:
            processed_image = uploaded_image.copy()  # Reset to original image
            show_image(processed_image, "Image Reset")

    def show_image(img, title):
        try:
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            img_base64 = base64.b64encode(buf.getvalue()).decode()
            
            # Pastikan image_display dan image_title sudah diinisialisasi
            if image_display and image_title:
                image_display.src_base64 = img_base64
                image_title.value = title
                
                # Update hanya komponen yang berubah
                image_display.update()
                image_title.update()
        except Exception as e:
            print(f"Error showing image: {e}")
            if image_title:
                image_title.value = f"Error: {str(e)}"
                image_title.update()

    # Functionality: Grayscale
    def apply_grayscale(e):
        nonlocal processed_image
        if processed_image:
            processed_image = ImageOps.grayscale(processed_image)
            show_image(processed_image, "Grayscale Image")

    # Functionality: Negative Transformation
    def apply_negative(e):
        nonlocal processed_image
        if processed_image:
            processed_image = ImageOps.invert(processed_image)
            show_image(processed_image, "Negative Image")

    # Functionality: Color Manipulation
    def apply_color_manipulation(e):
        nonlocal processed_image
        if processed_image:
            r, g, b = int(red_slider.value), int(green_slider.value), int(blue_slider.value)
            pixels = processed_image.load()
            for x in range(processed_image.width):
                for y in range(processed_image.height):
                    pr, pg, pb = pixels[x, y]
                    pixels[x, y] = (
                        min(pr + r, 255),
                        min(pg + g, 255),
                        min(pb + b, 255),
                    )
            show_image(processed_image, "Color Manipulation")

    # Functionality: Cropping
    def start_crop(e):
        nonlocal is_cropping, crop_start_x, crop_start_y
        is_cropping = True
        crop_start_x = e.local_x
        crop_start_y = e.local_y
        crop_overlay.visible = True
        crop_overlay.left = crop_start_x
        crop_overlay.top = crop_start_y
        crop_overlay.update()  # Update hanya overlay

    def update_crop(e):
        nonlocal crop_end_x, crop_end_y
        if is_cropping:
            crop_end_x = e.local_x
            crop_end_y = e.local_y
            
            # Update overlay position and size
            crop_overlay.width = abs(crop_end_x - crop_start_x)
            crop_overlay.height = abs(crop_end_y - crop_start_y)
            crop_overlay.left = min(crop_start_x, crop_end_x)
            crop_overlay.top = min(crop_start_y, crop_end_y)
            crop_overlay.update()  # Update hanya overlay

    def end_crop(e):
        nonlocal is_cropping, processed_image
        if is_cropping and processed_image:
            is_cropping = False
            crop_overlay.visible = False
            
            # Convert coordinates
            scale_x = processed_image.width / image_display.width
            scale_y = processed_image.height / image_display.height
            
            x1 = int(min(crop_start_x, crop_end_x) * scale_x)
            y1 = int(min(crop_start_y, crop_end_y) * scale_y)
            x2 = int(max(crop_start_x, crop_end_x) * scale_x)
            y2 = int(max(crop_start_y, crop_end_y) * scale_y)
            
            # Crop image
            try:
                cropped = processed_image.crop((x1, y1, x2, y2))
                processed_image = cropped
                show_image(processed_image, "Cropped Image")
            except Exception as e:
                print(f"Error cropping: {str(e)}")
                if image_title:
                    image_title.value = f"Error cropping image: {str(e)}"
                    image_title.update()

    # Functionality: Scaling
    def apply_scaling(e):
        nonlocal processed_image
        if processed_image:
            try:
                scale = float(scale_slider.value)
                
                # Get original dimensions
                orig_width = processed_image.width
                orig_height = processed_image.height
                
                # Calculate new dimensions
                if maintain_aspect.value:
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                else:
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                
                # Resize image
                processed_image = processed_image.resize(
                    (new_width, new_height), 
                    PILImage.LANCZOS
                )
                
                # Update image display tanpa page.update()
                show_image(processed_image, f"Scaled: {scale}x")
                
            except Exception as e:
                print(f"Error in scaling: {str(e)}")
                if image_title:
                    image_title.value = f"Error scaling image: {str(e)}"
                    image_title.update()

    # # Functionality: Image Blending
    # def apply_blending(e):
    #     nonlocal processed_image
    #     if processed_image and uploaded_image:
    #         alpha = blend_slider.value
    #         processed_image = PILImage.blend(uploaded_image, processed_image, alpha)
    #         show_image(processed_image, f"Blended with alpha {alpha}")

    # Functionality: Flip
    def apply_flip(e):
        nonlocal processed_image
        if processed_image:
            if flip_dropdown.value == "Horizontal":
                processed_image = ImageOps.mirror(processed_image)
            elif flip_dropdown.value == "Vertical":
                processed_image = ImageOps.flip(processed_image)
            elif flip_dropdown.value == "Diagonal":
                processed_image = ImageOps.mirror(ImageOps.flip(processed_image))
            show_image(processed_image, f"Flipped {flip_dropdown.value}")
    
    # Functinallity: Translation
    def apply_translation(e):
        nonlocal processed_image
        if processed_image:
            dx = int(translation_x.value)
            dy = int(translation_y.value)
            translated_image = PILImage.new("RGB", (processed_image.width, processed_image.height), (0,0,0))
            translated_image.paste(processed_image, (dx, dy))
            processed_image = translated_image
            show_image(processed_image, f"Translated: ({dx}, {dy})")

    # Functionallity: Rotation
    def apply_rotation(e):
        nonlocal processed_image
        if processed_image:
            angle = int(rotation_angle.value)
            processed_image = processed_image.rotate(angle, expand=True)
            show_image(processed_image, f"Rotated {angle}")
    
    # Brightness
    def apply_brightness(e):
        nonlocal processed_image
        if processed_image:
            enhancer = ImageEnhance.Brightness(processed_image)
            processed_image = enhancer.enhance(brightness_slider.value)
            show_image(processed_image, f"Brightness {brightness_slider.value}")

    # Contrast
    def apply_contrast(e):
        nonlocal processed_image
        if processed_image:
            enhancer = ImageEnhance.Contrast(processed_image)
            processed_image = enhancer.enhance(contrast_slider.value)
            show_image(processed_image, f"Contrast {contrast_slider.value}")
    
    # Filtering
    def apply_color_filter(e):
        nonlocal processed_image
        if processed_image:
            if filter_dropdown.value == "Sepia":
                sepia_filter = ImageOps.colorize(processed_image.convert("L"), "#704214", "#C0A080")
                processed_image = sepia_filter
            elif filter_dropdown.value == "Cyanotype":
                cyan_filter = ImageOps.colorize(processed_image.convert("L"), "#002B5B", "#8CF0E8")
                processed_image = cyan_filter
            show_image(processed_image, f"Filter: {filter_dropdown.value}")

    # Border
    def apply_border(e):
        """Add border with customizable color and thickness."""
        nonlocal processed_image
        if processed_image:
            thickness = int(border_thickness.value)
            color = border_color.value
            processed_image = ImageOps.expand(processed_image, border=thickness, fill=color)
            show_image(processed_image, f"Border: {color}, {thickness}px")

    # # Overlay
    # def apply_overlay(e):
    #     """Overlay a secondary image onto the primary image with transparency."""
    #     nonlocal processed_image
    #     if processed_image and secondary_image:
    #         overlay_alpha = overlay_transparency.value
    #         overlay_resized = secondary_image.resize(processed_image.size)
    #         processed_image = PILImage.blend(processed_image, overlay_resized, overlay_alpha)
    #         show_image(processed_image, f"Overlay with alpha {overlay_alpha}")

    # Definisi fungsi save_image di awal
    def save_image(e):
        if processed_image:
            try:
                save_file_dialog.save_file(
                    allowed_extensions=["png", "jpg", "jpeg"],
                    file_name="processed_image.png"
                )
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                if image_title:
                    image_title.value = f"Error saving image: {str(e)}"
                    image_title.update()

    def apply_wiener_filter(e):
        nonlocal processed_image
        if processed_image:
            # Konversi ke array numpy
            img_array = np.array(processed_image)
            
            # Jika gambar berwarna, proses setiap channel
            if len(img_array.shape) == 3:
                result = np.zeros_like(img_array)
                for i in range(3):
                    result[:,:,i] = scipy.signal.wiener(img_array[:,:,i], (5,5))
            else:
                result = scipy.signal.wiener(img_array, (5,5))
            
            processed_image = PILImage.fromarray(np.uint8(result))
            show_image(processed_image, "Wiener Filter Applied")

    # Kemudian definisikan UI components
    filtering_controls = Column(
        [
            Text("Filtering & Edge Detection", size=14, weight="bold"),
            Row(
                [
                    ElevatedButton("Fourier Transform", on_click=apply_fourier_transform),
                    ElevatedButton("Mean Filter", on_click=apply_mean_filter),
                    ElevatedButton("Gaussian Filter", on_click=apply_gaussian_filter),
                    ElevatedButton("Median Filter", on_click=apply_median_filter),
                    ElevatedButton("Wiener Filter", on_click=apply_wiener_filter),
                ],
                wrap=True
            ),
            Row(
                [
                    ElevatedButton("Sobel Edge", on_click=apply_sobel_filter),
                    ElevatedButton("Canny Edge", on_click=apply_canny_filter),
                    ElevatedButton("Laplacian", on_click=apply_laplacian_filter),
                ],
                wrap=True
            ),
        ]
    )

    enhancement_controls = Column(
        [
            Text("Enhancement", size=14, weight="bold"),
            Row(
                [
                    ElevatedButton("Histogram Equalization", on_click=apply_histogram_equalization),
                    ElevatedButton("Contrast Stretching", on_click=apply_contrast_stretching),
                ],
                wrap=True
            ),
        ]
    )

    # UI Components
    file_picker = FilePicker(on_result=upload_image)
    page.overlay.append(file_picker)

    # Define all UI components first
    red_slider = Slider(min=0, max=255, value=0, label="Red")
    green_slider = Slider(min=0, max=255, value=0, label="Green")
    blue_slider = Slider(min=0, max=255, value=0, label="Blue")
    
    scale_slider = Slider(
        min=0.1,
        max=2.0,
        value=1.0,
        label="Scale",
    )
    maintain_aspect = Checkbox(
        label="Maintain Aspect Ratio",
        value=True,
    )
    translation_x = TextField(value="0", label="X", width=100)
    translation_y = TextField(value="0", label="Y", width=100)
    rotation_angle = TextField(value="0", label="Angle", width=100)
    
    brightness_slider = Slider(min=0.1, max=2.0, value=1.0, label="Brightness")
    contrast_slider = Slider(min=0.1, max=2.0, value=1.0, label="Contrast")
    
    flip_dropdown = Dropdown(
        width=150,
        options=[
            dropdown.Option("Horizontal"),
            dropdown.Option("Vertical"),
            dropdown.Option("Diagonal"),
        ],
        value="Horizontal"
    )
    
    filter_dropdown = Dropdown(
        width=150,
        options=[
            dropdown.Option("Sepia"),
            dropdown.Option("Cyanotype"),
        ],
        value="Sepia"
    )
    
    border_thickness = TextField(value="5", label="Thickness", width=100)
    border_color = TextField(value="#000000", label="Color", width=100)

    image_display = Image(width=400, height=600, fit="contain")
    image_title = Text("No image uploaded", size=16, weight="bold")

    # Define basic controls first
    basic_controls = Column(
        [
            Text("Basic Controls", size=14, weight="bold"),
            Row(
                [
                    ElevatedButton("Upload Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    ElevatedButton("Reset Image", on_click=reset_image),
                ],
                wrap=True,
                spacing=10,
            ),
            Row(
                [
                    ElevatedButton("Start Crop", on_click=lambda _: setattr(crop_gesture, "visible", True)),
                    ElevatedButton(
                        "Download Image", 
                        on_click=save_image,
                        disabled=lambda: processed_image is None
                    ),
                ],
                wrap=True,
                spacing=10,
            ),
        ],
        spacing=10,
    )

    # Define control groups
    transform_controls = Column(
        [
            Text("Image Transformations", size=14, weight="bold"),
            Row(
                [
                    ElevatedButton("Grayscale", on_click=apply_grayscale),
                    ElevatedButton("Negative", on_click=apply_negative),
                    flip_dropdown,
                    ElevatedButton("Flip", on_click=apply_flip),
                ],
                wrap=True
            ),
        ]
    )

    color_controls = Column(
        [
            Text("Color Adjustments", size=14, weight="bold"),
            Row(
                [
                    Column([
                        red_slider,
                        green_slider,
                        blue_slider,
                    ], expand=True),
                    ElevatedButton("Apply", on_click=apply_color_manipulation),
                ]
            ),
        ]
    )

    geometry_controls = Column(
        [
            Text("Geometry", size=14, weight="bold"),
            Row(
                [
                    Column([
                        scale_slider,
                        maintain_aspect,
                        Row([translation_x, translation_y]),
                        rotation_angle,
                    ], expand=True),
                    Column([
                        ElevatedButton("Scale", on_click=apply_scaling),
                        ElevatedButton("Move", on_click=apply_translation),
                        ElevatedButton("Rotate", on_click=apply_rotation),
                    ])
                ]
            ),
        ]
    )

    # Create crop overlay container
    crop_overlay = Container(
        visible=False,
        border=border.all(2, "white"),
        bgcolor="#80000000",
    )

    # Update image container
    image_container = Container(
        content=Stack([
            image_display,
            crop_overlay,
        ]),
        width=400,
        height=600,
    )

    # Create gesture detector
    crop_gesture = GestureDetector(
        content=image_container,
        on_pan_start=start_crop,
        on_pan_update=update_crop,
        on_pan_end=end_crop,
        mouse_cursor=MouseCursor.MOVE,
    )

    # Then create main layout
    main_content = Container(
        content=Column(
            [
                Container(  # Header container
                    content=Row(
                        [
                            IconButton(
                                icon=Icons.ARROW_BACK,
                                icon_color="white",
                                on_click=lambda _: page.go("/"),
                                tooltip="Back to Home",
                            ),
                            image_title,
                        ],
                        alignment="center",
                    ),
                    padding=10,
                ),
                Container(  # Main content container
                    content=Row(
                        [
                            Container(  # Controls container with scroll - left
                                content=Column(
                                    [
                                        basic_controls,
                                        transform_controls,
                                        geometry_controls, 
                                        color_controls,
                                        enhancement_controls,
                                        filtering_controls,
                                    ],
                                    spacing=20,
                                    scroll=ScrollMode.ALWAYS,
                                    height=600,
                                ),
                                width=300,
                                bgcolor="#000000",
                                padding=20,
                                border_radius=10,
                                margin=10,
                            ),
                            Container(  # Image container - right
                                content=crop_gesture,
                                expand=True,  # Take remaining space
                                height=600,
                                margin=10,
                                alignment=alignment.center,  # Center the image
                            ),
                        ],
                        spacing=0,
                        alignment="start",
                    ),
                    padding=10,
                ),
            ],
            spacing=0,
            horizontal_alignment="center",
        ),
        expand=True,  # Make container take full width
    )

    view = View(
        "/basic-ops",  # Tambahkan route
        [main_content],
        padding=0,
        bgcolor="#1a1a1a", 
        scroll=ScrollMode.AUTO,
    )
    page.views.append(view)
    page.update()