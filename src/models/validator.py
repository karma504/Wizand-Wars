import re

def validate_register(user, email, password, repeat_password, agree):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not user:
        return "Введи ім'я"

    if len(user) < 3:
        return "Ім'я коротке"

    if not email:
        return "Введи email"

    if not re.match(pattern, email):
        return "Некоректний email"

    if not password:
        return "Введи пароль"

    if len(password) <= 5:
        return "Пароль занадто короткий"

    if password != repeat_password:
        return "Паролі не співпадають"

    if not any(p.isalpha() for p in password):
        return "Пароль має містити літери"

    if not any(p.isdigit() for p in password):
        return "Пароль має містити цифри"

    if not any(not p.isalnum() for p in password):
        return "Пароль має містити спецсимвол"

    if not agree:
        return "Потрібно прийняти умови"

    return "ok"