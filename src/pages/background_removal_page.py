import base64
import uuid
import flet as ft
from flet import (
    UserControl,
    Container,
    Row,
    Column,
    Text,
    IconButton,
    ElevatedButton,
    alignment,
    border_radius,
    padding,
    colors,
    border,
    Stack,
    FilePickerResultEvent,
    SnackBar,
)
import numpy as np
import io
from PIL import Image
from libs.background_removal import remove_background_threshold, remove_background_kmeans

class BackgroundRemovalPage(UserControl):
    def __init__(self, page, on_back):
        super().__init__()
        self.page = page
        self.on_back = on_back
        self.selected_image = None
        self.result_image = None
        self.image_container = None
        self.result_container = None
        self.download_button = None
        self.selected_method = "KMeans"
        self.method_buttons = None
        self.preview_dialog = None

    def add_image(self, e):
        def on_result(e: FilePickerResultEvent):
            if e.files:
                self.selected_image = ft.Image(
                    src=e.files[0].path,
                    width=300,
                    height=300,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=border_radius.all(10),
                )
                self.image_container.content = Stack([
                    self.selected_image,
                    Container(
                        content=IconButton(
                            icon=ft.icons.CLOSE,
                            icon_color=colors.RED_400,
                            icon_size=20,
                            on_click=self.clear_image,
                        ),
                        alignment=alignment.top_right,
                        margin=ft.margin.only(top=-10, right=-10),
                    )
                ])
                self.update()

        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        file_picker.pick_files(allow_multiple=False)

    def clear_image(self, e):
        self.selected_image = None
        self.image_container.content = IconButton(
            icon=ft.icons.ADD,
            icon_color=colors.BLUE_400,
            icon_size=40,
            on_click=self.add_image,
        )
        self.update()

    def select_method(self, method):
        def handle_click(e):
            self.selected_method = method
            # Update button styles
            for btn in self.method_buttons.controls:
                if btn.data == method:
                    btn.bgcolor = colors.BLUE_50
                    btn.border = border.all(width=2, color=colors.BLUE_400)
                else:
                    btn.bgcolor = colors.WHITE
                    btn.border = border.all(width=2, color=colors.BLACK38)
            self.update()
        return handle_click

    def show_preview(self, e):
        if self.selected_image:
            preview_image = ft.Image(
                src=self.selected_image.src,
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

    def remove_background(self, e):
        if self.selected_image:
            # Remove the background based on the selected method
            if self.selected_method == "Threshold":
                result_array = remove_background_threshold(self.selected_image.src)
            else:  # KMeans
                result_array = remove_background_kmeans(self.selected_image.src)

            # Convert the result array back to an image (assuming it's in RGB)
            result_img = Image.fromarray(result_array.astype('uint8'))

            # Convert image to RGBA to add transparency (alpha channel)
            result_img = result_img.convert("RGBA")
            result_array = np.array(result_img)

            # Create a mask where white pixels are found (or almost white)
            # Threshold values can be adjusted for specific use cases
            lower_white = np.array([200, 200, 200, 255])  # White pixel threshold
            upper_white = np.array([255, 255, 255, 255])

            # Create a mask to find white pixels
            white_mask = np.all((result_array[:, :, :3] >= lower_white[:3]) & (result_array[:, :, :3] <= upper_white[:3]), axis=-1)

            # Set the alpha channel to 0 (transparent) for white pixels
            result_array[white_mask] = [0, 0, 0, 0]  # Black with full transparency

            # Convert the numpy array back to an image
            result_img = Image.fromarray(result_array)

            # Save the image to an in-memory buffer
            self.result_image = io.BytesIO()
            result_img.save(self.result_image, format="PNG")
            self.result_image.seek(0)

            # Update the result image
            result = ft.Image(
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
            save_path = f"background_removed_image_{unique_id}.png"
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
                        "Background Removal",
                        size=32,
                        weight="bold",
                        color=colors.BLACK87,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    Text(
                        "Remove backgrounds effortlessly for creative designs",
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

        # Method selection with modern rectangle buttons
        self.method_buttons = Row(
            controls=[
                Container(
                    content=Text("Threshold Segmentation", size=14),
                    width=200,
                    height=40,
                    border=border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "Threshold" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("Threshold"),
                    bgcolor=colors.BLUE_50 if self.selected_method == "Threshold" else colors.WHITE,
                    data="Threshold",  # Store method identifier
                ),
                Container(
                    content=Text("KMeans Segmentation", size=14),
                    width=200,
                    height=40,
                    border=border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "KMeans" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("KMeans"),
                    bgcolor=colors.WHITE,
                    data="KMeans",  # Store method identifier
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Remove background button
        remove_button = ElevatedButton(
            text="Remove Background",
            icon=ft.icons.CONTENT_CUT,
            on_click=self.remove_background,
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
                # Center: Method Selection and Remove Button
                Column(
                    controls=[
                        self.method_buttons,
                        remove_button,
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

