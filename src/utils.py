import json
import typing
import sys

import argon2
from rich.panel import Panel
from rich import print as r_print

import config as cnf

def read_json(path: str, care_if_db_is_not_dict: bool=True):
    with open(path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            if care_if_db_is_not_dict:
                print(cnf.RED + cnf.DB_TYPE_IS_NOT_DICT_ERROR)

                sys.exit(1)
            
            return None

        if (type(data) is not dict) and (care_if_db_is_not_dict):
            print(cnf.RED + cnf.DB_TYPE_IS_NOT_DICT_ERROR)

            sys.exit(1)

        return data

def write_json(path: str, data: typing.Any, compact_mode: bool=False):
    """
    Функция для записи данных в JSON
    """

    with open(path, "w", encoding="utf-8") as file:
        if compact_mode:
            json.dump(data, file, ensure_ascii=False)
        else:
            json.dump(data, file, ensure_ascii=False, indent=4)

def argon2_hash(text: str) -> str:
    ph = argon2.PasswordHasher()
    text_hash = ph.hash(text)

    return text_hash

def verify_password(text_hash: str, new_text: str):
    ph = argon2.PasswordHasher()

    try:
        return ph.verify(text_hash, new_text)
    except argon2.exceptions.VerifyMismatchError:
        return False
    except Exception as e:
        print(cnf.RED + "[OOPS] Критическая ошибка: если Вы видите это сообщение, то этого сообщения Вы видеть не должны!")
        print(cnf.RED + "[OOPS] Сообщите об этой ошибке разработчикам!")
        print(cnf.RED + f"[OOPS] Код ошибки: {e.__class__.__name__}")

        return False

def check_profile(username: str, hide_some_info: bool = True) -> None:
    db = read_json(cnf.DB_FILE)
    user_to_check = db.get(username)

    if user_to_check is None:
        print(cnf.RED + "[!] Пользователь не найден в базе данных!")

        return

    string_to_show = ""
    index = 0

    for name, value in user_to_check.items():
        if name == "password":
            # В целях безопасности
            continue
        elif (hide_some_info) and (name in cnf.DONT_SHOW_THIS_ON_CHECK_PROFILE):
            # Некоторые поля (например: заблокирован ли Ваш аккаунт) показывать пользователю не стоит (не информативно)
            # Так как если мы уже зашли в профиль, то очевидно, что наш аккаунт не заблокирован
            # Однако админу, который смотрит профиль пользователя, эта информация может помочь!

            continue
        elif name == "rank":
            rank_info = cnf.RANK_DB[value]

            if rank_info["color"]:
                value = rank_info["color"] + rank_info["name"] + cnf.RESET
            else:
                value = rank_info["name"]

        index += 1

        human_name = cnf.DB_DECODES.get(name)
        string_to_show += f"{index}) {human_name if human_name else name}: {value}\n"

    user_panel = Panel(string_to_show.rstrip(), title="Информация о пользователе:")
    r_print(user_panel)
