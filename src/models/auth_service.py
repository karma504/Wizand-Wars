from src.models.load_json import read_json, write_json


def register_user(user, email, password):
    users = read_json("storage/users.json") or []

    for u in users:
        if u.get("email") == email:
            return {"ok": False, "error": "Користувач вже існує"}

    new_user = {
        "user": user,
        "email": email,
        "password": password,
        "stats": {
            "class": "",
            "photo": "",
            "photo_atk": "",
            "hp": 0,
            "damage": 0,
            "defense": 0,
            "level": 0,
            "gold": 0,
            "inventory": [],
            "attacks":[],
            "defenses":[]
        },
        "enemy": None
    }

    users.append(new_user)

    write_json("storage/users.json", users)

    return {"ok": True}


def login_user(email, password):
    if not email:
        return {"ok": False, "error": "Введіть email"}

    if not password:
        return {"ok": False, "error": "Введіть пароль"}

    users = read_json("storage/users.json") or []

    for u in users:
        if u.get("email") == email and u.get("password") == password:
            return {"ok": True}

    return {"ok": False, "error": "Невірний email або пароль"}