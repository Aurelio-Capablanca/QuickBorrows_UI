import flet as ft
import datetime

def create_date_picker(page: ft.Page):
    selected_date = {"value": None}
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # def handle_change(e):
    #     page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))

    def handle_change(e):
        selected_date["value"] = e.control.value
        page.update()

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    def get_selected_date():
        return selected_date["value"].strftime('%Y-%m-%d') if selected_date["value"] else None

    button = ft.ElevatedButton(
            "Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    last_date=datetime.datetime(year=2025, month=10, day=1),
                    on_change=handle_change,
                    on_dismiss=handle_dismissal,
                )
            ),
        )

    return button, get_selected_date