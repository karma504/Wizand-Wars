import flet as ft

from ..models.load_json import read_json

characters_data = read_json("src/storage/person.json")
# user = user


def build_stat_row(icon, color, text):
    return ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Icon(
                icon,
                color=color,
                size=22
            ),

            ft.Text(
                text,
                size=18,
                color="white",
                weight=ft.FontWeight.W_500
            )
        ]
    )



def build_card_views(page: ft.Page):
    """Create character button card"""
    async def open_battle():
        await page.push_route("/battle")

    for char in characters_data:
        for ch in char:
            img = ft.Container(ft.Image(
                src=ch['photo'])
                , expand=True)

            return ft.View(
                route = '/variant_person',
                controls=[
                ft.Container(
                expand=True,
                content=ft.Button(

                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Text(ch['class'].upper(), size=20),
                            # ft.Text(user['user'].upper(), size=20),

                            img,

                            ft.Text(f"❤️ HP: {ch['hp']}"),
                            ft.Text(f"⚔️ ATK: {ch['damage']}"),
                            ft.Text(f"🛡 DEF: {ch['defense']}"),
                        ]
                    )
                )
            )
            ]
            )