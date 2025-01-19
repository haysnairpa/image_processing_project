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
)

class PhotoCompressionPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_image = None
        self.result_image = None
        self.image_container = None
        self.result_container = None
        self.copy_button = None
        self.download_button = None
        self.compression_slider = None

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
            # TODO: Implement actual image compression
            # For now, we'll just use the original image as the result
            self.result_image = Image(
                src=self.selected_image.src,
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN,
            )
            self.result_container.content = self.result_image
            self.copy_button.disabled = False
            self.download_button.disabled = False
            self.update()

    def copy_result(self, e):
        if self.result_image:
            # TODO: Implement copy functionality
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image copied to clipboard!")))

    def download_result(self, e):
        if self.result_image:
            # TODO: Implement download functionality
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image downloaded successfully!")))

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

        # Image container
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
        )

        # Compression slider
        self.compression_slider = Slider(
            min=0,
            max=100,
            divisions=10,
            label="{value}%",
            value=50,
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

        # Copy and Download buttons
        self.copy_button = ElevatedButton(
            text="Copy Image",
            icon=ft.icons.COPY,
            on_click=self.copy_result,
            disabled=True,
        )
        self.download_button = ElevatedButton(
            text="Download",
            icon=ft.icons.DOWNLOAD,
            on_click=self.download_result,
            disabled=True,
        )

        # Main layout
        return Container(
            content=Column(
                controls=[
                    Row([back_button], alignment=ft.MainAxisAlignment.START),
                    header,
                    Row(
                        [self.image_container, self.compression_slider],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    compress_button,
                    self.result_container,
                    Row(
                        [self.copy_button, self.download_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
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
