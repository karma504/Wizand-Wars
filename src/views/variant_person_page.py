import flet as ft
from src.models.load_json import read_json,write_json



def build_card(page: ft.Page, character):
    async def select_character(e):
        users = read_json("storage/users.json") or []
        current_email = page.session.store.get('email')

        found = False

        for user in users:
            if user.get("email") == current_email:
                user["stats"]["class"] = character["class"]
                user["stats"]["photo"] = character["photo"]
                user["stats"]["photo_atk"] = character["photo_atk"]
                user["stats"]["hp"] = character["hp"]
                user["stats"]["damage"] = character["damage"]
                user["stats"]["defense"] = character["defense"]
                user["stats"]["level"] = character["level"]
                user["stats"]["gold"] = character["gold"]
                found = True
                break

        if found:
            write_json("storage/users.json", users)


        else:
            print("User not found")


        page.snack_bar = ft.SnackBar(ft.Text("Character selected!"))
        page.snack_bar.open = True

        await page.push_route("/battle")


    return ft.Button(
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=5,

            controls=[
                ft.Text(
                    character["class"].upper(),
                    size=20
                ),

                ft.Image(
                    src=character["photo"],
                    height=300,
                    fit=ft.BoxFit.COVER
                ),

                ft.Text(f"❤️ HP: {character['hp']}"),
                ft.Text(f"⚔️ ATK: {character['damage']}"),
                ft.Text(f"🛡 DEF: {character['defense']}")
            ]
        ),

        on_click=select_character
    )



def build_card_views(page: ft.Page):

    cards = []

    characters_data = read_json("storage/person.json")

    for character in characters_data:
        cards.append(build_card(page,character))

    return ft.View(
        route="/variant_person",
        controls=[
            ft.Text("ВЫБОР ПЕРСОНАЖА", size=30),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True,
                controls=cards
            )
        ]
    )

