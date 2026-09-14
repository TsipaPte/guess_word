import datetime
import secrets
import sys

import prompt_toolkit as ptk
import pwinput
import questionary

import admin
import config as cnf
import owner
import user
import utils

def login():
    db = utils.read_json(cnf.DB_FILE)

    users_list = list(db.keys())
    users_list.append(cnf.CANCEL_OPTION)

    users = questionary.select("Выберите в кого войти: ", users_list, use_shortcuts=True)
    user = users.ask()

    if (user is None) or (user == cnf.CANCEL_OPTION):
        sys.exit()

    correct_password = db[user]["password"]
    user_password = pwinput.pwinput("[?] Введите пароль от аккаунта: ")

    if utils.verify_password(correct_password, user_password):
        role = db[user]["role"]

        if db[user]["ban_status"]: # Если заблокирован
            current_date = datetime.datetime.now()
            ban_time_str = db[user]["ban_time"]
            ban_admin = db[user]["ban_admin"]
            ban_reason = db[user]["ban_reason"]

            if ban_time_str != "inf":
                ban_time_obj = datetime.datetime.strptime(db[user]["ban_time"], "%d-%m-%Y %H:%M:%S")

                if current_date > ban_time_obj:
                    print(cnf.GREEN + "[UNBAN] Вы были успешно разблокированы (срок блокировки прошёл)!")

                    db[user]["ban_status"] = False
                    db[user]["ban_time"] = None
                    db[user]["ban_admin"] = None
                    db[user]["ban_reason"] = None

                    utils.write_json(cnf.DB_FILE, db)
                else:
                    ban_window = ptk.shortcuts.message_dialog("Вы были заблокированы!", f"Ваш аккаунт был заблокирован за нарушение правил:\n\nДо: {ban_time_str}\nАдминистратором: {ban_admin}\nПричина: {ban_reason}", style=cnf.RED_PTK_STYLE)

                    ban_window.run()

                    sys.exit()
            else:
                    ban_window = ptk.shortcuts.message_dialog("Вы были заблокированы!", f"Ваш аккаунт был заблокирован за нарушение правил навсегда:\n\nАдминистратором: {ban_admin}\nПричина: {ban_reason}", style=cnf.RED_PTK_STYLE)

                    ban_window.run()

                    sys.exit()

        return user, role
    else:
        sys.exit()

def grant_access(username: str, role: str):
    if role == "owner":
        owner.menu(username)
    elif role == "admin":
        admin.menu(username)
    elif role == "user":
        user.menu(username)

def register():
    db = utils.read_json(cnf.DB_FILE)
    name = input("[?] Введите желаемое имя: ")

    if name in cnf.BANNED_USERNAMES:
        print(cnf.RED + cnf.BANNED_USERNAME_ERROR)

        return

    if name in db.keys():
        print(cnf.RED + "[!] Имя пользователя уже занято. Попробуйте другое!")

        return

    password = pwinput.pwinput("[?] Введите пароль: ")
    confirm_password = pwinput.pwinput("[?] Подтвердите пароль: ")

    if secrets.compare_digest(password, confirm_password):
        hash_of_password = utils.argon2_hash(password)

        db[name] = {"password": hash_of_password, "rank": 1, "role": "user", "current_elo": 0, "ban_status": False, "ban_admin": None, "ban_time": None, "ban_reason": None}

        utils.write_json(cnf.DB_FILE, db)

        print(cnf.GREEN + "[SUCCESS] Регистрация успешна!")
    else:
        print(cnf.RED + "[!] Пароли не совпадают!")

        return
