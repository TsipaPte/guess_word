import colorama
from prompt_toolkit.styles import Style

colorama.init(autoreset=True)

# Цвета
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA
BLUE = colorama.Fore.BLUE

# Если по какой-то причине autoreset=True не сработал!
RESET = colorama.Fore.RESET

# Файлы
DB_FILE = "../data/db.json"
WORDS_FILE = "../data/words.txt"

# Меню и прочие переменные, связанные с ним
EXIT_OPTION = "Выход"
CANCEL_OPTION = "Отмена"

MAIN_MENU_OPTIONS = ("Вход", "Регистрация", EXIT_OPTION)
OWNER_MENU = ("Заблокировать пользователя", "Разблокировать пользователя", "Создать учётную запись", "Удалить учётную запись", "Просмотреть профиль пользователя", "Настройки", "В режим пользователя", EXIT_OPTION)
ADMIN_MENU = ("Заблокировать пользователя", "Разблокировать пользователя", "Настройки", "В режим пользователя", EXIT_OPTION)
USER_MENU = ("Играть", "Просмотреть свой профиль", "Настройки", EXIT_OPTION)
SETTINGS_MENU = ("Удалить аккаунт", EXIT_OPTION)

# Роли и пользователи
ROLES = {"Пользователь": "user", "Администратор": "admin", "Владелец": "owner"}
BANNED_USERNAMES = (EXIT_OPTION, CANCEL_OPTION)
DONT_SHOW_THIS_ON_CHECK_PROFILE = ("ban_status", "ban_admin", "ban_time", "ban_reason")

# Ранги
RANK_DB = {1: {"name": "Деревянный", "color": None, "needs_elo": 0, "win": 400, "lose": 0},
           2: {"name": "Бронзовый", "color": None, "needs_elo": 1000, "win": 300, "lose": 30},
           3: {"name": "Серебряный", "color": None, "needs_elo": 2000, "win": 250, "lose": 50},
           4: {"name": "Золотой", "color": YELLOW, "needs_elo": 3000, "win": 225, "lose": 75},
           5: {"name": "Алмазный", "color": BLUE, "needs_elo": 4000, "win": 200, "lose": 80},
           6: {"name": "Обсидиановый", "color": MAGENTA, "needs_elo": 5000, "win": 150, "lose": 90},
           7: {"name": "Легендарный", "color": RED, "needs_elo": 6000, "win": 125, "lose": 95},
           8: {"name": "Профессиональный", "color": GREEN, "needs_elo": 7000, "win": 100, "lose": 100},
           9: {"name": "Бесконечный", "color": None, "needs_elo": 8000, "win": 75, "lose": 100}
           }

MAX_RANK = max(RANK_DB.keys())
MAX_RANK_BASE_ELO = RANK_DB[MAX_RANK]["needs_elo"]

MIN_RANK = min(RANK_DB.keys())

# Декодеры
DB_DECODES = {
    "password": "Пароль",
    "rank": "Ранг",
    "role": "Роль",
    "current_elo": "Рейтинг",
    "ban_status": "Статус блокировки",
    "ban_admin": "Администратор который заблокировал",
    "ban_time": "Время блокировки",
    "ban_reason": "Причина блокировки"
}

# prompt_toolkit стили
GREEN_PTK_STYLE = Style([("dialog", "bg:#75B44C")])
RED_PTK_STYLE = Style([("dialog", "bg:#B44C4C")])

# Прочее
DB_TYPE_IS_NOT_DICT_ERROR = "[CRITICAL] Невозможно корректно загрузить БД (код ошибки: DB_TYPE_IS_NOT_DICT)"
BANNED_USERNAME_ERROR = "[!] Имя пользователя невозможно использовать по техническим причинам!"
RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
