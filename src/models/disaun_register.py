import flet as ft


def register_ui(input_user,
                input_email,
                input_passwd,
                input_repeat_password,
                checkbox_game,
                error_text,
                btn_register,
                btn_log,
                back_btn,
                text_register,
                maeg_akk):

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

        content=ft.Column(

            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        back_btn,
                        text_register,
                    ],
                ),

                ft.Divider(height=1),

                input_user,
                input_email,
                input_passwd,
                input_repeat_password,
                checkbox_game,

                error_text,

                ft.Container(height=5),

                btn_register,

                maeg_akk,

                btn_log,
            ],
        ),
    )


#
#
#
# btn_style = ft.ButtonStyle(
#     color=ft.Colors.BLUE_100,
#     shape=ft.RoundedRectangleBorder(radius=12),
#     padding=12,
# )