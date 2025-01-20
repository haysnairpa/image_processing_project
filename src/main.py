import flet as ft
from flet import Page, ScrollMode, View
from pages.home_page import HomePage

def main(page: Page):
    # Konfigurasi page
    page.title = "Sona Picture Processing"
    page.padding = 0  # Remove padding for full-width hero
    page.bgcolor = "#F5F5F5"
    page.scroll = ScrollMode.AUTO
    
    # Inisialisasi routing
    def route_change(route):
        page.views.clear()
        
        if page.route == "/" or not page.route:
            # Homepage
            home = HomePage()
            page.views.append(
                View(
                    "/",
                    [home],
                    padding=0,
                    bgcolor="#F5F5F5",
                )
            )
        
        page.update()

    # Set up routing
    page.on_route_change = route_change
    
    # Initialize with homepage
    home = HomePage()
    page.add(home)
    
    # Handle page resize for responsive design
    page.on_resize = home.page_resize
    
    page.update()

ft.app(target=main, view=ft.WEB_BROWSER)

