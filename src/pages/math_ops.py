from flet import ElevatedButton, View, Text

def math_operation_page(page):
    def back_to_home(e):
        page.views.pop()
        page.update()

    return View(
        controls=[
            Text("Mathematical Operations", size=20, weight="bold"),
            ElevatedButton("Back to Home", on_click=back_to_home),
            # Ur Code
        ]
    )