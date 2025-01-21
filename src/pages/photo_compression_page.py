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
    Slider,
    alignment,
    border_radius,
    padding,
    colors,
    FilePickerResultEvent,
    FilePicker,
)

import numpy as np
from PIL import Image as PILImage

from libs.compression_ops import compress_image_dct, compress_image_rle

class PhotoCompressionPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_image = None
        self.result_image = None
        self.image_container = None
        self.result_container = None
        self.download_button = None
        self.method_buttons = None
        self.selected_method = "RLE"

    def add_image(self, e):
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_image = Image(
                    src=e.files[0].path,
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=border_radius.all(10),
                )
                self.image_container.content = self.selected_image
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=False)

    def compress_image(self, e):
        if self.selected_image:
            # Open the image and convert it to a numpy array
            img = PILImage.open(self.selected_image.src).convert("RGB")
            img_array = np.array(img)

            # Compress the image based on the selected method
            if self.selected_method == "RLE":
                compressed_array = compress_image_rle(img_array)  # Call RLE compression function
            else:  # DCT
                compressed_array = compress_image_dct(img_array)  # Call DCT compression function

            # Convert the compressed array back to an image
            compressed_img = PILImage.fromarray(compressed_array.astype('uint8'))

            # Save the compressed image in a high-compression format (JPEG with quality 85)
            self.result_image = io.BytesIO()
            compressed_img.save(self.result_image, format="JPEG", quality=85)
            self.result_image.seek(0)

            # Update the UI with the result image
            result = Image(
                src_base64=base64.b64encode(self.result_image.getvalue()).decode("utf-8"),
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
            save_path = f"compressed_image_{unique_id}.png"
            with open(save_path, "wb") as dst_file:
                dst_file.write(self.result_image.getvalue())
            
            # Trigger download
            self.page.launch_url(save_path)
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image downloaded successfully!")))
        else:
            self.page.show_snack_bar(ft.SnackBar(content=Text("You do not stitch any images!")))

    def save_file_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            img = Image.open(self.result_image.src)
            img.save(e.path)
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image saved successfully!")))

    def show_preview(self, e):
        # Add your preview logic here
        print("Image preview clicked!")
        pass

    def select_method(self, method):
        def handle_click(e):
            self.selected_method = method
            # Update button styles
            for btn in self.method_buttons.controls:
                if btn.data == method:
                    btn.bgcolor = colors.BLUE_50
                    btn.border = ft.border.all(width=2, color=colors.BLUE_400)
                else:
                    btn.bgcolor = colors.WHITE
                    btn.border = ft.border.all(width=2, color=colors.BLACK38)
            self.update()
        return handle_click

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
                        "Photo Compression",
                        size=32,
                        weight="bold",
                        color=colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    Text(
                        "Compress photos without compromising quality",
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

        # Image container with preview functionality
        self.image_container = Container(
            width=300,
            height=300,
            border_radius=border_radius.all(10),
            bgcolor=colors.BLUE_50,
            content=IconButton(
                icon=ft.icons.ADD,
                icon_color=colors.BLUE_400,
                icon_size=40,
                on_click=self.add_image,
            ),
            alignment=alignment.center,
            on_click=self.show_preview,
            ink=True,
        )

        self.method_buttons = Row(
            controls=[
                Container(
                    content=Text("Run Length Encoding", size=14),
                    width=200,
                    height=40,
                    border=ft.border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "RLE" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("RLE"),
                    bgcolor=colors.BLUE_50 if self.selected_method == "RLE" else colors.WHITE,
                    data="RLE",  # Store method identifier
                ),
                Container(
                    content=Text("Discreate Cosine Transform", size=14),
                    width=200,
                    height=40,
                    border=ft.border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "DCT" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("DCT"),
                    bgcolor=colors.WHITE,
                    data="DCT",  # Store method identifier
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Compress button
        compress_button = ElevatedButton(
            text="Compress Image",
            icon=ft.icons.COMPRESS,
            on_click=self.compress_image,
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

        # Main layout with horizontal arrangement
        main_content = Row(
            controls=[
                # Left: Input Image
                self.image_container,
                # Center: Compression Slider and Compress Button
                Column(
                    controls=[
                        self.method_buttons,
                        compress_button,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # Right: Output Image and Buttons
                Column(
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
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=40,
        )

        # Main layout
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

