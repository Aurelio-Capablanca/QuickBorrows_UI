import flet as ft
import requests

def login_page(page: ft.Page):

    username_field = ft.TextField(label="Username", width=300)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)

    def login_handler(e):
        username = username_field.value
        password = password_field.value
        url = "http://127.0.0.1:8001/login/"
        try:
            response = requests.post(url, json={"username": username, "password": password})
            if response.status_code == 200:
                token = response.json()["access_token"]
                print(token)
                page.snack_bar = ft.SnackBar(ft.Text("Login Successful!"), bgcolor="green")
                page.snack_bar.open = True
                page.update()
            else:
                print("Error")
                page.snack_bar = ft.SnackBar(ft.Text("Login Failed!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
        except Exception as ex:
            print(ex)

    login_btn = ft.ElevatedButton("Login", on_click=login_handler)

    return ft.Column(
        controls=[
            ft.Text("QuickBorrows Login", size=24, weight=ft.FontWeight.BOLD),
            username_field,
            password_field,
            login_btn
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
