import flet as ft
from pages.login import login_page

def main(page: ft.Page):
    page.title = "QuickBorrows - Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 50
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(login_page(page))
    page.update()

#ft.app(target=main, view=ft.WEB_BROWSER, port=5173)

# ft.app(target=main)
#
if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=5173)