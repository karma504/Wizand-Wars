import flet as ft
from views.register_page import page_register
from views.main_page import page_main
from views.variant_person_page import build_card_views
from views.battle_page import battle_page
from views.inventory_page import inventory_view
from views.shop_page import shop_view
from views.login_page import login_views

async def main(page: ft.Page):

    async def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(page_main(page))

        if page.route == "/register":
            page.views.append(page_register(page))

        if page.route == "/variant_person":
            page.views.append(build_card_views(page))

        if page.route == "/battle":
            page.views.append(battle_page(page))

        if page.route == "/shop":
            page.views.append(shop_view(page))

        if page.route == "/inventory":
            page.views.append(inventory_view(page))

        if page.route == "/login":
            page.views.append(login_views(page))

        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await route_change(None)


if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER)

