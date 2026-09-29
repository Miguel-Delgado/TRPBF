"""Тесты сущности «Результат» и её репозитория."""

import sqlite3

import pytest

from models import Match, Participant, Result, Tournament
from repositories import (
    MatchRepository,
    ParticipantRepository,
    ResultRepository,
    TournamentRepository,
)


def _create_match(connection):
    tournament = TournamentRepository(connection).add(Tournament("Кубок"))
    assert tournament.id is not None
    participants = ParticipantRepository(connection)
    first = participants.add(Participant("Иван", tournament.id))
    second = participants.add(Participant("Пётр", tournament.id))
    match = MatchRepository(connection).add(
        Match(tournament.id, player1_id=first.id, player2_id=second.id)
    )
    return tournament, first, second, match


def test_result_attributes():
    result = Result(match_id=1, winner_id=2, score="2:1")
    assert result.id is None
    assert result.match_id == 1
    assert result.winner_id == 2
    assert result.score == "2:1"
    assert result.created_at


def test_result_str_with_winner_name():
    result = Result(match_id=4, winner_id=2, score="2:1",
                    winner_name="Иван")
    assert str(result) == (
        "Результат матча #4: победитель Иван, счёт 2:1"
    )


def test_result_str_without_winner():
    result = Result(match_id=4, winner_id=None)
    assert str(result) == (
        "Результат матча #4: победитель не определён"
    )


def test_create_table_creates_results_table(connection):
    row = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name = 'results'"
    ).fetchone()
    assert row is not None


def test_repository_add_and_get_by_match(connection):
    tournament, first, second, match = _create_match(connection)
    assert match.id is not None
    repository = ResultRepository(connection)
    stored = repository.add(Result(match.id, first.id, "2:1"))

    assert stored.id is not None
    assert stored.winner_name == "Иван"

    loaded = repository.get_by_match(match.id)
    assert loaded is not None
    assert loaded.score == "2:1"
    assert loaded.winner_id == first.id


def test_repository_get_by_tournament(connection):
    tournament, first, second, match = _create_match(connection)
    assert match.id is not None
    assert tournament.id is not None
    repository = ResultRepository(connection)
    repository.add(Result(match.id, first.id, "2:1"))

    results = repository.get_by_tournament(tournament.id)
    assert len(results) == 1
    assert results[0].winner_name == "Иван"


def test_repository_delete_by_tournament(connection):
    tournament, first, second, match = _create_match(connection)
    assert match.id is not None
    assert tournament.id is not None
    repository = ResultRepository(connection)
    repository.add(Result(match.id, first.id, "2:1"))

    repository.delete_by_tournament(tournament.id)
    assert repository.get_by_tournament(tournament.id) == []


def test_result_is_unique_for_match(connection):
    tournament, first, second, match = _create_match(connection)
    assert match.id is not None
    repository = ResultRepository(connection)
    repository.add(Result(match.id, first.id, "2:1"))

    with pytest.raises(sqlite3.IntegrityError):
        repository.add(Result(match.id, second.id, "1:2"))
