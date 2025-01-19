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
    alignment,
    border_radius,
    padding,
    colors,
    border,
    Stack,
)

from ..libs.background_removal import remove_background_threshold, remove_background_kmeans

class BackgroundRemovalPage(UserControl):
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
        self.selected_method = "ai"
        self.method_buttons = None
        self.preview_dialog = None

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
            preview_image = Image(
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
        if self.selected_image and self.selected_method:
            # TODO: Implement actual background removal
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
            self.page.show_snack_bar(ft.SnackBar(content=Text("Image copied to clipboard!")))

    def download_result(self, e):
        if self.result_image:
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
                    content=Text("AI-powered removal", size=14),
                    width=200,
                    height=40,
                    border=border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "ai" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("ai"),
                    bgcolor=colors.BLUE_50 if self.selected_method == "ai" else colors.WHITE,
                    data="ai",  # Store method identifier
                ),
                Container(
                    content=Text("Manual selection", size=14),
                    width=200,
                    height=40,
                    border=border.all(
                        width=2,
                        color=colors.BLUE_400 if self.selected_method == "manual" else colors.BLACK38
                    ),
                    border_radius=border_radius.all(8),
                    padding=padding.all(10),
                    alignment=alignment.center,
                    on_click=self.select_method("manual"),
                    bgcolor=colors.WHITE,
                    data="manual",  # Store method identifier
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
                            controls=[self.copy_button, self.download_button],
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