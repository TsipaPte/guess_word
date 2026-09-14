import sys

import questionary

import auth
import config as cnf

def main() -> None:
    menu = questionary.select("[Главное меню] Выберите:", cnf.MAIN_MENU_OPTIONS, use_shortcuts=True)
    choice = menu.ask()

    if choice == cnf.EXIT_OPTION:
        sys.exit()
    elif choice == "Вход":
        # Функция auth.login() при успешной (!!) авторизации возвращает кортеж вида (имя пользователя, роль)
        # Если пароль введён неправильно или авторизация провалена другим образом, программа просто завершится ещё на этапе auth.login()

        username, role = auth.login()

        # Если мы до сюда дошли, то значит, авторизацию уже прошли успешно!
        auth.grant_access(username, role)
    elif choice == "Регистрация":
        auth.register()

if __name__ == "__main__":
    main()
