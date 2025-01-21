import flet as ft
from flet import (
    UserControl,
    Container,
    Row,
    Column,
    Text,
    Image,
    ScrollMode,
    alignment,
    border_radius,
    padding,
    colors,
    IconButton,
    animation,
    transform,
    Stack,
)
from .basic_ops import PhotoEditorPage
from .photo_stitch_page import PhotoStitchPage
from .background_removal_page import BackgroundRemovalPage
from .photo_compression_page import PhotoCompressionPage
from .photo_operators_page import PhotoOperatorsPage

class HomePage(UserControl):
    def __init__(self):
        super().__init__()
        self.hero_section = None
        self.buttons_header = None
        self.buttons_section = None
        self.sample_header = None
        self.gallery = None
        self.footer = None

    def create_card(self, icon: str, title: str, subtitle: str, onclick, width=180, height=180):
        return Container(
            width=width,
            height=height,
            border_radius=border_radius.all(20),
            bgcolor=colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=colors.BLACK12,
                offset=ft.Offset(0, 4),
            ),
            animate=animation.Animation(300, "easeOutQuad"),
            content=Column(
                controls=[
                    IconButton(
                        icon=icon,
                        icon_color=colors.BLUE_400,
                        icon_size=40,
                        on_click = onclick
                    ),
                    Text(title, size=16, color=colors.BLACK87, weight="bold"),
                    Text(subtitle, size=12, color=colors.BLACK54, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=alignment.center,
            on_click=onclick,
        )
    
    def navigate_to_photos_editor(self, e):
        self.page.clean()
        page = PhotoEditorPage(
            self.page,
            lambda _: self.show_home()
        )
        self.page.add(page)
    
    def navigate_to_photos_stitch(self, e):
        self.page.clean()
        page = PhotoStitchPage(
            self.page,
            lambda _: self.show_home())
        self.page.add(page)

    def navigate_to_photo_compression(self, e):
        self.page.clean()
        page = PhotoCompressionPage(
            self.page,
            lambda _: self.show_home())
        self.page.add(page)

    def navigate_to_photos_operator(self, e):
        self.page.clean()
        page = PhotoOperatorsPage(
            self.page,
            lambda _: self.show_home())
        self.page.add(page)

    def navigate_to_background_removal(self, e):
        self.page.clean()
        page = BackgroundRemovalPage(
            self.page, 
            lambda _: self.show_home())
        self.page.add(page)

    def show_home(self):
        self.page.clean()
        self.page.add(self)
        self.page.update()

    def create_header(self, title: str):
        return Container(
            padding=padding.symmetric(horizontal=30, vertical=20),
            content=Text(
                title,
                size=24,
                weight="bold",
                color=colors.BLACK87,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=alignment.center,
        )

    def build(self):
        # Hero section with background image and title
        self.hero_section = Container(
            width=1920,
            height=540,  # This will be adjusted dynamically
            content=Stack(
                controls=[
                    Image(
                        src="https://picsum.photos/1920/1080",
                        width=1920,
                        height=540,
                        fit=ft.ImageFit.COVER,
                    ),
                    Container(
                        width=1920,
                        height=540,
                        bgcolor=ft.colors.with_opacity(0.5, "#000000"),  # Dark overlay
                    ),
                    Container(
                        content=Column(
                            controls=[
                                Text(
                                    "SONA Picture Processing",
                                    size=64,
                                    weight="bold",
                                    color=colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                Text(
                                    "Transform your images with powerful processing tools",
                                    size=22,
                                    color=colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        alignment=alignment.center,
                    ),
                ],
            ),
        )

        self.buttons_header = self.create_header("What do you want to create?")

        # Buttons section
        self.buttons_section = Container(
            padding=padding.all(30),
            content=Row(
                controls=[
                    self.create_card(
                        ft.icons.AUTO_AWESOME, "Photo Editor", 
                        "Enhance photos instantly with powerful editing tools", 
                        lambda e: self.navigate_to_photos_editor(e)),
                    self.create_card(
                        ft.icons.FILTER, "Photo Operators", 
                        "Apply AI-powered filters to transform your images", 
                        lambda e: self.navigate_to_photos_operator(e)),
                    self.create_card(
                        ft.icons.FACE_RETOUCHING_NATURAL, "Photo Compression", 
                        "Compress photos without compromising quality", 
                        lambda e: self.navigate_to_photo_compression(e)),
                    self.create_card(
                        ft.icons.STYLE, "Background Removal", 
                        "Remove backgrounds effortlessly for creative designs", 
                        lambda e: self.navigate_to_background_removal(e)),
                    self.create_card(
                        ft.icons.ADD_PHOTO_ALTERNATE, "Photo Stitching", 
                        "Seamlessly stitch multiple photos into one", 
                        lambda e: self.navigate_to_photos_stitch(e)),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        )

        # Recent Creation section header
        self.sample_header = self.create_header("Sample Creations")

        # Image gallery
        self.gallery = Container(
            padding=padding.symmetric(horizontal=30),
            content=Row(
                scroll=ScrollMode.AUTO,
                controls=[
                    Image(src="https://picsum.photos/280/180?1", width=280, height=180, border_radius=border_radius.all(15), fit=ft.ImageFit.COVER),
                    Image(src="https://picsum.photos/280/180?2", width=280, height=180, border_radius=border_radius.all(15), fit=ft.ImageFit.COVER),
                    Image(src="https://picsum.photos/280/180?3", width=280, height=180, border_radius=border_radius.all(15), fit=ft.ImageFit.COVER),
                    Image(src="https://picsum.photos/280/180?4", width=280, height=180, border_radius=border_radius.all(15), fit=ft.ImageFit.COVER),
                    Image(src="https://picsum.photos/280/180?5", width=280, height=180, border_radius=border_radius.all(15), fit=ft.ImageFit.COVER),
                ],
                spacing=20,
            ),
        )

        # Footer
        self.footer = Container(
            content=Text(
                "Copyright © 2023 by Sona Enterprise",
                size=14,
                color=colors.BLACK54,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=padding.all(20),
            alignment=alignment.center,
        )

        # Main layout
        return Container(
            content=Column(
                controls=[
                    self.hero_section,
                    self.buttons_header,
                    self.buttons_section,
                    self.sample_header,
                    self.gallery,
                    self.footer,
                ],
                spacing=20,
                scroll=ScrollMode.AUTO,
            ),
            expand=True,
        )

    def page_resize(self, e):
        # Update hero width and height
        new_width = e.window_width
        new_height = min(int(e.window_height * 0.5), 540)  # Max 50% of window height, capped at 540px

        self.hero_section.width = new_width
        self.hero_section.height = new_height
        self.hero_section.content.controls[0].width = new_width  # Update image width
        self.hero_section.content.controls[0].height = new_height  # Update image height
        self.hero_section.content.controls[1].width = new_width  # Update overlay width
        self.hero_section.content.controls[1].height = new_height  # Update overlay height
        
        # Make buttons wrap on smaller screens
        self.buttons_section.content.wrap = e.window_width < 1000
        
        # Adjust spacing and padding
        if e.window_width < 600:
            self.buttons_section.padding = padding.all(15)
            self.buttons_section.content.spacing = 10
            self.gallery.content.spacing = 10
        else:
            self.buttons_section.padding = padding.all(30)
            self.buttons_section.content.spacing = 20
            self.gallery.content.spacing = 20
        
        self.update()

