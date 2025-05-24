import flet as ft

# Define shared routes and labels
NAV_ROUTES = [
    ("/dashboard", "Home"),
    ("/admin", "Administrators"),
    ("/client", "Clients"),
    ("/borrow", "Borrow")
]

def get_nav_rail(current_route: str, on_change=None) -> ft.NavigationRail:
    try:
        selected_index = [r[0] for r in NAV_ROUTES].index(current_route)
    except ValueError:
        selected_index = 0

    return ft.NavigationRail(
        destinations=[ft.NavigationRailDestination(label=label) for _, label in NAV_ROUTES],
        selected_index=selected_index,
        on_change=on_change or default_nav_change,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
    )

# Default behavior: go to route based on selected index
def default_nav_change(e):
    page = e.page
    page.go(NAV_ROUTES[e.control.selected_index][0])
