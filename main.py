import flet as ft

from pages.admin_form import admin_form
from pages.borrow_form import borrow_form
from pages.client_form import client_form
from pages.dashboard import dashboard_page
from pages.login import login_page


def main(page: ft.Page):
    def route_change(e):
        page.views.clear()
        route = page.route
        ##page.client_storage.remove("access_token")
        jwt_token = page.client_storage.get("access_token")
        if route == "/":
            page.views.append(
                ft.View("/", [login_page(page)])
            )
            page.title = "QuickBorrows - Login"
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.padding = 50
            page.theme_mode = ft.ThemeMode.LIGHT

        elif route == "/dashboard":
            print("are you there ? ",jwt_token)
            if not jwt_token:
                page.go("/")
                return
            page.views.append(
                ft.View("/dashboard", [dashboard_page(page)])
            )
            page.title = "QuickBorrows - Dashboard"
        elif route == "/admin":
            if not jwt_token:
                page.go("/")
                return
            page.views.append(
                ft.View("/admin", [admin_form(page)])
            )
            page.title = "QuickBorrows - Administrators"
        elif route == "/client":
            if not jwt_token:
                page.go("/")
                return
            page.views.append(
                ft.View("/admin", [client_form(page)])
            )
            page.title = "QuickBorrows - Clients"
        elif route == "/borrow":
            if not jwt_token:
                page.go("/")
                return
            page.views.append(
                ft.View("/admin", [borrow_form(page)])
            )
            page.title = "QuickBorrows - Borrows"
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=5173)
