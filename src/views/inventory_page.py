import flet as ft

from src.models.load_json import read_json


def inventory_view(page: ft.Page):

    async def page_batl(e):
        await page.push_route("/battle")

    current_email = page.session.store.get("email")

    users = read_json("storage/users.json") or []

    inventory_user = next(
        (user for user in users if user["email"] == current_email),
        None,
    )

    if inventory_user is None:
        return ft.View(
            route="/inventory",
            controls=[
                ft.Text(
                    "Користувача не знайдено",
                    size=24,
                    color=ft.Colors.RED,
                )
            ],
        )

    inventory = inventory_user["stats"].get("inventory", [])

    cards = []

    if not inventory:
        cards.append(
            ft.Container(
                padding=30,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    "🎒 Інвентар порожній",
                    size=20,
                    color=ft.Colors.GREY_700,
                ),
            )
        )

    for item in inventory:

        bonuses = []

        if item.get("attack", 0):
            bonuses.append(f"⚔️ +{item['attack']}")

        if item.get("defense", 0):
            bonuses.append(f"🛡️ +{item['defense']}")

        if item.get("hp", 0):
            bonuses.append(f"❤️ +{item['hp']}")

        cards.append(
            ft.Container(
                width=260,
                bgcolor="#F8F5EF",
                border=ft.border.all(2, "#D4AF37"),
                border_radius=15,
                padding=15,
                content=ft.Column(
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            item.get("name", "Невідомий предмет"),
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#B8860B",
                        ),

                        ft.Divider(height=1, color="#D4AF37"),

                        ft.Text(
                            (
                                " | ".join(bonuses)
                                if bonuses
                                else "Без бонусів"
                            ),
                            size=15,
                            color=ft.Colors.GREEN_700,
                        ),

                        ft.Text(
                            f"💰 Ціна: {item.get('price', 0)}",
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                ),
            )
        )

    return ft.View(
        route="/inventory",
        bgcolor="#EDE3C8",
        controls=[
            ft.Container(
                padding=20,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Назад до бою",
                            on_click=page_batl,
                        ),
                    ],
                ),
            ),

            ft.Container(
                alignment=ft.Alignment.CENTER,
                padding=10,
                content=ft.Text(
                    "ІНВЕНТАР",
                    size=34,
                    weight=ft.FontWeight.BOLD,
                    color="#B8860B",
                    text_align=ft.TextAlign.CENTER,
                ),
            ),

            ft.Container(
                expand=True,
                padding=20,
                content=ft.Row(
                    wrap=True,
                    spacing=15,
                    run_spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=cards,
                ),
            ),

            ft.Container(
                padding=20,
                alignment=ft.Alignment.CENTER,
                content=ft.ElevatedButton(
                    "⚔ Повернутися до бою",
                    icon=ft.Icons.SPORTS_MARTIAL_ARTS,
                    on_click=page_batl,
                    style=ft.ButtonStyle(
                        bgcolor="#D4AF37",
                        color="white",
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=15),
                        elevation=5,
                    ),
                ),
            ),
        ],
    )