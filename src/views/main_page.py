import flet as ft


def main_page(page: ft.Page):
    async def open_register(e):
        await page.push_route("/register")

    btn = ft.Button(
        "Почати гру",
        width=220,
        height=60,
        on_click=open_register,
    )

    background = ft.Container(
        content=ft.Image(
            src="../assets/ph.jpg",
            expand=True,
        ),
        expand=True,
    )

    return ft.View(
        route="/",
        padding=0,
        spacing=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    background,
                    ft.Container(
                        content=btn,
                        alignment=ft.Alignment.CENTER,
                        expand=True,
                    ),
                ],
            )
        ],
    )
