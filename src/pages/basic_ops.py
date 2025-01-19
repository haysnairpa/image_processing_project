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
)
from PIL import Image as PILImage, ImageOps, ImageEnhance, ImageDraw
import io
import base64


def basic_operations_page(page: Page):
    uploaded_image = None  # Original image
    processed_image = None  # Processed image (stateful)

    def upload_image(e: FilePickerResultEvent):
        nonlocal uploaded_image, processed_image
        if e.files:
            file_path = e.files[0].path
            uploaded_image = PILImage.open(file_path)
            processed_image = uploaded_image.copy()  # Initialize processed image
            show_image(processed_image, "Uploaded Image")

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
            image_display.src_base64 = img_base64
            image_title.value = title
            page.update()
        except Exception as e:
            print(f"Error showing image: {e}")
            image_title.value = f"Error: {str(e)}"
            page.update()

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
    def apply_crop(e):
        nonlocal processed_image
        if processed_image:
            x1, y1, x2, y2 = map(int, crop_coordinates.value.split(","))
            processed_image = processed_image.crop((x1, y1, x2, y2))
            show_image(processed_image, "Cropped Image")

    # Functionality: Scaling
    def apply_scaling(e):
        nonlocal processed_image
        if processed_image:
            scale = float(scale_slider.value)
            width = int(processed_image.width * scale)
            height = int(processed_image.height * scale)
            processed_image = processed_image.resize((width, height))
            show_image(processed_image, f"Scaled: {scale}x")

    # Functionality: Image Blending
    def apply_blending(e):
        nonlocal processed_image
        if processed_image and uploaded_image:
            alpha = blend_slider.value
            processed_image = PILImage.blend(uploaded_image, processed_image, alpha)
            show_image(processed_image, f"Blended with alpha {alpha}")

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

    # Overlay
    def apply_overlay(e):
        """Overlay a secondary image onto the primary image with transparency."""
        nonlocal processed_image
        if processed_image and secondary_image:
            overlay_alpha = overlay_transparency.value
            overlay_resized = secondary_image.resize(processed_image.size)
            processed_image = PILImage.blend(processed_image, overlay_resized, overlay_alpha)
            show_image(processed_image, f"Overlay with alpha {overlay_alpha}")

    # UI Components
    file_picker = FilePicker(on_result=upload_image)
    page.overlay.append(file_picker)

    # Define all UI components first
    red_slider = Slider(min=0, max=255, value=0, label="Red")
    green_slider = Slider(min=0, max=255, value=0, label="Green")
    blue_slider = Slider(min=0, max=255, value=0, label="Blue")
    
    scale_slider = Slider(min=0.1, max=2.0, value=1.0, label="Scale")
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

    # Then define control groups
    basic_controls = Row(
        [
            ElevatedButton("Upload Image", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
            ElevatedButton("Reset Image", on_click=reset_image),
        ],
        alignment="center"
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

    geometry_controls = Column(
        [
            Text("Geometry", size=14, weight="bold"),
            Row(
                [
                    Column([
                        scale_slider,
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

    enhancement_controls = Column(
        [
            Text("Enhancements", size=14, weight="bold"),
            Row(
                [
                    Column([
                        brightness_slider,
                        contrast_slider,
                    ], expand=True),
                    Column([
                        ElevatedButton("Brightness", on_click=apply_brightness),
                        ElevatedButton("Contrast", on_click=apply_contrast),
                    ])
                ]
            ),
        ]
    )

    effects_controls = Column(
        [
            Text("Effects", size=14, weight="bold"),
            Row(
                [
                    filter_dropdown,
                    ElevatedButton("Apply Filter", on_click=apply_color_filter),
                    border_thickness,
                    border_color,
                    ElevatedButton("Add Border", on_click=apply_border),
                ],
                wrap=True
            ),
        ]
    )

    # Wrap all controls in a scrollable container
    controls_container = Container(
        content=Column(
            [
                basic_controls,
                transform_controls,
                geometry_controls, 
                color_controls,
                enhancement_controls,
                effects_controls,
            ],
            spacing=20,
            scroll=ScrollMode.AUTO,
            height=800,  # Match image height
        ),
        width=400,   # Fixed width for controls
        bgcolor="#000000",  # Light background for controls area
        padding=20,
    )

    # Back button with nice design
    back_button = Container(
        content=IconButton(
            icon=Icons.ARROW_BACK,
            icon_color="white",
            on_click=lambda _: page.go("/"),
            tooltip="Back to Home",
        ),
        bgcolor="#2196F3",
        border_radius=30,
        padding=5,
        margin=10,
        offset=transform.Offset(-0.45, 0),
        animate_offset=animation.Animation(300, "easeOut"),
    )

    return View(
        controls=[
            Stack([  # Use Stack to overlay back button
                Container(  # Main content container
                    content=Row(
                        [
                            # Left side - Image
                            Container(
                                content=Column(
                                    [image_title, image_display],
                                    horizontal_alignment="center",
                                ),
                                expand=True,
                            ),
                            # Right side - Controls
                            controls_container,
                        ],
                        spacing=20,
                        height=page.window.height,  # Updated to new property
                    ),
                ),
                back_button,  # Floating back button
            ]),
        ],
    )
