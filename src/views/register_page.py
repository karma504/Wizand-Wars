import flet as ft

from ..models.validator import validate_register
from ..models.auth_service import register_user
from ..models.disaun_register import register_ui


def register_view(page: ft.Page):

    async def open_login_page(e):
        await page.push_route("/login")

    async def open_home_page(e):
        await page.push_route("/")

    username_field = ft.TextField(label="Ім'я")

    email_field = ft.TextField(label="Email")

    password_field = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True
    )

    repeat_password_field = ft.TextField(
        label="Повторіть пароль",
        password=True,
        can_reveal_password=True
    )

    terms_checkbox = ft.Checkbox(
        label="Я погоджуюсь з умовами гри"
    )

    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.BLUE_GREY_700,
        on_click=open_home_page
    )

    error_text = ft.Text(
        "",
        color="red"
    )

    login_button = ft.TextButton(
        "Увійти",
        on_click=open_login_page
    )

    login_hint_text = ft.Text(
        "Вже маєш акаунт?",
        size=12,
        color=ft.Colors.GREY_600
    )

    title_text = ft.Text("РЕЄСТРАЦІЯ")

    async def handle_register(e):
        validation_result = validate_register(
            username_field.value.strip(),
            email_field.value.strip(),
            password_field.value.strip(),
            repeat_password_field.value.strip(),
            terms_checkbox.value
        )

        if validation_result != "ok":
            error_text.value = validation_result
            page.update()
            return

        register_user(
            username_field.value.strip(),
            email_field.value.strip(),
            password_field.value.strip()
        )

        error_text.value = "Успіх!"
        page.update()

        await page.push_route("/variant_person")

    register_button = ft.Button(
        content=ft.Text("Зареєструватись"),
        on_click=handle_register,
        style=ft.ButtonStyle(
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=12),
        )
    )

    return ft.View(
        route="/register",
        controls=[
            register_ui(
                username_field,
                email_field,
                password_field,
                repeat_password_field,
                terms_checkbox,
                error_text,
                register_button,
                login_button,
                back_button,
                title_text,
                login_hint_text
            ),
        ]
    )

