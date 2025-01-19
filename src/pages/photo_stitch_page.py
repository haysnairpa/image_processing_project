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
    GridView,
    Stack,
    alignment,
    border_radius,
    padding,
    colors,
    animation,
)
import base64
import io
from PIL import Image as PILImage

class PhotoStitchPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_images = []
        self.result_image = None
        self.image_grid = None
        self.result_container = None
        self.copy_button = None
        self.download_button = None
        

    def add_image(self, e):
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                for f in e.files:
                    img = Image(
                        src=f.path,
                        width=150,
                        height=150,
                        fit=ft.ImageFit.COVER,
                        border_radius=border_radius.all(10),
                    )
                    self.selected_images.append(img)
                    self.image_grid.controls.insert(-1, img)
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=True)

    def stitch_images(self, e):
        # TODO: Implement actual image stitching
        # For now, we'll just use the first image as the result
        if self.selected_images:
            self.result_image = Image(
                src=self.selected_images[0].src,
                width=760,
                height=260,
                fit=ft.ImageFit.CONTAIN,
            )
            self.result_container.content.controls[0] = self.result_image
            self.update()

    def copy_result(self, e):
        if self.result_image:
            # Convert image to base64
            with open(self.result_image.src, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            
            # Set clipboard content
            self.page.set_clipboard(f"data:image/png;base64,{encoded_string}")
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image copied to clipboard!")))
        else:
            self.page.show_snack_bar(ft.SnackBar(content=Text("You do not stitch any images!")))

    def download_result(self, e):
        if self.result_image:
            # Save the image to a file
            save_path = "stitched_image.png"
            with open(self.result_image.src, "rb") as src_file, open(save_path, "wb") as dst_file:
                dst_file.write(src_file.read())
            
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
                        "Photos Stitching",
                        size=32,
                        weight="bold",
                        color=colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    Text(
                        "Seamlessly stitch multiple photos into one panoramic image",
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

        # Image grid with add button
        self.image_grid = GridView(
            expand=1,
            max_extent=150,
            child_aspect_ratio=1,
            spacing=10,
            run_spacing=10,
            padding=20,
            controls=[
                Container(
                    width=150,
                    height=150,
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
            ],
        )

        # Center the image grid
        centered_image_grid = Container(
            content=self.image_grid,
            alignment=alignment.center,
            expand=True,
        )

        # Stitch button
        stitch_button = Container(
            content=ElevatedButton(
                text="Stitch Images",
                icon=ft.icons.PANORAMA_HORIZONTAL,
                on_click=self.stitch_images,
            ),
            alignment=alignment.center,
            padding=padding.all(20),
        )

        # Result container
        self.result_container = Container(
            height=300,
            width=800,
            bgcolor=colors.BLACK12,
            border_radius=border_radius.all(10),
            padding=padding.all(20),
            content=Stack(
                controls=[
                    Container(  # Wrap the Text in a Container for proper centering
                        content=Text(
                            "Result will appear here",
                            color=colors.BLACK54,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=alignment.center,
                        expand=True,
                    ),
                ],
            ),
            alignment=alignment.center,
        )

        # Main layout
        return Container(
            content=Column(
                controls=[
                    Row([back_button], alignment=ft.MainAxisAlignment.START),
                    header,
                    centered_image_grid,
                    stitch_button,
                    self.result_container,
                    Container(
                        content=Row(
                            controls=[
                                ElevatedButton(
                                    text="Copy Image",
                                    icon=ft.icons.COPY,
                                    on_click=self.copy_result,
                                ),
                                ElevatedButton(
                                    text="Download",
                                    icon=ft.icons.DOWNLOAD,
                                    on_click=self.download_result,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        padding=padding.symmetric(vertical=10),
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

