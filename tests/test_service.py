"""Тесты бизнес-логики турнира (сервисный слой)."""

import pytest

from models import STATUS_FINISHED


def test_create_and_list_tournaments(service):
    service.create_tournament("Кубок")
    service.create_tournament("Лига")
    names = [tournament.name for tournament in service.list_tournaments()]
    assert names == ["Кубок", "Лига"]


def test_finish_tournament(service):
    tournament = service.create_tournament("Кубок")
    service.finish_tournament(tournament.id)

    loaded = service.get_tournament(tournament.id)
    assert loaded.status == STATUS_FINISHED


def test_add_participants(service):
    tournament = service.create_tournament("Кубок")
    service.add_participant(tournament.id, "Иван")
    service.add_participant(tournament.id, "Пётр")

    participants = service.list_participants(tournament.id)
    assert [item.name for item in participants] == ["Иван", "Пётр"]


def test_draw_requires_two_participants(service):
    tournament = service.create_tournament("Кубок")
    service.add_participant(tournament.id, "Иван")

    with pytest.raises(ValueError):
        service.draw_matches(tournament.id)


def test_draw_even_participants_has_no_bye(service):
    tournament = service.create_tournament("Кубок")
    for name in ("Иван", "Пётр", "Анна", "Мария"):
        service.add_participant(tournament.id, name)

    matches = service.draw_matches(tournament.id)
    assert len(matches) == 2
    assert all(match.is_bye is False for match in matches)


def test_draw_odd_participants_creates_bye(service):
    tournament = service.create_tournament("Кубок")
    for name in ("Иван", "Пётр", "Анна"):
        service.add_participant(tournament.id, name)

    matches = service.draw_matches(tournament.id)
    assert len(matches) == 2
    assert sum(1 for match in matches if match.is_bye) == 1


def test_record_result_marks_match_played(service):
    tournament = service.create_tournament("Кубок")
    service.add_participant(tournament.id, "Иван")
    service.add_participant(tournament.id, "Пётр")
    matches = service.draw_matches(tournament.id)

    result = service.record_result(matches[0], 1, "2:1")
    assert result.match_id == matches[0].id
    assert result.winner_id == matches[0].player1_id

    assert service.list_matches(tournament.id)[0].is_played is True


def test_record_bye_result_gives_technical_win(service):
    tournament = service.create_tournament("Кубок")
    for name in ("Иван", "Пётр", "Анна"):
        service.add_participant(tournament.id, name)
    matches = service.draw_matches(tournament.id)
    bye_match = next(match for match in matches if match.is_bye)

    result = service.record_result(bye_match, winner_side=2, score="bye")
    assert result.winner_id == bye_match.winner_id()


def test_standings_counts_wins(service):
    tournament = service.create_tournament("Кубок")
    service.add_participant(tournament.id, "Иван")
    service.add_participant(tournament.id, "Пётр")
    matches = service.draw_matches(tournament.id)

    service.record_result(matches[0], 1, "2:1")
    standings = service.standings(tournament.id)

    assert len(standings) == 2
    assert standings[0][1] == 1
    assert standings[1][1] == 0


def test_standings_without_participants(service):
    tournament = service.create_tournament("Кубок")
    assert service.standings(tournament.id) == []


def test_new_draw_clears_previous_matches_and_results(service):
    tournament = service.create_tournament("Кубок")
    for name in ("Иван", "Пётр", "Анна", "Мария"):
        service.add_participant(tournament.id, name)

    matches = service.draw_matches(tournament.id)
    service.record_result(matches[0], 1, "2:1")
    assert len(service.list_results(tournament.id)) == 1

    service.draw_matches(tournament.id)
    assert len(service.list_matches(tournament.id)) == 2
    assert service.list_results(tournament.id) == []
