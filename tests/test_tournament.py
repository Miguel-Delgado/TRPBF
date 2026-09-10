"""Автотесты логики турнира и модуля хранения данных."""

from tournament import (
    BYE_NAME,
    add_participant,
    draw_pairs,
    ensure_even_number,
    new_tournament,
)
from storage import load_tournament, save_tournament


def test_new_tournament_structure():
    """Проверяет создание структуры данных турнира."""
    tournament = new_tournament("Кубок города")
    assert tournament["name"] == "Кубок города"
    assert tournament["participants"] == []
    assert tournament["pairs"] == []


def test_new_tournament_empty_name():
    """Пустое название заменяется на 'Турнир без названия'."""
    tournament = new_tournament("   ")
    assert tournament["name"] == "Турнир без названия"


def test_add_participant_assigns_ids():
    """Проверяет, что участникам присваиваются последовательные id."""
    tournament = new_tournament("Тест")
    first = add_participant(tournament, "Иван")
    second = add_participant(tournament, "Петр")
    assert first == {"id": 1, "name": "Иван"}
    assert second == {"id": 2, "name": "Петр"}
    assert len(tournament["participants"]) == 2


def test_ensure_even_number_odd():
    """Нечётное количество -> добавляется виртуальный участник."""
    participants = [{"id": 1, "name": "A"},
                    {"id": 2, "name": "B"},
                    {"id": 3, "name": "C"}]
    updated, added = ensure_even_number(participants)
    assert len(updated) == 4
    assert added is True
    assert updated[-1]["name"] == BYE_NAME


def test_ensure_even_number_even():
    """Чётное количество -> ничего не добавляется."""
    participants = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
    updated, added = ensure_even_number(participants)
    assert len(updated) == 2
    assert added is False


def test_draw_pairs_count():
    """Проверяет, что количество пар равно половине участников."""
    participants = [{"id": i, "name": f"P{i}"} for i in range(1, 7)]
    pairs = draw_pairs(participants)
    assert len(pairs) == 3
    for pair in pairs:
        assert "player1" in pair and "player2" in pair


def test_draw_pairs_does_not_change_original():
    """Проверяет, что исходный список участников не изменяется."""
    participants = [{"id": 1, "name": "A"},
                    {"id": 2, "name": "B"},
                    {"id": 3, "name": "C"},
                    {"id": 4, "name": "D"}]
    snapshot = list(participants)
    draw_pairs(participants)
    assert participants == snapshot


def test_storage_roundtrip(tmp_path):
    """Проверяет сохранение и загрузку турнира в JSON."""
    tournament = new_tournament("Кубок города")
    add_participant(tournament, "Иван")
    add_participant(tournament, "Петр")
    tournament["pairs"] = [{"player1": "Иван", "player2": "Петр"}]
    filename = tmp_path / "tournament.json"

    assert save_tournament(tournament, str(filename)) is True
    loaded = load_tournament(str(filename))
    assert loaded == tournament


def test_load_tournament_missing_file(tmp_path):
    """Отсутствующий файл -> пустой шаблон турнира."""
    filename = tmp_path / "missing.json"
    loaded = load_tournament(str(filename))
    assert loaded == new_tournament()


def test_load_tournament_broken_file(tmp_path):
    """Повреждённый JSON -> пустой шаблон турнира."""
    filename = tmp_path / "broken.json"
    filename.write_text("{broken json", encoding="utf-8")
    loaded = load_tournament(str(filename))
    assert loaded == new_tournament()
