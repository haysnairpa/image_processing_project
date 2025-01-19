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
import cv2
import numpy as np
import uuid

class PhotoStitchPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_images = []
        self.result_image = None
        self.image_grid = None
        self.result_container = None
        self.preview_dialog = None        

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
                    self.add_image_to_grid(img)
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=True)

    def add_image_to_grid(self, img):
        container = Container(
            content=Stack(
                controls=[
                    img,
                    IconButton(
                        icon=ft.icons.CLOSE,
                        icon_color=colors.RED_400,
                        icon_size=20,
                        on_click=lambda _: self.remove_image(img),
                        top=0,
                        right=0,
                    ),
                ],
                width=150,
                height=150,

            ),
            on_click=lambda _: self.show_preview(img) 
            
        )
        self.image_grid.controls.insert(-1, container)

    def remove_image(self, img):
        self.selected_images.remove(img)
        for control in self.image_grid.controls:
            if isinstance(control.content, Stack) and control.content.controls[0] == img:
                self.image_grid.controls.remove(control)
                break
        self.update()

    def show_preview(self, img):
        self.preview_dialog = ft.AlertDialog(
            content=Image(src=img.src, width=400, height=400, fit=ft.ImageFit.CONTAIN),
            actions=[
                ft.TextButton("Close", on_click=self.close_preview),
            ],
        )
        self.page.dialog = self.preview_dialog
        self.preview_dialog.open = True
        self.page.update()

    def close_preview(self, e):
        self.preview_dialog.open = False
        self.page.update()

    def stitch_images(self, e):
        if len(self.selected_images) < 2:
            self.page.show_snack_bar(ft.SnackBar(content=Text("Please select at least two images to stitch.")))
            return

        imgs = []
        for img in self.selected_images:
            pil_img = PILImage.open(img.src)
            cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            imgs.append(cv_img)

        stitchy = cv2.Stitcher.create()
        (status, output) = stitchy.stitch(imgs)

        if status != cv2.STITCHER_OK:
            self.page.show_snack_bar(ft.SnackBar(content=Text("Stitching unsuccessful")))
        else:
            # Convert the output image to PIL Image
            output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

            output_pil = PILImage.fromarray(output_rgb)
            # Save the stitched image

            # Save the image to an in-memory buffer
            self.result_image = io.BytesIO()
            output_pil.save(self.result_image, format="PNG")
            self.result_image.seek(0)
            
            result = Image(
                src_base64= base64.b64encode(self.result_image.getvalue()).decode("utf-8"),
                width=760,
                height=260,
                fit=ft.ImageFit.CONTAIN,
            )
            self.result_container.content.controls[0] = result
            self.update()

    def download_result(self, e):
        if self.result_image:
            # Save the image to a file
            unique_id = uuid.uuid4().hex  # Generate a UUID and get its hexadecimal representation
            # Construct the file path with the UUID
            save_path = f"stitched_image_{unique_id}.png"
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
                    Container(
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

