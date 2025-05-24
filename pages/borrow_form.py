import flet as ft

from components.datepicker import create_date_picker
from components.navigation import get_nav_rail
from misc_functions.misc_api_calls import get_all_api, generate_dropdown, save_entities, delete_entity

base_url = "http://127.0.0.1:8001/api/"


def borrow_form(page: ft.Page):
    page.client_storage.set("edit_borrow_id", 0)
    token = page.client_storage.get("access_token")
    nav_rail = get_nav_rail(page.route)

    payment_type = get_all_api(f"{base_url}get-payment-methods", token)
    clients_all = get_all_api(f"{base_url}clients/get-all", token)
    print(payment_type, " ", clients_all)
    # ---- Borrows fields -----
    borrow_amount = ft.TextField(label="Borrow Amount", keyboard_type="number", width=200)
    date_taken, value_date_taken = create_date_picker(page)
    payment_type_form = generate_dropdown(payment_type, "Payment Type", "idmethod", "paymentmethod")
    id_client_form = generate_dropdown(clients_all, "Client", "idclient", "clientname")
    is_active = ft.Checkbox(label="Is Active", value=True)
    # --- Bill Conditions ---
    num_payments = ft.TextField(label="Number of Payments (comma-separated)", width=300)
    payments_of = ft.TextField(label="Amounts per Payment (comma-separated)", width=300)
    generate_to_fill = ft.Checkbox(label="Generate Extra Payments to Fill", value=False)
    result_text = ft.Text()

    def submit_borrow(_):
        borrow_id = page.client_storage.get("edit_borrow_id")
        print("Selected date: ", value_date_taken())
        if borrow_id != 0:
            borrow_data = {
                "idborrow": borrow_id,
                "borrowamount": float(borrow_amount.value),
                "datetaken": value_date_taken(),
                "idmethod": int(payment_type_form.value),
                "idclient": int(id_client_form.value),
                "idfound": 1,
                "isactive": is_active.value,
            }
        else:
            borrow_data = {
                "borrowamount": float(borrow_amount.value),
                "datetaken": value_date_taken(),
                "idmethod": int(payment_type_form.value),
                "idclient": int(id_client_form.value),
                "idfound": 1,
                "isactive": is_active.value,
            }
        bill_data = {
            "numpayments": [int(x) for x in num_payments.value.split(",") if x.strip()],
            "paymentsof": [float(x) for x in payments_of.value.split(",") if x.strip()],
            "generatetofill": generate_to_fill.value,
        }
        payload = {
            "borrow": borrow_data,
            "billconditions": bill_data,
        }
        try:
            response = save_entities(f"{base_url}borrows/save", token, payload)
            print("Admin Response", response.json()["detail"])
            if response.status_code in (200, 201):
                result_text.value = "Borrow saved!"
                borrow_amount.value = num_payments.value = payments_of.value = ""
                generate_to_fill.value = True
            else:
                result_text.value = f"Error: {response.status_code}"
        except Exception as e:
            result_text.value = f"Exception: {e}"
        page.client_storage.set("edit_admin_id", 0)
        page.update()

    def populate_borrow_fields(borrow_array):
        print("void")
        borrow_amount.value = borrow_array.get("borrowamount", "")
        payment_type_form.value = borrow_array.get("idmethod", "")
        id_client_form.value = borrow_array.get("idclient", "")
        is_active.value = borrow_array.get("isactive", "")
        page.client_storage.set("edit_borrow_id", borrow_array.get("idborrow", 0))
        page.update()

    borrows = get_all_api(f"{base_url}borrows/get-all", token)
    borrow_rows = []
    for borrow in borrows:
        borrow_rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(borrow.get("borrowamount", ""))),
                ft.DataCell(ft.Text(borrow.get("totalpayment", ""))),
                ft.DataCell(ft.Text(borrow.get("datetaken", ""))),
                ft.DataCell(ft.Text(borrow.get("duedate", ""))),
                ft.DataCell(ft.Text(borrow.get("percentagetax", ""))),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(content=ft.Text("Update"), tooltip="Edit",  # icon=ft.icons.EDIT,
                                      on_click=lambda e, a=borrow: populate_borrow_fields(a)),
                    ])
                )
            ])
        )

    borrows_table = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Amount")),
            ft.DataColumn(label=ft.Text("Total Payment")),
            ft.DataColumn(label=ft.Text("Date Taken")),
            ft.DataColumn(label=ft.Text("Due Date")),
            ft.DataColumn(label=ft.Text("Percentage Tax")),
            ft.DataColumn(label=ft.Text("Actions"))
        ],
        rows=borrow_rows
    )

    return ft.Row([
        nav_rail,
        ft.VerticalDivider(width=1),
        ft.Container(
            expand=True,
            padding=20,
            content=ft.Column([
                ft.Text("Manage Borrows", size=20, weight=ft.FontWeight.BOLD),
                borrow_amount,
                date_taken,
                payment_type_form,
                id_client_form,
                is_active,
                num_payments,
                payments_of,
                generate_to_fill,
                ft.ElevatedButton("Submit", on_click=submit_borrow),
                result_text,
                ft.Divider(),
                borrows_table
            ], spacing=10, scroll="auto")
        )
    ], expand=True)
