"""Точка входа: консольное меню системы организации турниров."""

from tournament import (
    BYE_NAME,
    add_participant,
    draw_pairs,
    ensure_even_number,
    new_tournament,
)
from storage import DEFAULT_DATA_FILE, load_tournament, save_tournament
from utils import input_int, input_name

MENU = """
=============== МЕНЮ ===============
1 - Создать новый турнир
2 - Добавить участников
3 - Показать список участников
4 - Жеребьёвка (сформировать пары)
5 - Показать пары
6 - Сохранить турнир в JSON
7 - Загрузить турнир из JSON
0 - Выход
====================================
"""


def create_tournament() -> dict:
    """
    Запрашивает название турнира и возвращает его структуру.

    Создание выполняет функция new_tournament() из модуля tournament.
    """
    print("\n--- Создание турнира ---")
    name = input_name("Введите название турнира: ")
    tournament = new_tournament(name)
    print(f"Турнир '{tournament['name']}' создан. "
          "Добавьте участников (пункт 2).")
    return tournament


def add_participants(tournament: dict) -> None:
    """
    Запрашивает количество и имена участников и добавляет их в турнир.

    Количество запрашивается через input_int() из модуля utils,
    добавление — через add_participant() из модуля tournament.
    """
    print("\n--- Добавление участников ---")
    count = input_int("Введите количество участников (целое число > 0): ")
    for i in range(1, count + 1):
        name = input_name(f"Введите имя участника #{i}: ", f"Участник {i}")
        participant = add_participant(tournament, name)
        print(f"  Добавлен: {participant['name']} (id: {participant['id']})")


def show_participants(tournament: dict) -> None:
    """Показывает нумерованный список участников турнира."""
    print("\nСписок участников:")
    if not tournament["participants"]:
        print("  (пока пусто)")
        return
    for i, participant in enumerate(tournament["participants"], 1):
        print(f"  {i}. {participant['name']} (id: {participant['id']})")


def display_pairs(tournament_name: str, pairs: list[dict]) -> None:
    """Выводит пары на экран с учётом прохода при 'None_name'."""
    if not pairs:
        print("Пары ещё не сформированы. Выполните жеребьёвку (пункт 4).")
        return
    print("\n" + "=" * 50)
    print(f"Пары первого тура турнира '{tournament_name}':")
    for idx, pair in enumerate(pairs, start=1):
        p1, p2 = pair["player1"], pair["player2"]
        if p1 == BYE_NAME:
            print(f"  Пара #{idx}: {p1} vs {p2} -> {p2} "
                  "проходит автоматически.")
        elif p2 == BYE_NAME:
            print(f"  Пара #{idx}: {p1} vs {p2} -> {p1} "
                  "проходит автоматически.")
        else:
            print(f"  Пара #{idx}: {p1} vs {p2}")
    print("=" * 50)


def run_draw(tournament: dict) -> None:
    """Выполняет жеребьёвку: проверяет чётность, формирует пары."""
    print("\n--- Жеребьёвка ---")
    participants = [p for p in tournament["participants"]
                    if p["name"] != BYE_NAME]
    participants, was_added = ensure_even_number(participants)
    if was_added:
        print("Количество участников нечётное. "
              "Добавлен виртуальный участник 'None_name'.")
    tournament["participants"] = participants
    tournament["pairs"] = draw_pairs(participants)
    display_pairs(tournament["name"], tournament["pairs"])


def load_from_file() -> dict:
    """Загружает турнир из JSON и выводит краткую информацию."""
    tournament = load_tournament()
    name = tournament["name"]
    count = len(tournament["participants"])
    print(f"Загружен турнир '{name}' ({count} участников).")
    return tournament


def main() -> None:
    """Главный цикл консольного меню приложения."""
    print("=" * 50)
    print("   Добро пожаловать в систему организации турниров!")
    print("=" * 50)

    # При старте пытаемся загрузить данные из файла по умолчанию
    tournament = load_from_file()

    while True:
        print(MENU)
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            tournament = create_tournament()
        elif choice == "2":
            add_participants(tournament)
        elif choice == "3":
            show_participants(tournament)
        elif choice == "4":
            run_draw(tournament)
        elif choice == "5":
            display_pairs(tournament["name"], tournament["pairs"])
        elif choice == "6":
            if save_tournament(tournament):
                print(f"Турнир сохранён в файл: {DEFAULT_DATA_FILE}")
        elif choice == "7":
            tournament = load_from_file()
        elif choice == "0":
            print("Спасибо за использование! До встречи.")
            break
        else:
            print("Ошибка: неизвестный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()
