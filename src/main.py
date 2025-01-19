from flet import Page, ElevatedButton, Column, View, Container, Text
import flet as ft
from pages.basic_ops import basic_operations_page
from pages.math_ops import math_operation_page
from pages.restoration_ops import restoration_page
from pages.matching import matching_page

def main(page: Page):
    def navigate_to_functionality(e):
        function = e.control.data
        if function == "Basic Operations":
            page.views.append(basic_operations_page(page))
        elif function == "Math Operations":
            page.views.append(math_operation_page(page))
        elif function == "Restoration":
            page.views.append(restoration_page(page))
        elif function == "Matching":
            page.views.append(matching_page(page))
        # Navigate to other function
        page.update()

    def back_to_home(e):
        page.views.pop()
        page.update()

    # Main Page
    home_view = View(
        controls=[
            Container(
                content=Column(
                    [
                        Text("Image Processing Project", size=24, weight="bold"),
                        ElevatedButton("Basic Operations", data="Basic Operations", on_click=navigate_to_functionality),
                        ElevatedButton("Mathematical Operations", data="Math Operations", on_click=navigate_to_functionality),
                        ElevatedButton("Transforms & Filtering", data="Transforms", on_click=navigate_to_functionality),
                        ElevatedButton("Image Enhancement", data="Enhancement", on_click=navigate_to_functionality),
                        ElevatedButton("Image Compression", data="Compression", on_click=navigate_to_functionality),
                        ElevatedButton("Image Segmentation", data="Segmentation", on_click=navigate_to_functionality),
                        ElevatedButton("Binary Processing", data="Binary", on_click=navigate_to_functionality),
                        ElevatedButton("Image Restoration", data="Restoration", on_click=navigate_to_functionality),
                        ElevatedButton("Image Matching", data="Matching", on_click=navigate_to_functionality),
                    ],
                    spacing=10,
                ),
                alignment=ft.alignment.center,
            )
        ]
    )
    page.views.append(home_view)
    page.update()

ft.app(target=main)