import flet as ft
from ..models.load_json import read_json


def inventory_view(page):

    async def page_batl(e):
        await page.push_route("/battle")

    current_email = page.session.store.get("email")

    inventory_user = None

    inventory = read_json('storage/users.json')

    cart = []

    for user in inventory:
        if user["email"] == current_email:
            inventory_user = user
            break

    for invent in range(len(inventory_user["stats"]["inventory"])):
        cart_invent = ft.Column(controls=[ft.Text(f'{inventory_user["stats"]["inventory"][invent]}')])

        cart.append(cart_invent)


    return ft.View(
        route="/inventory",
        controls=[
            ft.Text("ИНВЕНТАРЬ", size=30),
            ft.Column(cart),
            ft.Button("Назад", on_click=page_batl),
        ],
    )
