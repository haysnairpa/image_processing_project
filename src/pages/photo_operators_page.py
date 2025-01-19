import base64
import io
import uuid
import flet as ft
from flet import (
    UserControl,
    Container,
    Row,
    Column,
    Text,
    Image,
    IconButton,
    ElevatedButton,
    Dropdown,
    dropdown,
    Stack,
    Slider,
    TextField,
    alignment,
    border_radius,
    padding,
    margin,
    colors,
    FilePickerResultEvent
)

import numpy as np
from PIL import Image as PILImage

from libs.mathematical_operations import add_images, subtract_images, multiply_images, divide_images, bitwise_and_images, bitwise_or_images, bitwise_xor_images
from libs.blend_image import blend_images, overlay_images

class PhotoOperatorsPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_images = []
        self.result_image = None
        self.image_containers = []
        self.result_container = None
        self.download_button = None
        self.operator_dropdown = None
        self.preview_dialog = None
        self.alpha_slider = None
        self.beta_slider = None
        self.gamma_input = None
        self.blend_params_container = None

    def add_image(self, index):
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                img = Image(
                    src=e.files[0].path,
                    width=200,
                    height=200,
                    fit=ft.ImageFit.COVER,
                    border_radius=border_radius.all(10),
                )
                self.selected_images[index] = img
                self.image_containers[index].content = Stack([
                    img,
                    Container(
                        content=IconButton(
                            icon=ft.icons.CLOSE,
                            icon_color=colors.RED_400,
                            icon_size=20,
                            on_click=lambda _, i=index: self.clear_image(i),
                        ),
                        alignment=alignment.top_right,
                        margin=margin.only(top=-10, right=-10),
                    )
                ])
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=False)

    def clear_image(self, index):
        self.selected_images[index] = None
        self.image_containers[index].content = IconButton(
            icon=ft.icons.ADD,
            icon_color=colors.BLUE_400,
            icon_size=40,
            on_click=lambda _, i=index: self.add_image(i),
        )
        self.update()

    def show_preview(self, index):
        if self.selected_images[index]:
            preview_image = Image(
                src=self.selected_images[index].src,
                fit=ft.ImageFit.CONTAIN,
                width=800,
                height=600,
            )
            
            self.preview_dialog = ft.AlertDialog(
                content=Container(
                    content=preview_image,
                    padding=padding.all(10),
                ),
                actions=[
                    ElevatedButton(text="Close", on_click=self.close_preview)
                ],
            )
            
            self.page.dialog = self.preview_dialog
            self.preview_dialog.open = True
            self.page.update()

    def close_preview(self, e):
        if self.preview_dialog:
            self.preview_dialog.open = False
            self.page.update()

    def on_operator_change(self, e):
        if e.data == "Blend":
            self.blend_params_container.visible = True
        else:
            self.blend_params_container.visible = False
        self.update()

    def apply_operator(self, e):
        if all(self.selected_images) and self.operator_dropdown.value:
            # Open the images and convert them to numpy arrays
            img1 = self.selected_images[0].src
            img2 = self.selected_images[1].src

            # Apply the selected operator
            operator = self.operator_dropdown.value
            if operator == "Add":
                result_array = add_images(img1, img2)
            elif operator == "Subtract":
                result_array = subtract_images(img1, img2)
            elif operator == "Multiply":
                result_array = multiply_images(img1, img2)
            elif operator == "Divide":
                result_array = divide_images(img1, img2)
            elif operator == "AND":
                result_array = bitwise_and_images(img1, img2)
            elif operator == "OR":
                result_array = bitwise_or_images(img1, img2)
            elif operator == "XOR":
                result_array = bitwise_xor_images(img1, img2)
            elif operator == "Blend":
                alpha = self.alpha_slider.value
                beta = self.beta_slider.value
                gamma = float(self.gamma_input.value)
                result_array = blend_images(img1, img2, alpha, beta, gamma)
            elif operator == "Overlay":
                result_array = overlay_images(img1, img2)
            else:
                return

            # Convert the result array back to an image
            result_img = PILImage.fromarray(result_array.astype('uint8'))

            # Save the image to an in-memory buffer
            self.result_image = io.BytesIO()
            result_img.save(self.result_image, format="PNG")
            self.result_image.seek(0)

            # Update the result image
            result = Image(
                src_base64= base64.b64encode(self.result_image.getvalue()).decode("utf-8"),
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            self.result_container.content = result
            self.download_button.disabled = False
            self.update()

    def download_result(self, e):
        if self.result_image:
            # Save the image to a file
            unique_id = uuid.uuid4().hex  # Generate a UUID and get its hexadecimal representation
            # Construct the file path with the UUID
            save_path = f"operated_image_{unique_id}.png"
            with open(save_path, "wb") as dst_file:
                dst_file.write(self.result_image.getvalue())
            
            # Trigger download
            self.page.launch_url(save_path)
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image downloaded successfully!")))
        else:
            self.page.show_snack_bar(ft.SnackBar(content=Text("You do not stitch any images!")))


    def build(self):
        # Back button
        back_button = IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=colors.BLUE_400,
            on_click=self.on_back,
        )

        # Title and description
        header = Container(
            content=Column(
                controls=[
                    Text(
                        "Photo Operators",
                        size=32,
                        weight="bold",
                        color=colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    Text(
                        "Apply various operations to your images",
                        size=16,
                        color=colors.BLACK54,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=padding.all(20),
        )

        # Image containers with preview functionality
        self.image_containers = [
            Container(
                width=200,
                height=200,
                border_radius=border_radius.all(10),
                bgcolor=colors.BLUE_50,
                content=IconButton(
                    icon=ft.icons.ADD,
                    icon_color=colors.BLUE_400,
                    icon_size=40,
                    on_click=lambda _, i=i: self.add_image(i),
                ),
                alignment=alignment.center,
                on_click=lambda _, i=i: self.show_preview(i) if self.selected_images[i] else None,
                ink=True,
            )
            for i in range(2)
        ]
        self.selected_images = [None, None]

        # Operator dropdown
        operators = [
            dropdown.Option("Add"),
            dropdown.Option("Subtract"),
            dropdown.Option("Multiply"),
            dropdown.Option("Divide"),
            dropdown.Option("AND"),
            dropdown.Option("OR"),
            dropdown.Option("XOR"),
            dropdown.Option("Min"),
            dropdown.Option("Blend"),
            dropdown.Option("Overlay"),
        ]
        
        self.operator_dropdown = Dropdown(
            width=300,
            options=operators,
            label="Select Operation",
            on_change=self.on_operator_change
        )

        # Blend parameters
        self.alpha_slider = Slider(
            min=0,
            max=1,
            value=0.5,
            label="Alpha: {value}",
            width=200,
        )

        self.beta_slider = Slider(
            min=0,
            max=1,
            value=0.5,
            label="Beta: {value}",
            width=200,
        )

        self.gamma_input = TextField(
            label="Gamma",
            value="0",
            width=100,
            text_align=ft.TextAlign.RIGHT,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        # Container for blend parameters
        self.blend_params_container = Container(
            content=Column(
                controls=[
                    Row(
                        [Text("Alpha:"), self.alpha_slider],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    Row(
                        [Text("Beta:"), self.beta_slider],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    Row(
                        [Text("Gamma:"), self.gamma_input],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=10,
            ),
            visible=False,
        )

        # Apply operator button
        apply_button = ElevatedButton(
            text="Apply Operation",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.apply_operator,
        )

        # Result container
        self.result_container = Container(
            width=300,
            height=300,
            bgcolor=colors.BLACK12,
            border_radius=border_radius.all(10),
            content=Text(
                "Result will appear here",
                color=colors.BLACK54,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=alignment.center,
        )

        
        self.download_button = ElevatedButton(
            text="Download",
            icon=ft.icons.DOWNLOAD,
            on_click=self.download_result,
            disabled=True,
        )

        # Input images section
        input_images = Column(
            controls=[
                self.image_containers[0],
                self.image_containers[1],
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Operation selection and apply button
        operation_section = Column(
            controls=[
                Row(
                    [self.operator_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                self.blend_params_container,
                apply_button,
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Output section
        output_section = Column(
            controls=[
                self.result_container,
                Row(
                    controls=[self.download_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Main layout
        main_content = Row(
            controls=[
                input_images,
                operation_section,
                output_section,
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        # Full page layout
        return Container(
            content=Column(
                controls=[
                    Row([back_button], alignment=ft.MainAxisAlignment.START),
                    header,
                    main_content,
                    Container(
                        content=Text(
                            "Copyright © 2023 by Sona Enterprise",
                            size=14,
                            color=colors.BLACK54,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=padding.all(20),
                        alignment=alignment.center,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            padding=padding.all(20),
            alignment=alignment.center,
            expand=True,
        )

    def page_resize(self, e):
        self.update()

