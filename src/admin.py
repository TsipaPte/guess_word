import datetime

import questionary

import config as cnf
import settings
import user
import utils

def menu(username: str) -> None:
    while True:
        admin_menu = questionary.select("[ADMIN] Выберите:", cnf.ADMIN_MENU, use_shortcuts=True)
        admin_choice = admin_menu.ask()

        if admin_choice == cnf.EXIT_OPTION:
            break
        elif admin_choice == "В режим пользователя":
            user.menu(username, return_instead_exit=True)
        elif admin_choice == "Заблокировать пользователя":
            ban_user(username, "admin")
        elif admin_choice == "Разблокировать пользователя":
            unban_user("admin")
        elif admin_choice == "Настройки":
            settings.menu(username)

def ban_user(username: str, permission_level: str) -> None:
    db = utils.read_json(cnf.DB_FILE)
    users_available_to_ban = []

    for name, data in db.items():
        if not(data["ban_status"]): # Если не заблокирован
            if permission_level == "admin":
                if data["role"] == "user": # Только если пользователь, админа и уж тем более владельца админ заблокировать не может!
                    users_available_to_ban.append(name)
            elif permission_level == "owner": # Если владелец, то права не ограничены
                users_available_to_ban.append(name)

    users_available_to_ban.append(cnf.CANCEL_OPTION)

    ban_menu = questionary.select("[BAN] Выберите, кого заблокировать:", users_available_to_ban, use_shortcuts=True)
    user_to_ban = ban_menu.ask()

    if (user_to_ban is None) or (user_to_ban == cnf.EXIT_OPTION):
        print(cnf.RED + "[!] Отмена")

        return

    time_choice_menu = questionary.select("[BAN] Выберите тип времени:", ("Количество дней", "Навсегда", cnf.CANCEL_OPTION), use_shortcuts=True)
    time_chosen = time_choice_menu.ask()

    if (time_chosen is None) or (time_chosen == cnf.CANCEL_OPTION):
        print(cnf.RED + "[!] Отмена")

        return

    if time_chosen == "Количество дней":
        while True:
            try:
                days_to_ban = int(input("[?] Введите количество дней: "))
            except ValueError:
                print(cnf.RED + "[!] Это не число!")
            else:
                now = datetime.datetime.now()
                ban_time = now + datetime.timedelta(days=days_to_ban)
                ban_time = ban_time.strftime("%d-%m-%Y %H:%M:%S")

                break

    elif time_chosen == "Навсегда":
        ban_time = "inf"

    reason = input("[?] Введите причину: ")

    db[user_to_ban]["ban_status"] = True
    db[user_to_ban]["ban_admin"] = username
    db[user_to_ban]["ban_time"] = ban_time
    db[user_to_ban]["ban_reason"] = reason

    utils.write_json(cnf.DB_FILE, db)

def unban_user(permission_level: str) -> None:
    db = utils.read_json(cnf.DB_FILE)
    users_available_to_unban = []

    for name, data in db.items():
        if data["ban_status"]: # Если заблокирован, то мы можем его разблокировать
            if permission_level == "admin":
                if data["role"] == "user":
                    users_available_to_unban.append(name)
            elif permission_level == "owner":
                users_available_to_unban.append(name)

    users_available_to_unban.append(cnf.CANCEL_OPTION)

    unban_menu = questionary.select("[UNBAN] Выберите, кого разблокировать:", users_available_to_unban, use_shortcuts=True)
    user_to_unban = unban_menu.ask()

    if (user_to_unban is None) or (user_to_unban == cnf.CANCEL_OPTION):
        print(cnf.RED + "[!] Отмена")

        return

    db[user_to_unban]["ban_status"] = False
    db[user_to_unban]["ban_admin"] = None
    db[user_to_unban]["ban_time"] = None
    db[user_to_unban]["ban_reason"] = None

    utils.write_json(cnf.DB_FILE, db)
