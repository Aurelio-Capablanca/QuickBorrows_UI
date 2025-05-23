import json

import requests
import flet as ft


def get_all_api(url: str, token):
    try:
        result = requests.get(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                              json={"page": 0, "limit": 10})
        print(result)
        print(result.json()["detail"]["data"])
        return result.json()["detail"]["data"]
    except Exception as ex:
        print(ex)
        return None


def delete_entity(url, token, admin_id, result_text: ft.Text, page: ft.Page, entity_name: str):
    try:
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            json={"identity": admin_id}
        )
        if response.status_code == 200:
            result_text.value = f"{entity_name} deleted."
            page.go(page.route)
        else:
            result_text.value = f"Delete failed: {response.status_code}"
    except Exception as e:
        result_text.value = f" Exception: {e}"
    page.update()


def save_entities(url, token, payload):
    return requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps(payload)
    )


def generate_dropdown(options: list[dict], label: str, identifier, content, width: int = 300) -> ft.Dropdown:
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(str(opt.get(identifier, "")), opt.get(content, " ")) for opt in options],
        width=width
    )
