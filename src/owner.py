import secrets
import sys

import pwinput
import questionary

import admin
import config as cnf
import utils
import user
import settings

def menu(username: str):
    while True:
        owner_menu = questionary.select("[OWNER] Выберите:", cnf.OWNER_MENU, use_shortcuts=True)
        choice = owner_menu.ask()

        if choice == cnf.EXIT_OPTION:
            sys.exit()
        elif choice == "В режим пользователя":
            user.menu(username, return_instead_exit=True)
        elif choice == "Создать учётную запись":
            create_account()
        elif choice == "Удалить учётную запись":
            delete_account()
        elif choice == "Просмотреть профиль пользователя":
            see_user_profile_as_owner()
        elif choice == "Заблокировать пользователя":
            admin.ban_user(username, "owner")
        elif choice == "Разблокировать пользователя":
            admin.unban_user("owner")
        elif choice == "Настройки":
            settings.menu(username)

def create_account():
    db = utils.read_json(cnf.DB_FILE)
    users = db.keys()

    wanted_username = input("[?] Введите имя нового пользователя: ")

    if wanted_username in users:
        print(cnf.RED + "[!] Данный пользователь уже существует!")

        return

    new_user_password = pwinput.pwinput("[?] Введите пароль: ")
    confirm_password = pwinput.pwinput("[?] Подтвердите пароль: ")

    if secrets.compare_digest(new_user_password, confirm_password):
        hashed_password = utils.argon2_hash(new_user_password)

        configurate_specific = questionary.confirm("[?] Сконфигурировать специфичные параметры (роль и ранг) или оставить их по умолчанию?")
        configurate_answer = configurate_specific.ask()

        if configurate_answer:
            rank_names = []

            for name in cnf.RANK_DB.values():
                rank_names.append(name)

            rank_names.append(cnf.CANCEL_OPTION)

            ranks_menu = questionary.select("[?] Выберите ранг:", rank_names, use_shortcuts=True)
            ranks_answer = ranks_menu.ask()

            if (ranks_answer is None) or (ranks_answer == cnf.CANCEL_OPTION):
                return

            for id_, data in cnf.RANK_DB.items():
                if data["name"] == ranks_answer:
                    rank_id = id_
                    break

            role_menu = questionary.select("[?] Выберите роль:", tuple(cnf.ROLES.keys()), use_shortcuts=True)
            role = cnf.ROLES[role_menu.ask()]

            db[wanted_username] = {"password": hashed_password, "rank": rank_id, "role": role, "current_elo": cnf.RANK_DB[rank_id]["needs_elo"], "ban_status": False, "ban_admin": None, "ban_time": None, "ban_reason": None}
        else:
            db[wanted_username] = {"password": hashed_password, "rank": 1, "role": "user", "current_elo": 0, "ban_status": False, "ban_admin": None, "ban_time": None, "ban_reason": None}

        utils.write_json(cnf.DB_FILE, db)
    else:
        print(cnf.RED + "[!] Пароли не совпадают!")

        return

def delete_account():
    db = utils.read_json(cnf.DB_FILE)
    users = list(db.keys())

    users.append(cnf.EXIT_OPTION)

    users_menu = questionary.select("[?] Выберите пользователя для удаления:", users, use_shortcuts=True)
    user_to_delete = users_menu.ask()

    if (user_to_delete is None) or (user_to_delete == cnf.EXIT_OPTION):
        return

    if db[user_to_delete]["role"] == "owner":
        print(cnf.RED + "[!] Нельзя удалить владельца")

        return

    confirm_option = questionary.confirm("[!!!] Подтвердить удаление пользователя?")
    confirm_answer = confirm_option.ask()

    if confirm_answer:
        del db[user_to_delete]

        utils.write_json(cnf.DB_FILE, db)

        print(cnf.GREEN + "[SUCCESS] Пользователь был успешно удалён!")

def see_user_profile_as_owner():
    db = utils.read_json(cnf.DB_FILE)
    users = list(db.keys())

    users.append(cnf.EXIT_OPTION)

    users_menu = questionary.select("Выберите того, чей профиль посмотреть:", users, use_shortcuts=True)
    selected_user = users_menu.ask()

    if (selected_user is None) or (selected_user == cnf.EXIT_OPTION):
        return

    utils.check_profile(selected_user, hide_some_info=False)
