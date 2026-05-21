import flet as ft

def main(page:ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    btn_gol = ft.Button('Почати гру')

    page.add(btn_gol)


if __name__ == '__main__':
    ft.run(main)