import flet as ft
import random

from ..models.load_json import read_json, write_json
from ..models.services import generate_enemy
from ..models.logic_battle import (
    get_player_actions,
    get_max_damage,
    get_max_defense,
    apply_def,
    crit,
)

GOLD_PENALTY_PERCENT = 0.10


def battle_page(page: ft.Page):

    async def views_shop(e):
        await page.push_route("/shop")

    async def views_inventory(e):
        await page.push_route("/inventory")

    current_email = page.session.store.get("email")
    users = read_json("storage/users.json")
    player = None

    for user in users:
        if user["email"] == current_email:
            player = user
            break

    if player is None:
        return ft.View(
            route="/battle",
            controls=[ft.Text("Гравця не знайдено", size=24, color=ft.Colors.RED)]
        )

    battle = read_json("storage/battle_enemy.json")

    if not battle.get("enemy"):
        enemy_block = generate_enemy(player["stats"]["level"])
        enemy_name = list(enemy_block.keys())[0]
        enemy_data = enemy_block[enemy_name]

        battle["enemy"] = enemy_name
        battle["hp"] = enemy_data["hp"]
        battle["hp_max"] = enemy_data["hp"]
        battle["damage"] = enemy_data["damage"]
        battle["defense"] = enemy_data.get("defense", 0)
        battle["gold"] = enemy_data["gold"]
        battle["exp"] = enemy_data["exp"]
        battle["type"] = enemy_data["type_en"]
        battle["photo_atk"] = enemy_data["photo_atk"]
        battle["attacks"] = enemy_data["attacks"]
        battle["defenses"] = enemy_data["defenses"]
        write_json("storage/battle_enemy.json", battle)

    multipliers = {"COMMON": 1, "RARE": 1.5, "ELITE": 2.5, "BOSS": 3}
    enemy_multiplier = multipliers.get(battle.get("type", "COMMON"), 1)

    def recalc_limits():
        pmx_dmg = get_max_damage(player["stats"]["damage"], player["stats"].get("attacks", []))
        pmx_def = get_max_defense(player["stats"]["defense"], player["stats"].get("defenses", []))
        emx_dmg = get_max_damage(battle["damage"] * enemy_multiplier, battle.get("attacks", []))
        emx_def = get_max_defense(battle["defense"] * enemy_multiplier, battle.get("defenses", []))
        return pmx_dmg, pmx_def, emx_dmg, emx_def

    p_name_text  = ft.Text(player["user"], size=24, weight=ft.FontWeight.BOLD)
    p_class_text = ft.Text(f"CLASS: {player['stats']['class']}")
    p_hp_text    = ft.Text("", size=16)
    p_atk_text   = ft.Text("", size=14)
    p_def_text   = ft.Text("", size=14)
    p_lvl_text   = ft.Text("", size=14, color=ft.Colors.BLUE_400)
    p_exp_text   = ft.Text("", size=12, color=ft.Colors.GREY_500)

    e_name_text  = ft.Text("", size=24, weight=ft.FontWeight.BOLD)
    e_type_text  = ft.Text("", size=14)
    e_hp_text    = ft.Text("", size=16)
    e_atk_text   = ft.Text("", size=14)
    e_def_text   = ft.Text("", size=14)

    action_area = ft.Column(controls=[], spacing=10)
    selected_action = {"value": None}

    def save_and_refresh():
        player["stats"]["hp"] = max(0, player["stats"]["hp"])
        battle["hp"] = max(0, battle["hp"])

        write_json("storage/users.json", users)
        write_json("storage/battle_enemy.json", battle)

        pmx_dmg, pmx_def, emx_dmg, emx_def = recalc_limits()

        level = player["stats"].get("level", 1)
        exp = player["stats"].get("exp", 0)
        exp_needed = level * 100

        p_hp_text.value  = f"❤️ HP: {player['stats']['hp']}"
        p_atk_text.value = f"⚔️ ATK: {player['stats']['damage']}  (max {pmx_dmg})"
        p_def_text.value = f"🛡️ DEF: {player['stats']['defense']}  (max {pmx_def})"
        p_lvl_text.value = f"⭐ Уровень: {level}"
        p_exp_text.value = f"EXP: {exp} / {exp_needed}"

        e_name_text.value = battle.get("enemy", "???")
        e_type_text.value = f"TYPE: {battle.get('type', '')}  |  LVL: {level}"
        e_hp_text.value   = f"❤️ HP: {battle['hp']}"
        e_atk_text.value  = f"⚔️ ATK max: {emx_dmg}"
        e_def_text.value  = f"🛡️ DEF max: {emx_def}"

        page.update()

    def close_dlg(dlg):
        dlg.open = False
        page.update()

    def show_result_dialog(title, message):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(message, size=15),
            actions=[ft.TextButton("OK", on_click=lambda e: close_dlg(dlg))],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def apply_defeat_penalty():
        gold = player["stats"].get("gold", 0)
        penalty = int(gold * GOLD_PENALTY_PERCENT)
        player["stats"]["gold"] = max(0, gold - penalty)
        return penalty

    def reset_enemy():
        write_json("storage/battle_enemy.json", {})

    def check_outcome():
        if player["stats"]["hp"] <= 0 and battle["hp"] <= 0:
            return "Ничья"
        if battle["hp"] <= 0:
            return "Победа"
        if player["stats"]["hp"] <= 0:
            return "Поражение"
        return None

    def try_level_up():
        level = player["stats"].get("level", 1)
        exp = player["stats"].get("exp", 0)
        exp_needed = level * 100

        if exp < exp_needed:
            return None

        player["stats"]["level"] = level + 1
        player["stats"]["exp"] = exp - exp_needed
        player["stats"]["damage"] = player["stats"].get("damage", 0) + 3
        player["stats"]["defense"] = player["stats"].get("defense", 0) + 2
        player["stats"]["hp"] = player["stats"].get("hp", 0) + 10

        return (
            f"🎉 УРОВЕНЬ {level + 1}!\n"
            f"+3 ATK, +2 DEF, +10 HP\n"
            f"Следующий уровень: {(level + 1) * 100} опыта"
        )

    def show_outcome_dialog(outcome):
        if outcome == "Победа":
            earned_gold = battle.get("gold", 0)
            earned_exp  = battle.get("exp", 0)
            player["stats"]["gold"] = player["stats"].get("gold", 0) + earned_gold
            player["stats"]["exp"]  = player["stats"].get("exp", 0) + earned_exp
            levelup_msg = try_level_up()

            title_text   = "🏆 Победа!"
            color        = ft.Colors.GREEN
            content_text = (
                f"Ты победил {battle.get('enemy')}!\n"
                f"Получено: {earned_gold} 💰, {earned_exp} EXP."
            )
            if levelup_msg:
                content_text += f"\n\n{levelup_msg}"

            save_and_refresh()
            reset_enemy()

        elif outcome == "Поражение":
            penalty      = apply_defeat_penalty()
            title_text   = "💀 Поражение!"
            color        = ft.Colors.RED
            content_text = (
                f"Ты проиграл бой...\n"
                f"HP сохранено: {player['stats']['hp']}\n"
                f"Штраф: -{penalty} 💰"
            )
            save_and_refresh()
            reset_enemy()

        else:
            title_text   = "🤝 Ничья!"
            color        = ft.Colors.ORANGE
            content_text = "Оба пали одновременно. Ничья!"
            save_and_refresh()
            reset_enemy()

        async def go_home(e):
            dlg.open = False
            page.update()
            await page.push_route("/battle")

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(title_text, color=color, size=22, weight=ft.FontWeight.BOLD),
            content=ft.Text(content_text, size=16),
            actions=[ft.TextButton("OK", on_click=go_home)],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def on_exit_click(e):
        async def confirm_exit(e):
            dlg.open = False
            page.update()
            apply_defeat_penalty()
            save_and_refresh()
            reset_enemy()
            await page.push_route("/")

        def cancel_exit(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("🚪 Выход из боя", size=20, weight=ft.FontWeight.BOLD),
            content=ft.Text(
                "Вы уверены, что хотите выйти из боя?\n"
                "Это засчитается как поражение и вы потеряете часть золота.",
                size=15
            ),
            actions=[
                ft.TextButton("Да", on_click=confirm_exit),
                ft.TextButton("Нет", on_click=cancel_exit),
            ],
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def make_checkbox_group(options):
        checkboxes = []
        for opt in options:
            cb = ft.Checkbox(label=opt["name"], value=False, data=opt)
            checkboxes.append(cb)

        def on_change(e):
            for cb in checkboxes:
                if cb is not e.control:
                    cb.value = False
            e.control.value = True
            selected_action["value"] = e.control.data
            page.update()

        for cb in checkboxes:
            cb.on_change = on_change

        return checkboxes

    def on_attack_click(e):
        options = get_player_actions(player["stats"], "atk").get("attacks", [])
        selected_action["value"] = None
        checkboxes = make_checkbox_group(options)

        def on_confirm(e):
            chosen = selected_action["value"]
            if chosen is None:
                show_result_dialog("⚠️ Выбор не сделан", "Сначала выбери атаку!")
                return

            pmx_dmg, _, emx_dmg, emx_def = recalc_limits()

            raw_dmg    = player["stats"]["damage"] * chosen.get("damage_mult", 1)
            player_dmg = crit(raw_dmg, 0.25, max_dmg=pmx_dmg)

            raw_edef   = battle.get("defense", 0) * enemy_multiplier
            enemy_def  = min(int(raw_edef), emx_def)

            damage_to_enemy = apply_def(player_dmg, enemy_def)

            battle["hp"] = max(0, battle["hp"] - damage_to_enemy)

            action_area.controls.clear()
            save_and_refresh()

            outcome = check_outcome()
            if outcome:
                show_outcome_dialog(outcome)
            else:
                show_result_dialog(
                    f"⚔️ {chosen['name']}",
                    f"Ты нанёс {battle.get('enemy')} урон: {damage_to_enemy}\n"
                    f"(Твой урон: {player_dmg}, защита врага: {enemy_def})"
                )

        action_area.controls = [
            ft.Text("Выбери атаку:", size=16, weight=ft.FontWeight.BOLD),
            *checkboxes,
            ft.Button("Подтвердить", on_click=on_confirm, bgcolor=ft.Colors.RED_400),
        ]
        page.update()

    def on_defense_click(e):
        options = get_player_actions(player["stats"], "def").get("defenses", [])
        selected_action["value"] = None
        checkboxes = make_checkbox_group(options)

        def on_confirm(e):
            chosen = selected_action["value"]
            if chosen is None:
                show_result_dialog("⚠️ Выбор не сделан", "Сначала выбери защиту!")
                return

            pmx_dmg, pmx_def, emx_dmg, emx_def = recalc_limits()

            raw_pdef   = player["stats"]["defense"] * chosen.get("defense_mult", 1) * 1.5
            player_def = min(int(raw_pdef), int(pmx_def * 1.5))

            enemy_attacks = battle.get("attacks", [])
            enemy_attack  = (
                random.choice(enemy_attacks) if enemy_attacks
                else {"name": "Удар", "damage_mult": 1}
            )
            raw_edmg  = battle["damage"] * enemy_multiplier * enemy_attack.get("damage_mult", 1)
            enemy_dmg = crit(raw_edmg, 0.15, max_dmg=emx_dmg)

            damage_to_player = apply_def(enemy_dmg, player_def)

            player["stats"]["hp"] = max(0, player["stats"]["hp"] - damage_to_player)

            action_area.controls.clear()
            save_and_refresh()

            outcome = check_outcome()
            if outcome:
                show_outcome_dialog(outcome)
            else:
                show_result_dialog(
                    f"🛡️ Противник применил: {enemy_attack['name']}",
                    f"Тебе нанесено урона: {damage_to_player}\n"
                    f"(Атака врага: {enemy_dmg}, твоя защита: {player_def})"
                )

        action_area.controls = [
            ft.Text("Выбери защиту:", size=16, weight=ft.FontWeight.BOLD),
            *checkboxes,
            ft.Button("Подтвердить", on_click=on_confirm, bgcolor=ft.Colors.BLUE_400),
        ]
        page.update()

    player_panel = ft.Container(
        width=260, padding=15, border_radius=15, bgcolor=ft.Colors.BLUE_50,
        content=ft.Column(controls=[p_name_text, p_class_text, p_hp_text, p_atk_text, p_def_text, p_lvl_text, p_exp_text])
    )

    enemy_panel = ft.Container(
        width=260, padding=15, border_radius=15, bgcolor=ft.Colors.RED_50,
        content=ft.Column(controls=[e_name_text, e_type_text, e_hp_text, e_atk_text, e_def_text])
    )

    attack_btn  = ft.Button("⚔️ Атака",  on_click=on_attack_click,  bgcolor=ft.Colors.RED_300)
    defense_btn = ft.Button("🛡️ Защита", on_click=on_defense_click, bgcolor=ft.Colors.BLUE_300)
    exit_btn    = ft.Button("🚪 Выйти",  on_click=on_exit_click,    bgcolor=ft.Colors.GREY_400)
    shop_btn    = ft.IconButton(icon=ft.Icons.STORE, on_click=views_shop,      tooltip="Магазин")
    invent_btn  = ft.IconButton(icon=ft.Icons.BOY,   on_click=views_inventory, tooltip="Инвентарь")

    save_and_refresh()

    return ft.View(
        route="/battle",
        controls=[
            ft.Column(spacing=20, controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[player_panel, enemy_panel]),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=15, controls=[attack_btn, defense_btn, exit_btn, invent_btn, shop_btn]),
                action_area,
            ])
        ]
    )