import flet as ft

from ..views.style_button import main_btn


def page_main(page: ft.Page):
    """Головний екран"""
    async def open_register(e):
        """Перехід ло реєстрації"""
        await page.push_route("/register")

    return ft.View(
        route="/",
        controls=[
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src="main_photo.jpg",
                    fit=ft.BoxFit.COVER
                ),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(height=300),
                        ft.Button(
                            "Почати гру",
                            on_click=open_register,
                            style=main_btn
                        ),
                    ],
                ),
            )
        ]
    )




