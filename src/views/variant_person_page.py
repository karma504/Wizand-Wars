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
        style=ft.ButtonStyle(
        bgcolor="white",
        color="black",
        side=ft.BorderSide(2, "#D4AF37"),
        shape=ft.RoundedRectangleBorder(radius=20),
        elevation=5,
        padding=20,
    ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=10,

            controls=[
                ft.Text(
                    character["class"].upper(),
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#B8860B"
                ),

                ft.Divider(color="#E8D8A8"),

                ft.Image(
                    src=character["photo"],
                    height=600,
                    fit=ft.BoxFit.COVER
                ),

                ft.Divider(color="#E8D8A8"),

                ft.Container(
                    bgcolor="#F8F5EF",
                    border_radius=12,
                    padding=10,
                    content=ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text(
                                f"❤️ HP: {character['hp']}",
                                size=16
                            ),
                            ft.Text(
                                f"⚔️ ATK: {character['damage']}",
                                size=16
                            ),
                            ft.Text(
                                f"🛡 DEF: {character['defense']}",
                                size=16
                            ),
                        ]
                    )
                )
            ]
        ),

        on_click=select_character
    )



def build_card_views(page: ft.Page):

    cards = []

    characters_data = read_json("storage/person.json")

    for character in characters_data:
        cards.append(
            ft.Container(
                content=build_card(page, character),
                expand=1,
                padding=10,
            )
        )

    return ft.View(
        route="/variant_person",
        controls=[
            ft.Container(
                alignment=ft.Alignment.CENTER,
                padding=20,
                content=ft.Text(
                    "ВИБІР ПЕРСОНАЖА",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#B8860B",
                    text_align=ft.TextAlign.CENTER,
                ),
            ),

            ft.Row(
                controls=cards,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]
    )

