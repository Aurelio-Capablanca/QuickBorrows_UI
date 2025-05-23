import flet as ft
import json
import requests
from components.navigation import get_nav_rail
from misc_functions.misc_api_calls import get_all_api, generate_dropdown, save_entities, delete_entity

base_url = "http://127.0.0.1:8001/api/"


def client_form(page: ft.Page):
    token = page.client_storage.get("access_token")
    nav_rail = get_nav_rail(page.route)

    type_clients = get_all_api(f"{base_url}get-type-clients", token)
    risk_clients = get_all_api(f"{base_url}get-risk-levels", token)
    name_field = ft.TextField(label="First Name", width=300)
    lastname_field = ft.TextField(label="Last Name", width=300)
    phone_field = ft.TextField(label="Phone Number", width=300)
    email_field = ft.TextField(label="Email", width=300)
    address_field = ft.TextField(label="Address", width=300)
    status_switch = ft.Switch(label="Active", value=True)
    elig_switch = ft.Switch(label="Is Eligible", value=True)
    type_dropdown = generate_dropdown(type_clients, "Client Type", "idtypeclient", "typeclient")
    risk_dropdown = generate_dropdown(risk_clients, "Risk Profile", "idrisk", "risklevel", )
    result_text = ft.Text()

    def submit_client(_):
        client_id = page.client_storage.get("edit_client_id")
        print("Client id: ", client_id)
        if client_id is not None:
            payload = {
                "idclient": client_id,
                "clientname": name_field.value,
                "clientlastname": lastname_field.value,
                "clientphone": phone_field.value,
                "clientemail": email_field.value,
                "clientaddress": address_field.value,
                "clientstatus": status_switch.value,
                "idtypeclient": int(type_dropdown.value),
                "idriskclient": int(risk_dropdown.value),
                "iselegible": elig_switch.value
            }
        else:
            payload = {
                "clientname": name_field.value,
                "clientlastname": lastname_field.value,
                "clientphone": phone_field.value,
                "clientemail": email_field.value,
                "clientaddress": address_field.value,
                "clientstatus": status_switch.value,
                "idtypeclient": int(type_dropdown.value),
                "idriskclient": int(risk_dropdown.value),
                "iselegible": elig_switch.value
            }
        try:
            response = save_entities(f"{base_url}clients/create", token, payload)
            print(response)
            if response.status_code in (200, 201):
                result_text.value = "Client Saved!"
                name_field.value = lastname_field.value = email_field.value = address_field.value = phone_field.value = ""
                status_switch.value = True
            else:
                result_text.value = f"Error: {response.status_code}"
        except Exception as e:
            result_text.value = f"Exception: {e}"
        page.client_storage.remove("edit_client_id")
        page.update()

    def populate_client_fields():
        print("void")

    clients = get_all_api(f"{base_url}clients/get-all", token)
    client_rows = []
    for client in clients:
        client_rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(client.get("clientname", ""))),
                ft.DataCell(ft.Text(client.get("clientlastname", ""))),
                ft.DataCell(ft.Text(client.get("clientphone", ""))),
                ft.DataCell(ft.Text(client.get("clientemail", ""))),
                ft.DataCell(ft.Text(client.get("iselegible", ""))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(content=ft.Text("Update"), tooltip="Edit",  # icon=ft.icons.EDIT,
                                      on_click=lambda e, a=client: populate_client_fields(a)),
                        ft.IconButton(content=ft.Text("Delete"), tooltip="Delete",  # icon=ft.icons.DELETE,
                                      on_click=lambda e, aid=client.get("idclient"): delete_entity(
                                          f"{base_url}clients/delete", token, aid, result_text, page, "Client"))
                    ])
                )
            ])
        )

    client_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Name")),
            ft.DataColumn(label=ft.Text("Last Name")),
            ft.DataColumn(label=ft.Text("Phone")),
            ft.DataColumn(label=ft.Text("Email")),
            ft.DataColumn(label=ft.Text("Is Elegible")),
            ft.DataColumn(label=ft.Text("Actions"))
        ],
        rows=client_rows
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
                address_field,
                phone_field,
                type_dropdown,
                risk_dropdown,
                status_switch,
                elig_switch,
                ft.ElevatedButton("Submit", on_click=submit_client),
                result_text,
                ft.Divider(),
                client_table
            ], spacing=10, scroll="auto")
        )
    ], expand=True)
