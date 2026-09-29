"""Тесты сущности «Турнир» и её репозитория."""

from models import STATUS_ACTIVE, STATUS_FINISHED, Tournament
from repositories import TournamentRepository


def test_tournament_defaults():
    tournament = Tournament("Кубок города")
    assert tournament.id is None
    assert tournament.name == "Кубок города"
    assert tournament.status == STATUS_ACTIVE
    assert tournament.created_at
    assert tournament.is_active() is True


def test_tournament_uses_default_name():
    assert Tournament("   ").name == "Турнир без названия"


def test_tournament_to_dict():
    data = Tournament("Кубок", tournament_id=7).to_dict()
    assert data == {
        "id": 7,
        "name": "Кубок",
        "status": STATUS_ACTIVE,
        "created_at": data["created_at"],
    }


def test_tournament_str():
    tournament = Tournament("Кубок", tournament_id=7)
    assert str(tournament) == "Турнир #7: Кубок [active]"


def test_create_table_creates_tournaments_table(connection):
    row = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name = 'tournaments'"
    ).fetchone()
    assert row is not None


def test_repository_add_and_get_by_id(connection):
    repository = TournamentRepository(connection)
    stored = repository.add(Tournament("Кубок"))
    assert stored.id is not None

    loaded = repository.get_by_id(stored.id)
    assert loaded is not None
    assert loaded.name == "Кубок"


def test_repository_get_missing_returns_none(connection):
    assert TournamentRepository(connection).get_by_id(999) is None


def test_repository_get_all(connection):
    repository = TournamentRepository(connection)
    repository.add(Tournament("Первый"))
    repository.add(Tournament("Второй"))
    names = [tournament.name for tournament in repository.get_all()]
    assert names == ["Первый", "Второй"]


def test_repository_update_status(connection):
    repository = TournamentRepository(connection)
    stored = repository.add(Tournament("Кубок"))
    assert stored.id is not None
    repository.update_status(stored.id, STATUS_FINISHED)

    loaded = repository.get_by_id(stored.id)
    assert loaded is not None
    assert loaded.status == STATUS_FINISHED
    assert loaded.is_active() is False


def test_repository_delete(connection):
    repository = TournamentRepository(connection)
    stored = repository.add(Tournament("Кубок"))
    assert stored.id is not None
    repository.delete(stored.id)
    assert repository.get_by_id(stored.id) is None
