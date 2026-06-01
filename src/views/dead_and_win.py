import flet as ft


def dead_and_win_views(page: ft.Page, result: str):

    async def go_back(e):
        await page.push_route("/battle")

    if result == "Перемога":
        title = ft.Text(
            "Перемога!",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_600
        )
        message = ft.Text(
            "Ти здобув перемогу в бою!\nНагороди вже зараховано.",
            size=18,
            text_align=ft.TextAlign.CENTER
        )
        btn = ft.Button(
            "Продовжити",
            on_click=go_back,
            bgcolor=ft.Colors.GREEN_400
        )

    elif result == "Поразка":
        title = ft.Text(
            "Поразка!",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED_600
        )
        message = ft.Text(
            "Ти програв цей бій...\nСпробуй ще раз!",
            size=18,
            text_align=ft.TextAlign.CENTER
        )
        btn = ft.Button(
            "Спробувати знову",
            on_click=go_back,
            bgcolor=ft.Colors.RED_400
        )

    else:
        title = ft.Text(
            "Нічия!",
            size=36,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.ORANGE_600
        )
        message = ft.Text(
            "Обидва бійці впали одночасно.\nЦе нічия!",
            size=18,
            text_align=ft.TextAlign.CENTER
        )
        btn = ft.Button(
            "У бій знову",
            on_click=go_back,
            bgcolor=ft.Colors.ORANGE_400
        )

    return ft.View(
        route="/result",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=30,
                controls=[title, message, btn],
            )
        ],
    )