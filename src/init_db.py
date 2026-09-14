import secrets
import sys

import pwinput
import questionary

import config as cnf
import utils

def init():
    while True:
        login = input("[?] Введите имя первого пользователя (владельца): ")
        password = pwinput.pwinput("[?] Введите пароль: ")
        confirm_password = pwinput.pwinput("[?] Подтвердите пароль: ")

        if login in cnf.BANNED_USERNAMES:
            print(cnf.RED + cnf.BANNED_USERNAME_ERROR)

            continue

        if secrets.compare_digest(password, confirm_password):
            password_hash = utils.argon2_hash(password)

            db = {login: {"password": password_hash, "rank": 1, "role": "owner", "current_elo": 0, "ban_status": False, "ban_admin": None, "ban_time": None, "ban_reason": None}}
            utils.write_json(cnf.DB_FILE, db)

            print(cnf.GREEN + "[!] БД успешно инициализирована! Выход из установщика...")
            sys.exit()
        else:
            print(cnf.RED + "[!] Пароли не совпадают")


def start_setup():
    try:
        db = utils.read_json(cnf.DB_FILE, care_if_db_is_not_dict=False)
    except FileNotFoundError:
        print(cnf.RED + "[!] Файла с БД не существует!")

        create_db_question = questionary.confirm("[CREATE] Создать?")
        create_db_answer = create_db_question.ask()

        if create_db_answer:
            init()
        else:
            sys.exit()
    else:
        if (type(db) is not dict) or (db == {}):
            print(cnf.RED + "[!] Кажется, что файл БД был сильно повреждён.")

            wipe_db_question = questionary.confirm("[CREATE] Стереть БД и начать всё с начала?")
            wipe_db_choice = wipe_db_question.ask()

            if wipe_db_choice:
                init()
            else:
                sys.exit()
        else:
            print(cnf.BLUE + "[INFO] Всё хорошо. БД успешно создана и настроена. Всё равно начать с нуля?")

            wipe_db_question = questionary.confirm("Ваш выбор?")
            wipe_db_choice = wipe_db_question.ask()

            if wipe_db_choice:
                init()
            else:
                sys.exit()

if __name__ == "__main__":
    start_setup()
