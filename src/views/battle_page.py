import flet as ft
import random

from src.models.load_json import read_json, write_json
from src.models.services import generate_enemy
from src.models.logic_battle import (
    get_player_actions,
    get_max_damage,
    get_max_defense,
    apply_def,
    crit,
)

GOLD_PENALTY_PERCENT = 0.10

USERS_FILE = "storage/users.json"
BATTLE_FILE = "storage/battle_enemy.json"


def battle_page(page: ft.Page):
    current_email = page.session.store.get("email")
    users = read_json(USERS_FILE)
    player = next((u for u in users if u.get("email") == current_email), None)

    if player is None:
        return ft.View(
            route="/battle",
            bgcolor = "#0B1220",
            padding=0,
            spacing=0,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment.CENTER,
                    bgcolor="#0B1220",
                    content=ft.Text(
                        "Гравця не знайдено",
                        size=24,
                        color=ft.Colors.RED_300,
                        weight=ft.FontWeight.BOLD,
                    ),
                )
            ],
        )

    battle = read_json(BATTLE_FILE) or {}

    if not battle.get("enemy"):
        enemy_block = generate_enemy(player["stats"].get("level", 1))
        enemy_name = list(enemy_block.keys())[0]
        enemy_data = enemy_block[enemy_name]

        battle = {
            "enemy": enemy_name,
            "hp": enemy_data["hp"],
            "hp_max": enemy_data["hp"],
            "damage": enemy_data["damage"],
            "defense": enemy_data.get("defense", 0),
            "gold": enemy_data["gold"],
            "exp": enemy_data["exp"],
            "type": enemy_data.get("type_en", "COMMON"),
            "photo_atk": enemy_data.get("photo_atk"),
            "attacks": enemy_data.get("attacks", []),
            "defenses": enemy_data.get("defenses", []),
        }
        write_json(BATTLE_FILE, battle)

    multipliers = {
        "COMMON": 1,
        "RARE": 1.5,
        "ELITE": 2.5,
        "BOSS": 3,
    }

    def enemy_multiplier() -> float:
        return multipliers.get(str(battle.get("type", "COMMON")).upper(), 1)

    def recalc_limits():
        p_stats = player["stats"]
        e_mult = enemy_multiplier()

        pmx_dmg = get_max_damage(
            p_stats.get("damage", 0),
            p_stats.get("attacks", []),
        )
        pmx_def = get_max_defense(
            p_stats.get("defense", 0),
            p_stats.get("defenses", []),
        )
        emx_dmg = get_max_damage(
            battle.get("damage", 0) * e_mult,
            battle.get("attacks", []),
        )
        emx_def = get_max_defense(
            battle.get("defense", 0) * e_mult,
            battle.get("defenses", []),
        )
        return pmx_dmg, pmx_def, emx_dmg, emx_def

    TEXT_PRIMARY = "#1E293B"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748B"
    CARD_BG = "#F8F5EF"
    CARD_BG_LIGHT = "#F8F5EF"
    CARD_BORDER = "#D4AF37"
    ACCENT = "#D4AF37"
    RED_BTN = "#B91C1C"
    BLUE_BTN = "#1D4ED8"
    GREY_BTN = "#475569"

    p_name_text = ft.Text(
        player["user"],
        size=24,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )
    p_class_text = ft.Text(size=14, color=TEXT_SECONDARY)
    p_hp_text = ft.Text(size=16, color=TEXT_PRIMARY)
    p_atk_text = ft.Text(size=14, color=TEXT_SECONDARY)
    p_def_text = ft.Text(size=14, color=TEXT_SECONDARY)
    p_lvl_text = ft.Text(size=14, color="#93C5FD")
    p_exp_text = ft.Text(size=12, color=TEXT_MUTED)

    e_name_text = ft.Text(
        size=24,
        weight=ft.FontWeight.BOLD,
        color=TEXT_PRIMARY,
    )
    e_type_text = ft.Text(size=14, color=TEXT_SECONDARY)
    e_hp_text = ft.Text(size=16, color=TEXT_PRIMARY)
    e_atk_text = ft.Text(size=14, color=TEXT_SECONDARY)
    e_def_text = ft.Text(size=14, color=TEXT_SECONDARY)

    action_area = ft.Column(controls=[], spacing=10)
    selected_action = {"value": None}

    def refresh_ui():
        player["stats"]["hp"] = max(0, int(player["stats"].get("hp", 0)))
        battle["hp"] = max(0, int(battle.get("hp", 0)))

        pmx_dmg, pmx_def, emx_dmg, emx_def = recalc_limits()

        level = int(player["stats"].get("level", 1))
        exp = int(player["stats"].get("exp", 0))
        exp_needed = level * 100

        p_class_text.value = f"Клас: {player['stats'].get('class', 'Невідомо')}"
        p_hp_text.value = f"❤️ HP: {player['stats']['hp']}"
        p_atk_text.value = (
            f"⚔️ Атака: {player['stats'].get('damage', 0)} "
            f"(макс. {pmx_dmg})"
        )
        p_def_text.value = (
            f"🛡️ Захист: {player['stats'].get('defense', 0)} "
            f"(макс. {pmx_def})"
        )
        p_lvl_text.value = f"⭐ Рівень: {level}"
        p_exp_text.value = f"EXP: {exp} / {exp_needed}"

        e_name_text.value = battle.get("enemy", "Невідомий ворог")
        e_type_text.value = f"Тип: {battle.get('type', 'COMMON')}"
        e_hp_text.value = f"❤️ HP: {battle.get('hp', 0)}"
        e_atk_text.value = f"⚔️ Атака макс.: {emx_dmg}"
        e_def_text.value = f"🛡️ Захист макс.: {emx_def}"

        page.update()

    def persist_state():
        write_json(USERS_FILE, users)
        write_json(BATTLE_FILE, battle)

    def reset_enemy():
        write_json(BATTLE_FILE, {})
        battle.clear()

    def show_message(title: str, message: str, color=ft.Colors.BLUE_300):
        def close_dialog(e):
            page.pop_dialog()
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=CARD_BG,
            title=ft.Text(
                title,
                size=22,
                weight=ft.FontWeight.BOLD,
                color=color,
            ),
            content=ft.Text(
                message,
                size=16,
                color=TEXT_PRIMARY,
            ),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
        )
        page.show_dialog(dlg)

    def check_outcome():
        if player["stats"]["hp"] <= 0 and battle.get("hp", 0) <= 0:
            return "draw"
        if battle.get("hp", 0) <= 0:
            return "win"
        if player["stats"]["hp"] <= 0:
            return "lose"
        return None

    def apply_defeat_penalty():
        gold = int(player["stats"].get("gold", 0))
        penalty = int(gold * GOLD_PENALTY_PERCENT)
        player["stats"]["gold"] = max(0, gold - penalty)
        return penalty

    def try_level_up():
        level = int(player["stats"].get("level", 1))
        exp = int(player["stats"].get("exp", 0))
        exp_needed = level * 100

        if exp < exp_needed:
            return None

        player["stats"]["level"] = level + 1
        player["stats"]["exp"] = exp - exp_needed
        player["stats"]["damage"] = int(player["stats"].get("damage", 0)) + 3
        player["stats"]["defense"] = int(player["stats"].get("defense", 0)) + 2
        player["stats"]["hp"] = int(player["stats"].get("hp", 0)) + 10

        return (
            f"🎉 Новий рівень: {level + 1}\n"
            f"+3 атаки, +2 захисту, +10 HP\n"
            f"До наступного рівня: {(level + 1) * 100} EXP"
        )

    def finish_battle(outcome: str):
        if outcome == "win":
            earned_gold = int(battle.get("gold", 0))
            earned_exp = int(battle.get("exp", 0))
            player["stats"]["gold"] = int(player["stats"].get("gold", 0)) + earned_gold
            player["stats"]["exp"] = int(player["stats"].get("exp", 0)) + earned_exp

            levelup_msg = try_level_up()

            title = "🏆 Перемога!"
            color = ft.Colors.GREEN_300
            message = (
                f"Ти переміг {battle.get('enemy', 'ворога')}.\n"
                f"Отримано: {earned_gold} золота, {earned_exp} EXP."
            )
            if levelup_msg:
                message += f"\n\n{levelup_msg}"

        elif outcome == "lose":
            penalty = apply_defeat_penalty()
            title = "💀 Поразка"
            color = ft.Colors.RED_300
            message = (
                "Ти програв бій.\n"
                f"Штраф: -{penalty} золота."
            )
        else:
            title = "🤝 Нічия"
            color = ft.Colors.ORANGE_300
            message = "Обидва впали одночасно. Це нічия."

        persist_state()
        reset_enemy()

        def go_to_battle(e):
            page.pop_dialog()
            page.go("/battle")
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=CARD_BG,
            title=ft.Text(
                title,
                size=22,
                weight=ft.FontWeight.BOLD,
                color=color,
            ),
            content=ft.Text(message, size=16, color=TEXT_PRIMARY),
            actions=[ft.TextButton("OK", on_click=go_to_battle)],
        )
        page.show_dialog(dlg)

    def make_single_choice_group(options):
        checkboxes = []

        def on_change(e):
            for cb in checkboxes:
                if cb is not e.control:
                    cb.value = False
            e.control.value = True
            selected_action["value"] = e.control.data
            page.update()

        for opt in options:
            cb = ft.Checkbox(
                label=opt["name"],
                value=False,
                data=opt,
                on_change=on_change,
                fill_color=ACCENT,
                check_color=ft.Colors.WHITE,
                label_style=ft.TextStyle(color=TEXT_PRIMARY),
            )
            checkboxes.append(cb)

        return checkboxes

    def on_attack_click(e):
        options = get_player_actions(player["stats"], "atk").get("attacks", [])
        selected_action["value"] = None

        if not options:
            raw_dmg = player["stats"].get("damage", 0)

            player_dmg = crit(
                raw_dmg,
                0.25,
                max_dmg=int(raw_dmg * 2),
            )

            enemy_def = int(
                battle.get("defense", 0) * enemy_multiplier()
            )

            damage_to_enemy = apply_def(player_dmg, enemy_def)
            battle["hp"] = max(0, battle.get("hp", 0) - damage_to_enemy)

            action_area.controls.clear()
            persist_state()
            refresh_ui()

            outcome = check_outcome()
            if outcome:
                finish_battle(outcome)
                return

            show_message(
                "⚔️ Звичайна атака",
                (
                    f"Ти завдав ворогу {damage_to_enemy} шкоди.\n\n"
                    f"Атака: {player_dmg}\n"
                    f"Захист ворога: {enemy_def}"
                ),
                ft.Colors.ORANGE_300,
            )
            return

        def on_confirm_attack(e):
            chosen = selected_action["value"]

            if chosen is None:
                show_message(
                    "Увага",
                    "Спочатку вибери атаку.",
                    ft.Colors.ORANGE_300,
                )
                return

            pmx_dmg, _, _, emx_def = recalc_limits()

            raw_dmg = (
                player["stats"].get("damage", 0)
                * chosen.get("damage_mult", 1)
            )

            player_dmg = crit(
                raw_dmg,
                0.25,
                max_dmg=pmx_dmg,
            )

            enemy_def = min(
                int(
                    battle.get("defense", 0)
                    * enemy_multiplier()
                ),
                emx_def,
            )

            damage_to_enemy = apply_def(player_dmg, enemy_def)
            battle["hp"] = max(0, battle.get("hp", 0) - damage_to_enemy)

            action_area.controls.clear()
            persist_state()
            refresh_ui()

            outcome = check_outcome()
            if outcome:
                finish_battle(outcome)
                return

            show_message(
                f"⚔️ {chosen['name']}",
                (
                    f"Ти завдав ворогу {damage_to_enemy} шкоди.\n\n"
                    f"Атака: {player_dmg}\n"
                    f"Захист ворога: {enemy_def}"
                ),
                ft.Colors.GREEN_300,
            )

        action_area.controls = [
            ft.Container(
                padding=12,
                border_radius=14,
                bgcolor=CARD_BG_LIGHT,
                border=ft.border.all(1, "#334155"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text(
                            "Оберіть атаку:",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        *make_single_choice_group(options),
                        ft.ElevatedButton(
                            "Підтвердити",
                            on_click=on_confirm_attack,
                            style=ft.ButtonStyle(
                                bgcolor=RED_BTN,
                                color=ft.Colors.WHITE,
                                padding=14,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                        ),
                    ],
                ),
            )
        ]
        page.update()

    def on_defense_click(e):
        options = get_player_actions(player["stats"], "def").get("defenses", [])
        selected_action["value"] = None

        if not options:
            enemy_attacks = battle.get("attacks", [])

            enemy_attack = (
                random.choice(enemy_attacks)
                if enemy_attacks
                else {"name": "Звичайний удар", "damage_mult": 1}
            )

            raw_edmg = (
                battle.get("damage", 0)
                * enemy_multiplier()
                * enemy_attack.get("damage_mult", 1)
            )

            enemy_dmg = crit(
                raw_edmg,
                0.15,
                max_dmg=int(raw_edmg * 2),
            )

            player_def = player["stats"].get("defense", 0)
            damage_to_player = apply_def(enemy_dmg, player_def)

            player["stats"]["hp"] = max(
                0,
                player["stats"]["hp"] - damage_to_player,
            )

            persist_state()
            refresh_ui()

            outcome = check_outcome()
            if outcome:
                finish_battle(outcome)
                return

            show_message(
                "🛡️ Базовий захист",
                (
                    f"Противник використав {enemy_attack['name']}.\n\n"
                    f"Отримано шкоди: {damage_to_player}\n"
                    f"Атака ворога: {enemy_dmg}\n"
                    f"Твій захист: {player_def}"
                ),
                ft.Colors.BLUE_300,
            )
            return

        def on_confirm_defense(e):
            chosen = selected_action["value"]

            if chosen is None:
                show_message(
                    "Увага",
                    "Спочатку вибери захист.",
                    ft.Colors.ORANGE_300,
                )
                return

            _, pmx_def, emx_dmg, _ = recalc_limits()

            raw_pdef = (
                player["stats"].get("defense", 0)
                * chosen.get("defense_mult", 1)
                * 1.5
            )

            player_def = min(
                int(raw_pdef),
                int(pmx_def * 1.5),
            )

            enemy_attacks = battle.get("attacks", [])

            enemy_attack = (
                random.choice(enemy_attacks)
                if enemy_attacks
                else {"name": "Звичайний удар", "damage_mult": 1}
            )

            raw_edmg = (
                battle.get("damage", 0)
                * enemy_multiplier()
                * enemy_attack.get("damage_mult", 1)
            )

            enemy_dmg = crit(
                raw_edmg,
                0.15,
                max_dmg=emx_dmg,
            )

            damage_to_player = apply_def(enemy_dmg, player_def)
            player["stats"]["hp"] = max(
                0,
                player["stats"]["hp"] - damage_to_player,
            )

            action_area.controls.clear()
            persist_state()
            refresh_ui()

            outcome = check_outcome()
            if outcome:
                finish_battle(outcome)
                return

            show_message(
                f"🛡️ {chosen['name']}",
                (
                    f"Противник використав {enemy_attack['name']}.\n\n"
                    f"Отримано шкоди: {damage_to_player}\n"
                    f"Атака ворога: {enemy_dmg}\n"
                    f"Твій захист: {player_def}"
                ),
                ft.Colors.BLUE_300,
            )

        action_area.controls = [
            ft.Container(
                padding=12,
                border_radius=14,
                bgcolor=CARD_BG_LIGHT,
                border=ft.border.all(1, "#334155"),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text(
                            "Оберіть захист:",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),
                        *make_single_choice_group(options),
                        ft.ElevatedButton(
                            "Підтвердити",
                            on_click=on_confirm_defense,
                            style=ft.ButtonStyle(
                                bgcolor=BLUE_BTN,
                                color=ft.Colors.WHITE,
                                padding=14,
                                shape=ft.RoundedRectangleBorder(radius=12),
                            ),
                        ),
                    ],
                ),
            )
        ]
        page.update()

    def open_shop(e):
        page.go("/shop")

    def open_inventory(e):
        page.go("/inventory")

    def on_exit_click(e):
        def confirm_exit(e):
            apply_defeat_penalty()
            persist_state()
            reset_enemy()
            page.pop_dialog()
            page.go("/")
            page.update()

        def cancel_exit(e):
            page.pop_dialog()
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor="#0F172A",
            title=ft.Text(
                "Вихід з бою",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),
            content=ft.Text(
                "Ти справді хочеш вийти з бою?\n"
                "Це буде зараховано як поразка, і ти втратиш частину золота.",
                size=15,
                color=TEXT_PRIMARY,
            ),
            actions=[
                ft.TextButton("Так", on_click=confirm_exit),
                ft.TextButton("Ні", on_click=cancel_exit),
            ],
        )
        page.show_dialog(dlg)

    player_image = ft.Container(
        width=280,
        height=400,
        border_radius=20,
        bgcolor="#FFFFFF1A",
        border=ft.border.all(1, "#FFFFFF26"),
        content=ft.Image(
            src=player["stats"].get("photo"),
            fit=ft.BoxFit.CONTAIN,
        ),
    )

    enemy_image = ft.Container(
        width=280,
        height=400,
        border_radius=20,
        bgcolor="#FFFFFF1A",
        border=ft.border.all(1, "#FFFFFF26"),
        content=ft.Image(
            src=battle.get("photo_atk"),
            fit=ft.BoxFit.CONTAIN,
        ),
    )

    player_panel = ft.Container(
        width=330,
        padding=16,
        bgcolor=CARD_BG,
        border_radius=20,
        border=ft.border.all(2, CARD_BORDER),
        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=1,
            color="#00000055",
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "Гравець",
                    size=18,
                    color=ACCENT,
                    weight=ft.FontWeight.BOLD,
                ),
                player_image,
                p_name_text,
                ft.Divider(color="#334155"),
                p_class_text,
                p_hp_text,
                p_atk_text,
                p_def_text,
                p_lvl_text,
                p_exp_text,
            ],
        ),
    )

    enemy_panel = ft.Container(
        width=330,
        padding=16,
        bgcolor=CARD_BG,
        border_radius=20,
        border=ft.border.all(2, CARD_BORDER),
        shadow=ft.BoxShadow(
            blur_radius=18,
            spread_radius=1,
            color="#00000055",
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    "☠ Супротивник",
                    size=18,
                    color=ACCENT,
                    weight=ft.FontWeight.BOLD,
                ),
                enemy_image,
                e_name_text,
                ft.Divider(color="#334155"),
                e_type_text,
                e_hp_text,
                e_atk_text,
                e_def_text,
            ],
        ),
    )

    attack_btn = ft.ElevatedButton(
        "⚔ Атака",
        width=180,
        height=54,
        style=ft.ButtonStyle(
            bgcolor=ACCENT,
            color=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=14),
        ),
        on_click=on_attack_click,
    )

    defense_btn = ft.ElevatedButton(
        "🛡 Захист",
        width=180,
        height=54,
        style=ft.ButtonStyle(
            bgcolor=BLUE_BTN,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
        ),
        on_click=on_defense_click,
    )

    exit_btn = ft.ElevatedButton(
        "🚪 Вийти",
        width=180,
        height=54,
        style=ft.ButtonStyle(
            bgcolor=GREY_BTN,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
        ),
        on_click=on_exit_click,
    )

    invent_btn = ft.Container(
        border=ft.border.all(2, CARD_BORDER),
        border_radius=15,
        bgcolor=CARD_BG,
        content=ft.IconButton(
            icon=ft.Icons.INVENTORY_2,
            icon_color=ACCENT,
            icon_size=30,
            tooltip="Інвентар",
            on_click=open_inventory,
        ),
    )

    shop_btn = ft.Container(
        border=ft.border.all(2, CARD_BORDER),
        border_radius=15,
        bgcolor=CARD_BG,
        content=ft.IconButton(
            icon=ft.Icons.STORE,
            icon_color=ACCENT,
            icon_size=30,
            tooltip="Магазин",
            on_click=open_shop,
        ),
    )

    refresh_ui()

    content = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                image=ft.DecorationImage(
                    src="main_photo.jpg",
                    fit=ft.BoxFit.COVER,
                ),
            ),
            ft.Container(
                expand=True,
                bgcolor="#0B1220A8",
                padding=0,
                content=ft.Column(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Container(
                            expand=True,
                            padding=0,
                            content=ft.Row(
                                expand=True,
                                spacing=0,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.Alignment.TOP_LEFT,
                                        padding=0,
                                        content=player_panel,
                                    ),
                                    ft.Container(
                                        width=240,
                                        alignment=ft.Alignment.CENTER,
                                        padding=0,
                                        content=ft.Container(
                                            padding=16,
                                            border_radius=20,
                                            bgcolor=CARD_BG,
                                            border=ft.border.all(2, CARD_BORDER),
                                            shadow=ft.BoxShadow(
                                                blur_radius=18,
                                                spread_radius=1,
                                                color="#00000055",
                                            ),
                                            content=ft.Column(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                spacing=16,
                                                controls=[
                                                    attack_btn,
                                                    defense_btn,
                                                    action_area,
                                                ],
                                            ),
                                        ),
                                    ),
                                    ft.Container(
                                        expand=True,
                                        alignment=ft.Alignment.TOP_RIGHT,
                                        padding=0,
                                        content=enemy_panel,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=12,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=16,
                                controls=[
                                    invent_btn,
                                    shop_btn,
                                    exit_btn,
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )

    return ft.View(
        route="/battle",
        controls=[content],
    )