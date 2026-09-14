import sys
import time

import questionary

import config as cnf
import utils

def menu(username: str) -> None:
    while True:
        settings_menu = questionary.select("[SETTINGS] Выберите:", cnf.SETTINGS_MENU)
        settings_choice = settings_menu.ask()

        if settings_choice == cnf.EXIT_OPTION:
            return
        elif settings_choice == "Удалить аккаунт":
            delete_account(username)

def delete_account(username: str) -> None:
    db = utils.read_json(cnf.DB_FILE)

    if db[username]["role"] == "owner":
        print(cnf.RED + "[!] Вы как владелец не должны удалять себя!")
        print(cnf.RED + "[!] Однако, если вы очень этого хотите, то дело за вами...")

        confirm_owner_delete = questionary.confirm("Точно удалить аккаунт владельца?", default=False)
        confirm_answer = confirm_owner_delete.ask()

        if confirm_answer:
            for i in range(10, 0, -1):
                try:
                    print(f"Удаление вашего аккаунта через {i}... Для отмены: CTRL + C")

                    time.sleep(1)
                except KeyboardInterrupt:
                    print(cnf.BLUE + "[CANCELLED] Удаление аккаунта успешно отменено!")

                    return

            # Если все 10 секунд прошли (не было CTRL + C и следовательно выхода из функции), то удаляем аккаунт

            del db[username]
            utils.write_json(cnf.DB_FILE, db)
            sys.exit()

        return

    confirm_menu = questionary.confirm("[?] Удалить аккаунт? Это действие нельзя отменить! Это последнее предупреждение!")
    confirm_answer = confirm_menu.ask()

    if (confirm_answer is None) or (not(confirm_answer)): # Если CTRL + C или NO
        print(cnf.RED + "[!] Отмена")

        return
    
    del db[username]
    utils.write_json(cnf.DB_FILE, db)
    sys.exit()
