import flet as ft

def login_ui(
        email_field,
        password_field,
        error_text,
        back_button,
        login_button
):

    title_text = ft.Text(
        "ВХІД",
        size=24,
        weight=ft.FontWeight.BOLD
    )

    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            back_button,
            title_text,
        ],
    )

    divider = ft.Divider(height=1)

    spacer = ft.Container(height=5)

    content_column = ft.Column(
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            header_row,
            divider,
            email_field,
            password_field,
            error_text,
            spacer,
            login_button,
        ],
    )

    return ft.Container(
        width=420,
        padding=25,
        border_radius=20,
        bgcolor=ft.Colors.BLUE_50,
        shadow=ft.BoxShadow(
            blur_radius=15,
            spread_radius=1,
            color=ft.Colors.BLACK12,
        ),
        content=content_column,
    )