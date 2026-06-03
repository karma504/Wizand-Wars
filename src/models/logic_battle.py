import random


def get_max_damage(base_damage, attacks):
    if not attacks:
        return int(base_damage)
    max_mult = max(a.get("damage_mult", 1) for a in attacks)
    return int(base_damage * max_mult)


def get_max_defense(base_defense, defenses):
    if not defenses:
        return int(base_defense)
    max_mult = max(d.get("defense_mult", 1) for d in defenses)
    return int(base_defense * max_mult)


def crit(dmg, chance=0.2, max_dmg=None):
    if random.random() < chance:
        result = int(dmg * 2)
    else:
        result = int(dmg)

    if max_dmg is not None:
        result = min(result, int(max_dmg))

    return result


def apply_def(dmg, defense):
    reduced = dmg - defense
    if reduced > 0:
        return int(reduced)
    return int(dmg * 0.25)


def get_player_actions(player_stats, atk_def):
    if atk_def == "atk":
        attacks = player_stats.get("attacks", [])
        return {
            "attacks": random.sample(attacks, k=min(3, len(attacks)))
        }
    elif atk_def == "def":
        defenses = player_stats.get("defenses", [])
        return {
            "defenses": random.sample(defenses, k=min(3, len(defenses)))
        }
    return {}


def get_enemy_action(enemy, atk_def):
    if atk_def == "atk":
        attack = random.choice(enemy.get("attacks", [])) if enemy.get("attacks") else None
        return {"attack": attack}
    if atk_def == "def":
        defense = random.choice(enemy.get("defenses", [])) if enemy.get("defenses") else None
        return {"defense": defense}
    return {}


def battle_round(
        player_hp,
        enemy_hp,
        player_action,
        enemy_action,
        player,
        enemy,
        enemy_type="common"
):
    multipliers = {
        "common": 1,
        "rare": 1.5,
        "elite": 2.5,
        "boss": 3
    }

    multiplier = multipliers.get(enemy_type, 1)

    player_base_damage = player["damage"]
    player_base_defense = player["defense"]

    player_attack = random.choice(player.get("attacks", [])) if player.get("attacks") else {"damage_mult": 1}
    player_defense = random.choice(player.get("defenses", [])) if player.get("defenses") else {"defense_mult": 1}

    player_damage = player_base_damage * player_attack.get("damage_mult", 1)
    player_defense_value = player_base_defense * player_defense.get("defense_mult", 1)

    player_max_dmg = get_max_damage(player_base_damage, player.get("attacks", []))
    player_max_def = get_max_defense(player_base_defense, player.get("defenses", []))

    player_damage = crit(player_damage, 0.25, max_dmg=player_max_dmg)
    player_defense_value = min(int(player_defense_value), player_max_def)

    enemy_base_damage = enemy["damage"]
    enemy_base_defense = enemy["defense"]

    enemy_attack = random.choice(enemy.get("attacks", [])) if enemy.get("attacks") else {"damage_mult": 1}
    enemy_defense = random.choice(enemy.get("defenses", [])) if enemy.get("defenses") else {"defense_mult": 1}

    enemy_damage = enemy_base_damage * enemy_attack.get("damage_mult", 1) * multiplier
    enemy_defense_value = enemy_base_defense * enemy_defense.get("defense_mult", 1) * multiplier

    enemy_max_dmg = get_max_damage(enemy_base_damage * multiplier, enemy.get("attacks", []))
    enemy_max_def = get_max_defense(enemy_base_defense * multiplier, enemy.get("defenses", []))

    enemy_damage = crit(enemy_damage, 0.15, max_dmg=enemy_max_dmg)
    enemy_defense_value = min(int(enemy_defense_value), enemy_max_def)

    damage_to_player = 0
    damage_to_enemy = 0

    if player_action == "attack" and enemy_action == "attack":
        damage_to_enemy = apply_def(player_damage, enemy_defense_value)
        damage_to_player = apply_def(enemy_damage, player_defense_value)

    elif player_action == "attack" and enemy_action == "defense":
        damage_to_enemy = apply_def(player_damage, enemy_defense_value * 1.5)

    elif player_action == "defense" and enemy_action == "attack":
        damage_to_player = apply_def(enemy_damage, player_defense_value * 1.5)

    elif player_action == "defense" and enemy_action == "defense":
        damage_to_player = 0
        damage_to_enemy = 0

    player_hp -= damage_to_player
    enemy_hp -= damage_to_enemy

    if player_hp <= 0 and enemy_hp <= 0:
        return "Ничія"

    if enemy_hp <= 0:
        return "Вийграш"

    if player_hp <= 0:
        return "Поразка"

    return {
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "player_damage": int(player_damage),
        "enemy_damage": int(enemy_damage),
        "player_defense": int(player_defense_value),
        "enemy_defense": int(enemy_defense_value),
        "damage_to_player": damage_to_player,
        "damage_to_enemy": damage_to_enemy,
        "player_attack_used": player_attack.get("name"),
        "enemy_attack_used": enemy_attack.get("name"),
    }

