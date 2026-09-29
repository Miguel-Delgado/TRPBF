"""Тесты сущности «Матч» и её репозитория."""

from models import BYE_NAME, Match, Participant, Tournament
from repositories import (
    MatchRepository,
    ParticipantRepository,
    TournamentRepository,
)


def _create_match(connection):
    tournament = TournamentRepository(connection).add(Tournament("Кубок"))
    assert tournament.id is not None
    participants = ParticipantRepository(connection)
    first = participants.add(Participant("Иван", tournament.id))
    second = participants.add(Participant("Пётр", tournament.id))
    match = Match(tournament.id, player1_id=first.id, player2_id=second.id)
    return tournament, first, second, match


def test_match_attributes():
    match = Match(tournament_id=1, player1_id=10, player2_id=20)
    assert match.id is None
    assert match.round_number == 1
    assert match.is_played is False
    assert match.is_bye is False


def test_match_is_bye_and_winner_id():
    bye = Match(tournament_id=1, player1_id=10, player2_id=None)
    assert bye.is_bye is True
    assert bye.winner_id() == 10

    regular = Match(tournament_id=1, player1_id=10, player2_id=20)
    assert regular.is_bye is False
    assert regular.winner_id() is None


def test_match_str_shows_names_and_bye():
    match = Match(
        tournament_id=1,
        player1_id=10,
        player2_id=None,
        match_id=3,
        player1_name="Иван",
    )
    assert str(match) == (
        f"Матч #3 (тур 1): Иван vs {BYE_NAME} [не сыгран]"
    )


def test_create_table_creates_matches_table(connection):
    row = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name = 'matches'"
    ).fetchone()
    assert row is not None


def test_repository_add_returns_match_with_names(connection):
    tournament, first, second, match = _create_match(connection)
    stored = MatchRepository(connection).add(match)

    assert stored.id is not None
    assert stored.player1_name == "Иван"
    assert stored.player2_name == "Пётр"


def test_repository_get_by_tournament(connection):
    tournament, first, second, match = _create_match(connection)
    assert tournament.id is not None
    repository = MatchRepository(connection)
    repository.add(match)

    matches = repository.get_by_tournament(tournament.id)
    assert len(matches) == 1
    assert matches[0].player1_id == first.id
    assert matches[0].player2_id == second.id


def test_repository_set_played(connection):
    tournament, first, second, match = _create_match(connection)
    repository = MatchRepository(connection)
    stored = repository.add(match)
    assert stored.id is not None

    repository.set_played(stored.id, True)
    loaded = repository.get_by_id(stored.id)
    assert loaded is not None
    assert loaded.is_played is True


def test_repository_delete_by_tournament(connection):
    tournament, first, second, match = _create_match(connection)
    assert tournament.id is not None
    repository = MatchRepository(connection)
    repository.add(match)

    repository.delete_by_tournament(tournament.id)
    assert repository.get_by_tournament(tournament.id) == []
