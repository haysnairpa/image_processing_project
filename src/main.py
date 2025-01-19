import flet as ft
from flet import Page, ScrollMode
from pages.home_page import HomePage

def main(page: Page):
    page.title = "Sona Picture Processing"
    page.padding = 0  # Remove padding for full-width hero
    page.bgcolor = "#F5F5F5"
    page.scroll = ScrollMode.AUTO

    home_page = HomePage()
    page.add(home_page)

    page.on_resize = home_page.page_resize

ft.app(target=main)

