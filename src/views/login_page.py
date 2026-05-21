import flet as ft

from ..models.auth_service import login_user
from ..models.disaun_login import login_ui


def login_page(page: ft.Page):
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
    )
    error_text = ft.Text("", color="red")

    async def open_register(e):
        await page.push_route("/register")

    async def handle_login(e):
        is_success = login_user(
            email_field.value.strip(),
            password_field.value.strip(),
        )

        if not is_success:
            error_text.value = "Неправильний логін або пароль"
            page.update()
            return

        await page.push_route("/variant_person")

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_GREY_700,
        on_click=open_register,
    )

    login_button = ft.Button(
        content=ft.Text("Увійти"),
        on_click=handle_login,
        width=300,
        style=ft.ButtonStyle(
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    return ft.View(
        route="/login",
        controls=[
            login_ui(
                email_field,
                password_field,
                error_text,
                back_button,
                login_button,
            )
        ],
    )
