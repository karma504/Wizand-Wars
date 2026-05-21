from .load_json import read_json, write_json


def register_user(user, email, password):
    users = read_json("../storage/user.json") or {}

    # перевірка на дублікати
    for u in users:
        if u.get("email") == email:
            return {"ok": False, "error": "Користувач вже існує"}

    users.append({
        "user": user,
        "email": email,
        "password": password
    })

    write_json("user.json",users )

    return {"ok": True}


def login_user(email, password):
    if not email:
        return {"ok": False, "error": "Введіть email"}

    if not password:
        return {"ok": False, "error": "Введіть пароль"}

    users = read_json("user.json") or []

    for u in users:
        if u.get("email") == email and u.get("password") == password:
            return {"ok": True}

    return {"ok": False, "error": "Невірний email або пароль"}