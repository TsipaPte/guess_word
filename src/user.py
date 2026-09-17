import secrets
import sys

import prompt_toolkit as ptk
import questionary

import config as cnf
import utils
import settings

with open(cnf.WORDS_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()
    words = []

    for i in lines:
        words.append(i.rstrip())

def menu(username: str, return_instead_exit: bool=False) -> None:
    while True:
        user_menu = questionary.select("[USER] Выберите:", cnf.USER_MENU, use_shortcuts=True)
        user_choice = user_menu.ask()

        if user_choice == "Просмотреть свой профиль":
            utils.check_profile(username)
        elif user_choice == "Играть":
            start_game(username)
        elif user_choice == cnf.EXIT_OPTION:
            if return_instead_exit:
                return
            else:
                sys.exit()
        elif user_choice == "Настройки":
            settings.menu(username)

def start_game(username: str) -> None:
    guessed_word = secrets.choice(words).lower()
    TOTAL_ATTEMPTS = len(guessed_word)

    hints = ["_"] * len(guessed_word)
    used_letters = []
    attempts = 1
    is_user_win = False

    while True:
        if attempts > TOTAL_ATTEMPTS:
            break

        print(" ".join(hints))

        while True:
            if used_letters:
                print(f"[Использованные буквы]: {" ".join(used_letters)}")
            else:
                print("[Использованные буквы]: нет")

            try:
                user_letter = input(f"[Попытка {attempts}/{TOTAL_ATTEMPTS}] Введите букву: ")
            except KeyboardInterrupt:
                user_lose(username)
                return

            if len(user_letter) != 1:
                print(cnf.RED + "[!] Это не одна буква!")
                continue
            elif user_letter not in cnf.RUSSIAN_LETTERS:
                print(cnf.RED + "[!] Это не русская буква!")
                continue
            elif user_letter in used_letters:
                print(cnf.RED + "[!] Уже была!")
                continue

            break

        used_letters.append(user_letter)

        if user_letter in guessed_word:
            print(cnf.GREEN + "[GOOD] Буква есть в данном слове! Попытка не отнимается!")

            # Если буква есть в слове, то раскрываем её!
            for index, correct_letter in enumerate(guessed_word):
                if correct_letter == user_letter:
                    hints[index] = user_letter

            if "".join(hints) == guessed_word:
                is_user_win = True
                break
        else:
            print(cnf.RED + "[BAD] Буквы нет в данном слове! Попытка отнимается!")

            attempts += 1

    if is_user_win:
        user_win(username)
    else:
        user_lose(username)

def user_win(username: str) -> None:
    db = utils.read_json(cnf.DB_FILE)
    current_rank_id = db[username]["rank"]
    rank_info = cnf.RANK_DB[current_rank_id]
    give_win = rank_info["win"]
    is_rank_up = False

    db[username]["current_elo"] += give_win
    elo_after_update = db[username]["current_elo"]

    if current_rank_id < cnf.MAX_RANK:
        # Если у пользователя не самый максимальный ранг, то возможно он повысился!
        
        possible_next_rank_id = current_rank_id + 1
        possible_next_rank_info = cnf.RANK_DB[possible_next_rank_id]
        possible_next_rank_needs_elo = possible_next_rank_info["needs_elo"]

        if possible_next_rank_needs_elo <= db[username]["current_elo"]:
            db[username]["rank"] = possible_next_rank_id

            is_rank_up = True

        win_dialog = ptk.shortcuts.message_dialog("Победа!", f"Поздравляем с победой!\nВам добавили рейтинга: +{give_win}\nРейтинга: {elo_after_update}/{possible_next_rank_needs_elo}", style=cnf.GREEN_PTK_STYLE)
        win_dialog.run()
    else:
        win_dialog = ptk.shortcuts.message_dialog("Победа!", f"Поздравляем с победой!\nВам добавили рейтинга: +{give_win}\nРейтинга: {elo_after_update}", style=cnf.GREEN_PTK_STYLE)
        win_dialog.run()

    if is_rank_up:
        name = possible_next_rank_info["name"]

        rank_up_dialog = ptk.shortcuts.message_dialog("С повышением!", f"Поздравляем Вас с повышением! Теперь вы официально находитесь на одной ступеньке выше: ранг \"{name}\"")

        rank_up_dialog.run()

    utils.write_json(cnf.DB_FILE, db)

def user_lose(username: str) -> None:
    db = utils.read_json(cnf.DB_FILE)
    current_rank_id = db[username]["rank"]
    current_rank_info = cnf.RANK_DB[current_rank_id]

    needs_to_delete_elo = current_rank_info["lose"]
    old_elo = db[username]["current_elo"]
    new_elo = old_elo - needs_to_delete_elo

    if new_elo < 0:
        new_elo = 0

    db[username]["current_elo"] = new_elo

    if current_rank_id > cnf.MIN_RANK:
        # Если у пользователя не минимальный ранг, то возможно он упал на ступень ниже

        possible_lower_rank_id = current_rank_id - 1

        if new_elo < current_rank_info["needs_elo"]:
            db[username]["rank"] = possible_lower_rank_id

    lose_dialog = ptk.shortcuts.message_dialog("Вы проиграли!", f"К сожалению, вы проиграли!\nСписано: -{needs_to_delete_elo}\nРейтинга: {new_elo}", style=cnf.RED_PTK_STYLE)
    lose_dialog.run()

    utils.write_json(cnf.DB_FILE, db)
