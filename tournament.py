"""Логика турнира: структура данных, участники, жеребьёвка."""

import random

BYE_NAME = "None_name"


def new_tournament(name: str = "") -> dict:
    """
    Создаёт и возвращает шаблон турнира.

    Шаблон содержит название, пустой список участников
    и пустой список пар. Пустое название заменяется
    на "Турнир без названия".
    """
    return {
        "name": name.strip() or "Турнир без названия",
        "participants": [],
        "pairs": [],
    }


def next_participant_id(participants: list[dict]) -> int:
    """
    Возвращает следующий свободный id участника.

    id вычисляется как максимум существующих id + 1,
    для пустого списка возвращается 1.
    """
    if not participants:
        return 1
    return max(p.get("id", 0) for p in participants) + 1


def add_participant(tournament: dict, name: str) -> dict:
    """
    Добавляет участника в турнир.

    Создаёт словарь {"id": ..., "name": ...}, присваивает следующий
    свободный id, добавляет в tournament["participants"]
    и возвращает созданного участника.
    """
    participant = {
        "id": next_participant_id(tournament["participants"]),
        "name": name.strip()
        or f"Участник {len(tournament['participants']) + 1}",
    }
    tournament["participants"].append(participant)
    return participant


def ensure_even_number(participants: list[dict]) -> tuple[list[dict], bool]:
    """
    Проверяет чётность количества участников.

    Если участников нечётное количество, добавляет виртуального
    участника "None_name" (соперник проходит автоматически).
    Возвращает кортеж (список участников, добавлен_ли_виртуальный).
    """
    if len(participants) % 2 != 0:
        bye = {"id": next_participant_id(participants), "name": BYE_NAME}
        participants.append(bye)
        return participants, True
    return participants, False


def draw_pairs(participants: list[dict]) -> list[dict]:
    """
    Перемешивает участников и разбивает их на пары.

    Оригинальный список не изменяется. Возвращает список словарей
    вида {"player1": имя, "player2": имя}.
    """
    shuffled = participants[:]  # копируем, чтобы не изменять оригинал
    random.shuffle(shuffled)
    pairs = []
    for i in range(0, len(shuffled) - 1, 2):
        pairs.append({
            "player1": shuffled[i]["name"],
            "player2": shuffled[i + 1]["name"],
        })
    return pairs
