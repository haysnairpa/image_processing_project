import base64
import flet as ft
from PIL import Image
import io
import os
from libs.basic_operations import *

class PhotoEditorPage(ft.UserControl):
    def __init__(self, page: ft.Page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.uploaded_image = None
        self.processed_image = None
        self.init_controls()

    def init_controls(self):
        # Initialize sliders
        self.red_slider = ft.Slider(min=0, max=255, value=0, label="Red")
        self.green_slider = ft.Slider(min=0, max=255, value=0, label="Green")
        self.blue_slider = ft.Slider(min=0, max=255, value=0, label="Blue")
        self.brightness_slider = ft.Slider(min=0.1, max=3.0, value=1.0, label="Brightness")
        self.contrast_slider = ft.Slider(min=0.1, max=3.0, value=1.0, label="Contrast")
        
        # Initialize dropdowns
        self.flip_dropdown = ft.Dropdown(
            width=300,
            options=[
                ft.dropdown.Option("Horizontal"),
                ft.dropdown.Option("Vertical"),
                ft.dropdown.Option("Diagonal"),
            ],
            value="Horizontal"
        )
        
        self.filter_dropdown = ft.Dropdown(
            width=300,
            options=[
                ft.dropdown.Option("Sepia"),
                ft.dropdown.Option("Cyanotype"),
            ],
            value="Sepia"
        )
        
        # Initialize text fields
        self.rotation_angle = ft.TextField(value="0", label="Angle", width=300)
        self.gamma = ft.TextField(value="1", label="Gamma", width=300)
        self.new_width = ft.TextField(value="0", label="New Width", width=145)
        self.new_height = ft.TextField(value="0", label="New Heigth", width=145)
        self.maintain_aspect = None # use toogle button to implement this
        self.translate_x = ft.TextField(value="0", label="X", width=145)
        self.translate_y = ft.TextField(value="0", label="Y", width=145)
        self.border_thickness = ft.TextField(value="5", label="Thickness")
        self.border_color = ft.TextField(value="Black", label="Color")
        
        # Initialize file picker
        self.file_picker = ft.FilePicker(
            on_result=self.handle_file_picked
        )
        self.page.overlay.append(self.file_picker)
        
        self.save_file_dialog = ft.FilePicker(
            on_result=self.handle_save_result
        )
        self.page.overlay.append(self.save_file_dialog)

    def pil_to_ft_image(self, pil_image, width=None, height=None):
        # Convert PIL image to flet Image
        img_byte_arr = io.BytesIO()
        pil_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return ft.Stack(
            controls=[
                    ft.Image(
                        src_base64=base64.b64encode(img_byte_arr).decode(),
                        width=width,
                        height=height,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        icon_color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLACK54,
                        on_click=lambda _: self.reset_input(),
                    ),
                ],
        )

    def handle_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            self.uploaded_image = Image.open(file_path)
            self.processed_image = self.uploaded_image.copy()
            self.update_images()

    def handle_save_result(self, e: ft.FilePickerResultEvent):
        if e.path and self.processed_image:
            try:
                self.processed_image.save(e.path)
            except Exception as e:
                print(f"Error saving image: {str(e)}")

    def update_images(self):
        if self.processed_image:
            self.output_image.controls[0].content = self.pil_to_ft_image(self.processed_image, 600, 600)
        self.update()

    # Image processing methods
    def apply_grayscale(self, _):
        if self.processed_image:
            self.processed_image = apply_grayscale(self.processed_image)
            self.update_images()

    def apply_negative(self, _):
        if self.processed_image:
            self.processed_image = apply_negative(self.processed_image)
            self.update_images()

    def apply_color_manipulation(self, _):
        if self.processed_image:
            r = int(self.red_slider.value)
            g = int(self.green_slider.value)
            b = int(self.blue_slider.value)
            self.processed_image = apply_color_manipulation(self.processed_image, r, g, b)
            self.update_images()

    def apply_flip(self, _):
        if self.processed_image:
            self.processed_image = apply_flip(self.processed_image, self.flip_dropdown.value)
            self.update_images()

    def apply_scale(self, _):
        if self.processed_image:
            self.processed_image = apply_scaling(self.processed_image, int(self.new_width.value), int(self.new_height.value))
            self.update_images()

    def apply_translate(self, _):
        if self.processed_image:
            self.processed_image = apply_translation(self.processed_image, int(self.translate_x.value), int(self.translate_y.value))
            self.update_images()

    def apply_rotation(self, _):
        if self.processed_image:
            angle = float(self.rotation_angle.value)
            self.processed_image = apply_rotation(self.processed_image, angle)
            self.update_images()

    def apply_brightness(self, _):
        if self.processed_image:
            factor = float(self.brightness_slider.value)
            self.processed_image = apply_brightness(self.processed_image, factor)
            self.update_images()

    def apply_contrast(self, _):
        if self.processed_image:
            factor = float(self.contrast_slider.value)
            self.processed_image = apply_contrast(self.processed_image, factor)
            self.update_images()

    def apply_he(self, _):
        if self.processed_image:
            self.processed_image = apply_histogram_equalization(self.processed_image)
            self.update_images()

    def apply_cs(self, _):
        if self.processed_image:
            self.processed_image = apply_contrast_stretching(self.processed_image)
            self.update_images()

    def apply_gc(self, _):
        if self.processed_image:
            gamma = float(self.gamma.value)
            self.processed_image = apply_gamma_correction(self.processed_image, gamma)
            self.update_images()

    def apply_color_filtering(self, _):
        if self.processed_image:
            self.processed_image = apply_color_filter(self.processed_image, self.filter_dropdown.value)
            self.update_images()
    
    def apply_gaussian(self, _):
        if self.processed_image:
            self.processed_image = apply_gaussian_filter(self.processed_image)
            self.update_images()

    def apply_median(self, _):
        if self.processed_image:
            self.processed_image = apply_median_filter(self.processed_image)
            self.update_images()

    def apply_mean(self, _):
        if self.processed_image:
            self.processed_image = apply_mean_filter(self.processed_image)
            self.update_images()

    def apply_sobel(self, _):
        if self.processed_image:
            self.processed_image = apply_sobel_filter(self.processed_image)
            self.update_images()

    def apply_canny(self, _):
        if self.processed_image:
            self.processed_image = apply_canny_filter(self.processed_image)
            self.update_images()

    def apply_laplacian(self, _):
        if self.processed_image:
            self.processed_image = apply_laplacian_filter(self.processed_image)
            self.update_images()

    def apply_wiener(self, _):
        if self.processed_image:
            self.processed_image = apply_wiener_filter(self.processed_image)
            self.update_images()

    def apply_high_pass(self, _):
        if self.processed_image:
            self.processed_image = apply_high_pass_filter(self.processed_image)
            self.update_images()

    def apply_low_pass(self, _):
        if self.processed_image:
            self.processed_image = apply_low_pass_filter(self.processed_image)
            self.update_images()

    def apply_border(self, _):
        if self.processed_image:
            thickness = int(self.border_thickness.value)
            color = self.border_color.value
            self.processed_image = apply_border(self.processed_image, thickness, color)
            self.update_images()

    def apply_morphological(self, operation_type):
        if self.processed_image:
            self.processed_image = apply_morphological_operation(self.processed_image, operation_type)
            self.update_images()

    def reset_image(self, _):
        if self.uploaded_image:
            self.processed_image = self.uploaded_image.copy()
            self.update_images()

    def save_image(self, _):
        if self.processed_image:
            self.save_file_dialog.save_file(
                allowed_extensions=["png", "jpg", "jpeg"],
                file_name="processed_image.png"
            )
    def create_tool_button(self, text, icon, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=icon,
                        size=20,
                        color=ft.colors.WHITE,
                    ),
                    ft.Text(
                        text,
                        color=ft.colors.BLACK,
                        size=14,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.all(8),
            on_click=on_click,
            ink=True,
        )

    def reset_input(self):
        self.uploaded_image = None
        self.processed_image = None
        self.output_image.controls[0].content = ft.Container(
            content=ft.IconButton(
                icon=ft.icons.ADD_PHOTO_ALTERNATE_ROUNDED,
                icon_size=50,
                icon_color=ft.colors.BLUE_200,
                on_click=lambda _: self.file_picker.pick_files(),
            ),
            width=200,
            height=200,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            alignment=ft.alignment.center,
        )
        self.update()

    def build(self):
        # Back button
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.colors.BLUE_400,
            on_click=self.on_back,
        )

        # Title and description
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Photos Editor",
                        size=32,
                        weight="bold",
                        color=ft.colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Edit and process your photo",
                        size=16,
                        color=ft.colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=ft.padding.all(20),
        )
        # Create toolbar sections
        crop_rotate_tools = ft.ExpansionTile(
            title=ft.Text("Crop & Rotate"),
            subtitle=ft.Text("Crop and rotate your image"),
            controls=[
                ft.Column(
                    [
                        self.create_tool_button("Crop", ft.icons.CROP, lambda _: self.apply_negative),
                        ft.Row(
                            [
                                self.rotation_angle,
                                self.create_tool_button("Rotate", ft.icons.ROTATE_RIGHT, self.apply_rotation),
                            ],
                            spacing=5
                        )
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,
        )

        transform_tools = ft.ExpansionTile(
            title=ft.Text("Transformation"),
            subtitle=ft.Text("Apply transformations to your image"),
            controls=[
                ft.Column(
                    [
                        self.create_tool_button("Grayscale", ft.icons.GRADIENT, self.apply_grayscale),
                        self.create_tool_button("Negative", ft.icons.INVERT_COLORS, self.apply_negative),
                        ft.Row(
                            [
                                self.translate_x,
                                self.translate_y,
                                self.create_tool_button("Translate", ft.icons.TRANSLATE, self.apply_translate),
                            ], 
                            spacing=5
                        ),
                        ft.Row(
                            [
                                self.new_width,
                                self.new_height,
                                # self.maintain_aspect,
                                self.create_tool_button("Scale", ft.icons.SCALE, self.apply_scale),
                            ], 
                            spacing=5
                        ),
                        ft.Row(
                            [
                                self.flip_dropdown,
                                self.create_tool_button("Flip", ft.icons.FLIP, self.apply_flip),
                            ], 
                            spacing=5
                        ),
                    ],
                    spacing=5,
                ),
            ],
            tile_padding=5,

        )

        filter_tools = ft.ExpansionTile(
            title=ft.Text("Filters"),
            subtitle=ft.Text("Apply color filters"),
            controls=[
                ft.Column(
                    [
                        self.create_tool_button("Gaussian Filter", ft.icons.FILTER_1, self.apply_gaussian),
                        self.create_tool_button("Median Filter", ft.icons.FILTER_2, self.apply_median),
                        self.create_tool_button("Mean Filter", ft.icons.FILTER_3, self.apply_mean),
                        self.create_tool_button("Sobel Filter", ft.icons.FILTER_4, self.apply_sobel),
                        self.create_tool_button("Canny Filter", ft.icons.FILTER_5, self.apply_canny),
                        self.create_tool_button("Laplacian Filter", ft.icons.FILTER_6, self.apply_laplacian),
                        self.create_tool_button("Wiener Filter", ft.icons.FILTER_7, self.apply_wiener),
                        self.create_tool_button("Low Pass Filter", ft.icons.FILTER_8, self.apply_low_pass),
                        self.create_tool_button("High Pass Filter", ft.icons.FILTER_9, self.apply_high_pass),
                        ft.Row(
                            [
                                self.filter_dropdown,
                                self.create_tool_button("Apply Filter", ft.icons.FILTER, self.apply_color_filtering),

                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,

        )

        color_tools = ft.ExpansionTile(
            title=ft.Text("Color"),
            subtitle=ft.Text("Adjust color channels"),
            controls=[
                ft.Column(
                    [
                        self.red_slider,
                        self.green_slider,
                        self.blue_slider,
                        self.create_tool_button("Apply Colors", ft.icons.COLOR_LENS, self.apply_color_manipulation),
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,

        )

        enhancement_tools = ft.ExpansionTile(
            title=ft.Text("Enhancement"),
            subtitle=ft.Text("Adjust brightness and contrast"),
            controls=[
                ft.Column(
                    [
                        self.create_tool_button("Histogram Equalization", ft.icons.EQUALIZER, self.apply_he),
                        self.create_tool_button("Contrast Stretching", ft.icons.CONTRAST_ROUNDED, self.apply_cs),
                        ft.Row([
                            self.gamma,
                            self.create_tool_button("Gamma Correction", None, self.apply_gc),
                        ], spacing=5),
                        ft.Row([
                            self.brightness_slider,
                            self.create_tool_button("Brightness", ft.icons.BRIGHTNESS_6, self.apply_brightness),
                        ], spacing=5),
                        ft.Row([
                            self.contrast_slider,
                            self.create_tool_button("Contrast", ft.icons.CONTRAST, self.apply_contrast),
                        ], spacing=5),
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,

        )

        morphological_tools = ft.ExpansionTile(
            title=ft.Text("Morphological"),
            subtitle=ft.Text("Apply morphological operations"),
            controls=[
                ft.Column(
                    [
                        self.create_tool_button("Dilation", ft.icons.ADD, lambda _: self.apply_morphological("dilation")),
                        self.create_tool_button("Erosion", ft.icons.REMOVE, lambda _: self.apply_morphological("erosion")),
                        self.create_tool_button("Opening", ft.icons.OPEN_IN_NEW, lambda _: self.apply_morphological("opening")),
                        self.create_tool_button("Closing", ft.icons.CLOSE, lambda _: self.apply_morphological("closing")),
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,
        )

        border_tools = ft.ExpansionTile(
            title=ft.Text("Border"),
            subtitle=ft.Text("Add border to your image"),
            controls=[
                ft.Column(
                    [
                        self.border_thickness,
                        self.border_color,
                        self.create_tool_button("Apply Border", ft.icons.BORDER_STYLE, self.apply_border),
                    ],
                    spacing=10,
                ),
            ],
            tile_padding=5,
        )

        # Create toolbar with ExpansionTiles
        toolbar = ft.Column(
            controls=[
                crop_rotate_tools,
                transform_tools,
                filter_tools,
                color_tools,
                enhancement_tools,
                morphological_tools,
                border_tools,
            ],
            spacing=0,
            expand=True,
        )

        self.output_image = ft.Stack(
            controls=[
                ft.Container(
                    content=ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.ADD_PHOTO_ALTERNATE_ROUNDED,
                            icon_size=50,
                            icon_color=ft.colors.BLUE_200,
                            on_click=lambda _: self.file_picker.pick_files(),
                        ),
                        width=200,
                        height=200,
                        bgcolor=ft.colors.BLUE_50,
                        border_radius=10,
                        alignment=ft.alignment.center,
                    ),
                    width=600,
                    height=600,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
            ],
        )
    
        image_area = ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            self.output_image,
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            text="Download",
                                            icon=ft.icons.DOWNLOAD,
                                            on_click=self.save_image,
                                        ),
                                        ft.ElevatedButton(
                                            text="Reset",
                                            icon=ft.icons.REFRESH,
                                            on_click=self.reset_image,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                padding=ft.padding.symmetric(vertical=10),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                    expand=True,
                ),
            ],
            expand=True,
        )

        # Create main layout
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row([back_button], alignment=ft.MainAxisAlignment.START),
                    header,
                    ft.Row(
                        [
   
                            ft.Container(
                                content=toolbar,
                                expand=1,
                                padding=10,
                            ),
                            ft.VerticalDivider(width=1),
                            ft.Container(
                                content=image_area,
                                expand=2,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=ft.padding.all(20),
            alignment=ft.alignment.center,
            expand=True,
        )

