import flet as ft
import random
from load_json import read_json



characters_data = read_json("../storage/person.json")

current_hero = None
current_enemy = None
page_ref = None




class Character:
    def init(self, class_name: str, hp: int, damage: int,
                 defense: int, level: int, gold: int, photo):
        self.class_name = class_name
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.level = level
        self.gold = gold
        self.photo = photo

    def build_card(self) -> ft.Container:
        """Create character button card"""
        img =ft.Container(ft.Image(
        src= self.photo)
        ,expand=True)

        return ft.Container(
            expand=True,
            content=ft.Button(
                on_click=lambda e: open_character_page(e.page, self.class_name),

                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                        ft.Text(self.class_name.upper(), size=20),

                        img,

                        ft.Text(f"❤️ HP: {self.hp}"),
                        ft.Text(f"⚔️ ATK: {self.damage}"),
                        ft.Text(f"🛡 DEF: {self.defense}"),
                    ]
                )
            )
        )


class Entity:
    def init(self, name, hp, damage, defense=0, level=1, gold=0, exp=0, entity_type="hero",photo=""):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.level = level
        self.gold = gold
        self.exp = exp
        self.entity_type = entity_type
        self.photo = photo

    def create_hero(self,data):
        return Entity(
            name=data["class"],
            hp=data["hp"],
            damage=data["damage"],
            defense=data["defense"],
            level=data["level"],
            gold=data["gold"],
            entity_type="hero",
            photo=data["photo_atk"]
        )


    def create_enemy(self,data):
        return Entity(
            name=data["name"],
            hp=data["hp"],
            damage=data["damage"],
            gold=data["gold"],
            exp=data["exp"],
            entity_type="enemy",
            photo=data["photo_atk"]
        )


def get_character_by_class(class_name):
    """Find character in JSON by class name"""
    for char in characters_data["characters"]:
        if char["class"] == class_name:
            return char

def open_character_page(page: ft.Page, class_name):
    """Start battle after choosing hero"""


    hero_data = get_character_by_class(class_name)
    hero = Entity.create_hero(hero_data)

    def generate_enemy(hero_level: int):
        """Random enemy generator based on hero level"""

        data = read_json('../storage/enemies.json')


        if hero_level <= 10:
            chances = {"common": 80, "rare": 15, "elite": 5, "boss": 0}
        elif hero_level <= 25:
            chances = {"common": 60, "rare": 25, "elite": 10, "boss": 5}
        elif hero_level <= 50:
            chances = {"common": 40, "rare": 30, "elite": 20, "boss": 10}
        else:
            chances = {"common": 25, "rare": 30, "elite": 25, "boss": 20}


        roll = random.randint(1, 100)
        cumulative = 0
        rarity = "common"

        for r, chance in chances.items():
            cumulative += chance
            if roll <= cumulative:
                rarity = r
                break

        enemy_data = random.choice(data[rarity])

        return Entity.create_enemy(enemy_data)

    enemy = generate_enemy(hero.level)

    open_battle_screen(page, hero, enemy)

def build_stats_panel(entity: Entity):

    return ft.Container(

            content=ft.Column(
                spacing=6,
                controls=[

                    ft.Text(entity.name.upper()),
                    ft.Text(f"❤️ HP {entity.hp}/{entity.max_hp}"),
                    ft.ProgressBar(value=entity.hp / entity.max_hp),

                    ft.Text(f"⚔️ ATTACK {entity.damage}"),
                    ft.ProgressBar(value=1),

                    *(
                        [
                            ft.Text(f"🛡 DEFENCE {entity.defense}"),
                            ft.ProgressBar(value=1),
                        ] if entity.defense > 0 else []
                    ),

                    *(
                        [
                            ft.Text(f"⭐️ LEVEL {entity.level}"),
                            ft.ProgressBar(value=entity.level / 100),
                        ] if entity.entity_type == "hero" else []
                    ),

                    *(
                        [
                            ft.Text(f"✨ EXP {entity.exp}"),
                        ] if entity.entity_type == "enemy" else []
                    ),

                    ft.Text(f"🪙 GOLD {entity.gold}"),
                ]
        )
    )



def open_battle_screen(page: ft.Page, hero: Entity, enemy: Entity):
        global current_hero, current_enemy, page_ref

        page_ref = page
        current_hero = hero
        current_enemy = enemy
        page.controls.clear()

        left_panel = build_stats_panel(hero)
        right_panel = build_stats_panel(enemy)

        def attack(e):
            pass



        hero_sprite = ft.Image(
            src=hero.photo,
            width=350,
            height=350
        )

        enemy_sprite = ft.Image(
            src=enemy.photo,
            width=350,
            height=350,
        )

        sprites = ft.Row(
            [
                ft.Container(hero_sprite, alignment=ft.Alignment.CENTER_LEFT),
                ft.Container(expand=True),
                ft.Container(enemy_sprite, alignment=ft.Alignment.CENTER_RIGHT),
            ],
            expand=True
        )

        bottom_panel = ft.Container(
            content=ft.Row(
                [
                    ft.Button("⚔️ Attack",on_click=attack),
                    ft.Button("🧪 Shop",),
                    ft.Button("🎒 Inventory"),
                    ft.Button("⬅️ Back", on_click=lambda e: open_game_screen(e.page))
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            )
        )



        page.add(
            ft.Stack(
                expand=True,
                controls=[
                    sprites,

                    ft.Column(
                        [
                            ft.Row(
                                [
                                    left_panel,
                                    ft.Container(expand=True),
                                    right_panel
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            bottom_panel
                        ],
                        expand=True
                    )
                ]
            )
        )



def open_game_screen(page: ft.Page):
    """Main screen with character list"""
    page.controls.clear()

    character_cards = []

    for char in characters_data["characters"]:
        character = Character(
            char["class"],
            char["hp"],
            char["damage"],
            char["defense"],
            char["level"],
            char["gold"],
            char["photo"]
            )
        character_cards.append(character.build_card())

    page.add(ft.Row(character_cards, expand=True))


