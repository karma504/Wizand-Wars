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

    gold_text = ft.Text(f"💰 Золото: {current_user['stats']['gold']}")
    stats_text = ft.Text(
        f"⚔️ ATK: {current_user['stats']['damage']}   "
        f"🛡️ DEF: {current_user['stats']['defense']}   "
        f"❤️ HP: {current_user['stats']['hp']}",
        size=14,
        color=ft.Colors.BLUE_200,
    )

    msg_text = ft.Text(size=16)
    items_column = ft.Column(spacing=15)

    def get_owned_item_names():
        inventory = current_user["stats"].get("inventory", [])
        return {item["name"] for item in inventory}

    def refresh():
        gold_text.value = f"💰 Золото: {current_user['stats']['gold']}"
        stats_text.value = (
            f"⚔️ ATK: {current_user['stats']['damage']}   "
            f"🛡️ DEF: {current_user['stats']['defense']}   "
            f"❤️ HP: {current_user['stats']['hp']}"
        )
        rebuild_items()
        items_column.update()  # ← принудительное обновление колонки
        page.update()

    def stat_bonus_text(item):
        parts = []
        if item.get("attack", 0) != 0:
            sign = "+" if item["attack"] > 0 else ""
            parts.append(f"⚔️ {sign}{item['attack']} ATK")
        if item.get("defense", 0) != 0:
            sign = "+" if item["defense"] > 0 else ""
            parts.append(f"🛡️ {sign}{item['defense']} DEF")
        if item.get("hp", 0) != 0:
            sign = "+" if item["hp"] > 0 else ""
            parts.append(f"❤️ {sign}{item['hp']} HP")
        return "  ".join(parts) if parts else "Нет бонусов"

    def rebuild_items():
        owned = get_owned_item_names()
        controls = []

        for key, item in products.items():
            if item["name"] in owned:
                continue  # ← пропускаем уже купленные

            controls.append(
                ft.Container(
                    padding=15,
                    border_radius=15,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(item["name"], size=20),
                                    ft.Text(
                                        f"Ціна: {item['price']} 💰",
                                        color="yellow",
                                    ),
                                    ft.Text(
                                        stat_bonus_text(item),
                                        size=13,
                                        color=ft.Colors.GREEN_300,
                                    ),
                                ]
                            ),
                            ft.ElevatedButton(
                                "Купити",
                                data=item,
                                on_click=buy_item,
                            ),
                        ],
                    ),
                )
            )

        items_column.controls = controls

    def buy_item(e):
        item = e.control.data
        price = item["price"]

        if current_user["stats"]["gold"] >= price:
            current_user["stats"]["gold"] -= price

            # Применяем бонусы к характеристикам
            current_user["stats"]["damage"] = (
                current_user["stats"].get("damage", 0) + item.get("attack", 0)
            )
            current_user["stats"]["defense"] = (
                current_user["stats"].get("defense", 0) + item.get("defense", 0)
            )
            current_user["stats"]["hp"] = (
                current_user["stats"].get("hp", 0) + item.get("hp", 0)
            )

            inventory = current_user["stats"].setdefault("inventory", [])
            inventory.append(item)

            write_json("storage/users.json", users)

            bonuses = stat_bonus_text(item)
            msg_text.value = f"✅ Куплено: {item['name']}\n{bonuses}"
            msg_text.color = ft.Colors.GREEN
        else:
            msg_text.value = "❌ Недостатньо монет"
            msg_text.color = ft.Colors.RED

        refresh()

    rebuild_items()

    return ft.View(
        route="/shop",
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=20,
                    controls=[
                        gold_text,
                        stats_text,
                        msg_text,
                        items_column,
                    ],
                ),
            )
        ],
    )