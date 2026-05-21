import flet as ft
from src.views.main_page import main_page
from src.views.login_page import login_page
from src.views.register_page import register_view
from src.views.variant_person_page import build_card_views


def main(page: ft.Page):
    # pag

    def route_change():
        page.views.clear()
        page.views.append(main_page(page))
        if page.route == "/register":
            page.views.append(register_view(page))

        if page.route == "/login":
            page.views.append(login_page(page))
        # #
        # if page.route == "/variant_person":
        #     page.views.append(build_card_views(page))
        #
        # if page.route == ("/pass"):
        #     page.views.append(view_pass_menu(page))

        page.update()

    async def view_pop(e):

        if len(page.views) > 1:
            page.views.pop()

            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change

    page.on_view_pop = view_pop

    route_change()


if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER)
