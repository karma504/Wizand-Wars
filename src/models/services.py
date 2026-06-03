import random
from src.models.load_json import read_json


def generate_enemy(hero_level):

    data = read_json('storage/enemies.json')


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

    return enemy_data






