import flet as ft

def dashboard_page(page: ft.Page):
    def logout(_):
        page.client_storage.clear()
        page.go("/")

    # Handle NavigationRail change
    def on_nav_change(e):
        routes = ["/dashboard", "/admin", "/clients", "/borrow", "/funds"]
        selected = e.control.selected_index
        page.go(routes[selected])

    nav_rail = ft.NavigationRail(
        destinations=[
            ft.NavigationRailDestination(label="Home"),
            ft.NavigationRailDestination(label="Administrators"),
            ft.NavigationRailDestination(label="Clients"),
            ft.NavigationRailDestination(label="Borrow"),
            ft.NavigationRailDestination(label="Funds"),
        ],
        selected_index=0,  # You should update this dynamically depending on current route
        on_change=on_nav_change,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("QuickBorrows Dashboard"),
        actions=[
            ft.IconButton(tooltip="Profile"),
            ft.IconButton(tooltip="Logout", on_click=logout)
        ]
    )
    # Simple welcome message
    return ft.Row([nav_rail, ft.Text("Welcome!", size=24)], expand=True)
