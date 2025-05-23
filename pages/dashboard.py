import flet as ft

from components.navigation import get_nav_rail


def dashboard_page(page: ft.Page):
    def logout(_):
        page.client_storage.clear()
        page.go("/")
    nav_rail = get_nav_rail(page.route)
    page.appbar = ft.AppBar(
        title=ft.Text("QuickBorrows Dashboard"),
        actions=[
            ft.IconButton(tooltip="Profile"),
            ft.IconButton(tooltip="Logout", on_click=logout)
        ]
    )
    return ft.Row([nav_rail, ft.Text("Welcome!", size=24)], expand=True)
