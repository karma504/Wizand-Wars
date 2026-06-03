import flet as ft

from src.models.auth_service import login_user


def login_views(page: ft.Page):

    email_field = ft.TextField(
        label="Введіть еmail",
        width=350,
        border_color="#D4AF37",
        focused_border_color="#C9A227",
        border_radius=12,
        bgcolor="white",
    )

    password_field = ft.TextField(
        label="Введіть пароль",
        password=True,
        can_reveal_password=True,
        width=350,
        border_color="#D4AF37",
        focused_border_color="#C9A227",
        border_radius=12,
        bgcolor="white",
    )

    error_text = ft.Text(
        "",
        color="red",
        size=14,
    )

    async def open_register(e):
        await page.push_route("/register")

    async def handle_login(e):
        page.session.store.set("email", email_field.value.strip())
        is_success = login_user(
            email_field.value.strip(),
            password_field.value.strip(),
        )

        if not is_success:
            error_text.value = "Неправильний логін або пароль"
            page.update()
            return

        await page.push_route("/battle")

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#B8860B",
        icon_size=28,
        on_click=open_register,
    )

    login_button = ft.Button(
        "Увійти",
        width=350,
        height=55,
        on_click=handle_login,
        style=ft.ButtonStyle(
            bgcolor="#D4AF37",
            color="white",
            elevation=5,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
    )

    return ft.View(
        route="/login",
        bgcolor="#F8F5EF",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Container(
                    width=500,
                    padding=40,
                    bgcolor="white",
                    border_radius=20,
                    border=ft.border.all(1, "#D4AF37"),
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=1,
                        color=ft.Colors.BLACK12,
                    ),
                    content=ft.Column(
                        tight=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                [back_button],
                                alignment=ft.MainAxisAlignment.START,
                            ),

                            ft.Text(
                                "Вхід",
                                size=32,
                                weight=ft.FontWeight.BOLD,
                                color="#B8860B",
                            ),

                            ft.Divider(color="#E8D8A8"),

                            email_field,

                            password_field,

                            error_text,

                            ft.Container(height=10),

                            login_button,
                        ],
                    ),
                ),
            )
        ],
    )