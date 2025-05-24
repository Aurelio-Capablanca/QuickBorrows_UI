import flet as ft
from components.navigation import get_nav_rail
from misc_functions.misc_api_calls import get_all_api, delete_entity, save_entities

base_url = "http://127.0.0.1:8001/api/"


def admin_form(page: ft.Page):
    page.client_storage.set("edit_admin_id", 0)
    token = page.client_storage.get("access_token")
    nav_rail = get_nav_rail(page.route)

    name_field = ft.TextField(label="First Name", width=300)
    lastname_field = ft.TextField(label="Last Name", width=300)
    email_field = ft.TextField(label="Email", width=300)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300)
    phone_field = ft.TextField(label="Phone Number", width=300)
    status_switch = ft.Switch(label="Active", value=True)
    result_text = ft.Text()

    def submit_admin(_):
        admin_id = page.client_storage.get("edit_admin_id")
        print("Admin id: ", admin_id)
        if admin_id != 0:
            payload = {
                "idadministrator": admin_id,
                "adminname": name_field.value,
                "adminlastname": lastname_field.value,
                "adminemail": email_field.value,
                "adminpass": password_field.value,
                "adminphone": phone_field.value,
                "adminstatus": status_switch.value,
            }
        else:
            payload = {
                "adminname": name_field.value,
                "adminlastname": lastname_field.value,
                "adminemail": email_field.value,
                "adminpass": password_field.value,
                "adminphone": phone_field.value,
                "adminstatus": status_switch.value,
            }
        try:
            response = save_entities(f"{base_url}admins/create", token, payload)
            print("Admin Response", response.json()["detail"])
            if response.status_code in (200, 201):
                result_text.value = "Administrator saved!"
                name_field.value = lastname_field.value = email_field.value = password_field.value = phone_field.value = ""
                status_switch.value = True
            else:
                result_text.value = f"Error: {response.status_code}"
        except Exception as e:
            result_text.value = f"Exception: {e}"
        page.client_storage.set("edit_admin_id", 0)
        page.update()

    def populate_admin_fields(admin_array):
        name_field.value = admin_array.get("adminname", "")
        lastname_field.value = admin_array.get("adminlastname", "")
        email_field.value = admin_array.get("adminemail", "")
        phone_field.value = admin_array.get("adminphone", "")
        status_switch.value = admin_array.get("adminstatus", False)
        page.client_storage.set("edit_admin_id", str(admin_array.get("idadministrator", 0)))
        page.update()

    admins = get_all_api(f"{base_url}admins/get-all", token)
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
                        ft.IconButton(content=ft.Text("Update"), tooltip="Edit",  # icon=ft.icons.EDIT,
                                      on_click=lambda e, a=admin: populate_admin_fields(a)),
                        ft.IconButton(content=ft.Text("Delete"), tooltip="Delete",  # icon=ft.icons.DELETE,
                                      on_click=lambda e, aid=admin.get("idadministrator"): delete_entity(
                                          f"{base_url}admins/delete", token, aid, result_text, page, "Administrator"))
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
    return ft.Row([
        nav_rail,
        ft.VerticalDivider(width=1),
        ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
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
            ], spacing=10, scroll="auto")
        )
    ], expand=True)
