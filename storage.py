"""Сохранение и загрузка данных турнира в формате JSON."""

import json
import os

from tournament import new_tournament

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_FILE = os.path.join(BASE_DIR, "data", "tournament.json")


def save_tournament(data: dict, filename: str = DEFAULT_DATA_FILE) -> bool:
    """
    Сохраняет словарь турнира в JSON-файл.

    При необходимости создаёт каталог data/. Возвращает True
    при успехе и False, если сохранить файл не удалось.
    """
    try:
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except OSError as e:
        print(f"Ошибка сохранения: {e}")
        return False


def load_tournament(filename: str = DEFAULT_DATA_FILE) -> dict:
    """
    Загружает турнир из JSON-файла.

    Если файла нет или его данные повреждены, возвращает пустой
    шаблон турнира. Отсутствующие ключи дополняются значениями
    по умолчанию.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Файл данных не найден. Будет создан новый турнир.")
        return new_tournament()
    except json.JSONDecodeError:
        print("Ошибка чтения файла. Данные повреждены.")
        return new_tournament()

    if not isinstance(data, dict):
        print("Некорректный формат данных. Будет создан новый турнир.")
        return new_tournament()

    data.setdefault("name", "Турнир без названия")
    data.setdefault("participants", [])
    data.setdefault("pairs", [])
    return data
