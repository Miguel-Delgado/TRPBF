"""Тесты сущности «Участник» и её репозитория."""

from models import Participant, Tournament
from repositories import ParticipantRepository, TournamentRepository


def _create_tournament(connection, name="Кубок"):
    return TournamentRepository(connection).add(Tournament(name))


def test_participant_attributes():
    participant = Participant("Иван", tournament_id=3)
    assert participant.id is None
    assert participant.name == "Иван"
    assert participant.tournament_id == 3


def test_participant_uses_default_name():
    assert Participant("   ", tournament_id=1).name == "Участник"


def test_participant_str_and_to_dict():
    participant = Participant("Иван", tournament_id=1, participant_id=5)
    assert str(participant) == "Участник #5: Иван"
    assert participant.to_dict() == {
        "id": 5,
        "name": "Иван",
        "tournament_id": 1,
    }


def test_create_table_creates_participants_table(connection):
    row = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name = 'participants'"
    ).fetchone()
    assert row is not None


def test_repository_add_and_get_by_id(connection):
    tournament = _create_tournament(connection)
    assert tournament.id is not None
    repository = ParticipantRepository(connection)
    stored = repository.add(Participant("Иван", tournament.id))
    assert stored.id is not None

    loaded = repository.get_by_id(stored.id)
    assert loaded is not None
    assert loaded.name == "Иван"
    assert loaded.tournament_id == tournament.id


def test_repository_get_by_tournament_and_count(connection):
    tournament = _create_tournament(connection)
    assert tournament.id is not None
    repository = ParticipantRepository(connection)
    repository.add(Participant("Иван", tournament.id))
    repository.add(Participant("Пётр", tournament.id))

    assert repository.count_by_tournament(tournament.id) == 2
    names = [item.name for item in
             repository.get_by_tournament(tournament.id)]
    assert names == ["Иван", "Пётр"]


def test_repository_delete_by_tournament(connection):
    tournament = _create_tournament(connection)
    assert tournament.id is not None
    repository = ParticipantRepository(connection)
    repository.add(Participant("Иван", tournament.id))

    repository.delete_by_tournament(tournament.id)
    assert repository.count_by_tournament(tournament.id) == 0


def test_tournament_delete_cascades_to_participants(connection):
    tournament = _create_tournament(connection)
    assert tournament.id is not None
    repository = ParticipantRepository(connection)
    repository.add(Participant("Иван", tournament.id))

    TournamentRepository(connection).delete(tournament.id)
    assert repository.count_by_tournament(tournament.id) == 0
