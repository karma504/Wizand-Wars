import flet as ft

from src.models.load_json import read_json, write_json


def shop_view(page: ft.Page):
    products = read_json("storage/shop_item.json") or {}
    users = read_json("storage/users.json") or []

    current_email = page.session.store.get("email")
    current_user = None

    for user in users:
        if user["email"] == current_email:
            current_user = user
            break

    gold_text = ft.Text(
        f"💰 Золото: {current_user['stats']['gold']}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#B8860B",
    )

    stats_text = ft.Text(
        f"⚔️ {current_user['stats']['damage']}    "
        f"🛡️ {current_user['stats']['defense']}    "
        f"❤️ {current_user['stats']['hp']}",
        size=16,
    )

    msg_text = ft.Text(size=16)

    items_container = ft.Row(
        wrap=True,
        spacing=15,
        run_spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    async def page_battle(e):
        await page.push_route("/battle")

    def get_owned_item_names():
        inventory = current_user["stats"].get("inventory", [])
        return {item["name"] for item in inventory}

    def stat_bonus_text(item):
        parts = []

        if item.get("attack", 0):
            parts.append(f"⚔️ +{item['attack']}")

        if item.get("defense", 0):
            parts.append(f"🛡️ +{item['defense']}")

        if item.get("hp", 0):
            parts.append(f"❤️ +{item['hp']}")

        return "  ".join(parts)

    def refresh():
        gold_text.value = f"💰 Золото: {current_user['stats']['gold']}"

        stats_text.value = (
            f"⚔️ {current_user['stats']['damage']}    "
            f"🛡️ {current_user['stats']['defense']}    "
            f"❤️ {current_user['stats']['hp']}"
        )

        rebuild_items()
        page.update()

    def buy_item(e):
        item = e.control.data

        if current_user["stats"]["gold"] >= item["price"]:
            current_user["stats"]["gold"] -= item["price"]

            current_user["stats"]["damage"] += item.get("attack", 0)
            current_user["stats"]["defense"] += item.get("defense", 0)
            current_user["stats"]["hp"] += item.get("hp", 0)

            inventory = current_user["stats"].setdefault("inventory", [])
            inventory.append(item)

            write_json("storage/users.json", users)

            msg_text.value = f"✅ Куплено: {item['name']}"
            msg_text.color = ft.Colors.GREEN

        else:
            msg_text.value = "❌ Недостатньо золота"
            msg_text.color = ft.Colors.RED

        refresh()

    def rebuild_items():
        owned = get_owned_item_names()

        cards = []

        for item in products.values():
            if item["name"] in owned:
                continue

            cards.append(
                ft.Container(
                    width=220,
                    height=180,
                    bgcolor="#F8F5EF",
                    border=ft.border.all(2, "#D4AF37"),
                    border_radius=15,
                    padding=10,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                item["name"],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#B8860B",
                                text_align=ft.TextAlign.CENTER,
                            ),

                            ft.Text(
                                f"💰 {item['price']}",
                                size=16,
                                color="#C89B3C",
                            ),

                            ft.Text(
                                stat_bonus_text(item),
                                size=14,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.Colors.GREEN_700,
                            ),

                            ft.ElevatedButton(
                                "Купити",
                                data=item,
                                on_click=buy_item,
                                style=ft.ButtonStyle(
                                    bgcolor="#D4AF37",
                                    color="white",
                                ),
                            ),
                        ],
                    ),
                )
            )

        items_container.controls = cards

    rebuild_items()

    return ft.View(
        route="/shop",
        bgcolor="#EDE3C8",
        controls=[
            ft.Container(
                expand=True,
                padding=20,
                content=ft.Column(
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "МАГАЗИН",
                            size=34,
                            weight=ft.FontWeight.BOLD,
                            color="#B8860B",
                        ),

                        gold_text,

                        stats_text,

                        msg_text,

                        ft.Divider(color="#D4AF37"),

                        items_container,
                        ft.Container(
                            padding=20,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Button(
                                "⚔ Назад в бой",
                                on_click=page_battle,
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
                ),
            )
        ],
    )