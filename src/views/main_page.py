import flet as ft


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
                            style=ft.ButtonStyle(
        color="white",
        bgcolor="#C89B3C",
        padding=ft.padding.symmetric(horizontal=50, vertical=22),
        text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
        shape=ft.RoundedRectangleBorder(radius=16),
        side=ft.BorderSide(2, "#7A5A1E"),
    )
                        ),
                    ],
                ),
            )
        ]
    )




