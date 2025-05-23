from operator import concat

import flet as ft
import json
import requests
from components.navigation import get_nav_rail

base_url = "http://127.0.0.1:8001/api/"


def admin_form(page: ft.Page):
    token = page.client_storage.get("access_token")

    nav_rail = get_nav_rail(page.route)
    # --- Form Fields ---
    name_field = ft.TextField(label="First Name", width=300)
    lastname_field = ft.TextField(label="Last Name", width=300)
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    phone_field = ft.TextField(label="Phone Number", width=300)
    status_switch = ft.Switch(label="Active", value=True)
    result_text = ft.Text()

    def submit_admin(_):
        payload = {
            "adminname": name_field.value,
            "adminlastname": lastname_field.value,
            "adminemail": email_field.value,
            "adminpass": password_field.value,
            "adminphone": phone_field.value,
            "adminstatus": status_switch.value,
        }
        try:
            response = requests.post(
                concat(base_url, "/admins/create"),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            if response.status_code in (200, 201):
                result_text.value = "✅ Administrator created!"
                name_field.value = lastname_field.value = email_field.value = password_field.value = phone_field.value = ""
                status_switch.value = True
            else:
                result_text.value = f"❌ Error: {response.status_code}"
        except Exception as e:
            result_text.value = f"❌ Exception: {e}"
        page.update()

    def populate_admin_fields(admin):
        name_field.value = admin.get("adminname", "")
        lastname_field.value = admin.get("adminlastname", "")
        email_field.value = admin.get("adminemail", "")
        phone_field.value = admin.get("adminphone", "")
        status_switch.value = admin.get("adminstatus", False)
        # store admin id in hidden form-level variable
        page.client_storage.set("edit_admin_id", str(admin.get("adminid", "")))
        page.update()

    def get_all_users():
        url = "http://127.0.0.1:8001/api/admins/get-all"
        try:
            result = requests.get(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                                  json={"page": 0, "limit": 10})
            print(result)
            print(result.json()["detail"]["data"])
            return result.json()["detail"]["data"]
        except Exception as ex:
            print(ex)
            return None

    def delete_admin(admin_id):
        try:
            response = requests.delete(
                f"{base_url}admins/delete/{admin_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 204:
                result_text.value = "🗑️ Administrator deleted."
                page.go(page.route)  # simple way to refresh the page
            else:
                result_text.value = f"❌ Delete failed: {response.status_code}"
        except Exception as e:
            result_text.value = f"❌ Exception: {e}"
        page.update()

    admins = get_all_users()
    admin_rows = []

    for admin in admins:
        admin_rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(admin.get("adminname", ""))),
                ft.DataCell(ft.Text(admin.get("adminemail", ""))),
                ft.DataCell(ft.Text(admin.get("adminphone", ""))),
                ft.DataCell(ft.Text(admin.get("adminstatus", ""))),
                ft.DataCell(ft.Text(admin.get("datecreated", ""))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(content=ft.Text("Update"), tooltip="Edit",#icon=ft.icons.EDIT,
                                      on_click=lambda e, a=admin: populate_admin_fields(a)),
                        ft.IconButton(content=ft.Text("Delete"), tooltip="Delete",#icon=ft.icons.DELETE,
                                      on_click=lambda e, aid=admin.get("idadministrator"): delete_admin(aid))
                    ])
                )
            ])
        )

    admin_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Phone")),
            ft.DataColumn(label=ft.Text("Status")),
            ft.DataColumn(label=ft.Text("Created")),
            ft.DataColumn(label=ft.Text("Actions"))
        ],
        rows=admin_rows
    )

    return ft.Container(
        content=ft.Column([
            # nav_rail,
            ft.Text("Manage Administrators", size=20, weight=ft.FontWeight.BOLD),
            name_field,
            lastname_field,
            email_field,
            password_field,
            phone_field,
            status_switch,
            ft.ElevatedButton("Submit", on_click=submit_admin),
            result_text,
            ft.Divider(),
            admin_table
        ], spacing=10),
        padding=20,
        expand=True
    )
