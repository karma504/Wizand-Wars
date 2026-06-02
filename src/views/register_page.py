import flet as ft

from ..models.validator import validate_register
from ..models.auth_service import register_user


def page_register(page: ft.Page):
    async def open_login_page(e):
        await page.push_route("/login")

    async def open_home_page(e):
        await page.push_route("/")

    def open_terms(e):
        page.show_dialog(ft.AlertDialog(
            title=ft.Text(
                "Умови гри",
                size=26,
                weight=ft.FontWeight.BOLD,
                color="#B8860B",
            ),
            content=ft.Text(
                "1. Не використовуй баги\n"
                "2. Поважай інших гравців\n"
                "3. Адміністрація може змінювати правила"
            ),
        ))

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#B8860B",
        on_click = open_home_page

    )

    title = ft.Text(
        "РЕЄСТРАЦІЯ",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#B8860B",
    )


    field_style = dict(
        border_radius=12,
        bgcolor="white",
        border_color="#D4AF37",
        focused_border_color="#C9A227",
        width=350,
    )

    user_fd = ft.TextField(label="Ім'я користувача", **field_style)
    email_fd = ft.TextField(label="Email", **field_style)

    password_fd = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        **field_style,
    )

    repeat_password_fd = ft.TextField(
        label="Повторіть пароль",
        password=True,
        can_reveal_password=True,
        **field_style,
    )

    terms_checkbox = ft.Checkbox(
        label="Я погоджуюсь з умовами гри",
        active_color="#D4AF37",
    )

    terms_button = ft.TextButton(
        "Умови гри",
        style=ft.ButtonStyle(color="#B8860B"),
        on_click=open_terms,
    )

    async def handle_register(e):
        page.session.store.set("email",email_fd.value.strip())
        validation_result = validate_register(user_fd.value.strip(),
                                            email_fd.value.strip(),
                                            password_fd.value.strip(),
                                            repeat_password_fd.value.strip(),
                                            terms_checkbox.value)

        if validation_result != "ok":
            error_text.value = validation_result
            page.update()
            return

        register_user(
            user_fd.value.strip(),
            email_fd.value.strip(),
            password_fd.value.strip()
        )

        error_text.value = "Успіх!"
        page.update()
        await page.push_route("/variant_person")

    register_button = ft.Button(
        "Створити акаунт",
        width=350,
        height=55,
        on_click=handle_register,
        style=ft.ButtonStyle(
            bgcolor="#D4AF37",
            color="white",
            elevation=5,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
    )

    login_button = ft.TextButton(
        "Увійти",
        style=ft.ButtonStyle(color="#B8860B"),
        on_click = open_login_page
    )

    error_text = ft.Text("", color="red")

    return ft.View(
        route="/register",
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
                        spacing=15,
                        controls=[

                            ft.Row(
                                [back_button],
                                alignment=ft.MainAxisAlignment.START,
                            ),

                            title,

                            ft.Divider(color="#E8D8A8"),

                            user_fd,
                            email_fd,
                            password_fd,
                            repeat_password_fd,

                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    terms_checkbox,
                                    terms_button,
                                ],
                            ),

                            error_text,

                            register_button,

                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=0,
                                controls=[
                                    ft.Text("Вже є акаунт?", color="#6b5b3e"),
                                    login_button,
                                ],
                            ),
                        ],
                    ),
                ),
            )
        ],
    )