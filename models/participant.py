"""Сущность «Участник»: объектная модель и создание таблицы в БД."""

import sqlite3

DEFAULT_NAME = "Участник"


class Participant:
    """Участник турнира."""

    TABLE_NAME = "participants"

    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS participants (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            name          TEXT    NOT NULL,
            FOREIGN KEY (tournament_id)
                REFERENCES tournaments (id) ON DELETE CASCADE
        )
    """

    CREATE_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS idx_participants_tournament
            ON participants (tournament_id)
    """

    def __init__(
        self,
        name: str,
        tournament_id: int,
        participant_id: int | None = None,
    ) -> None:
        self.id = participant_id
        self.name = name.strip() or DEFAULT_NAME
        self.tournament_id = tournament_id

    @classmethod
    def create_table(cls, connection: sqlite3.Connection) -> None:
        """Создаёт таблицу участников и её индексы."""
        connection.execute(cls.CREATE_TABLE_SQL)
        connection.execute(cls.CREATE_INDEX_SQL)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Participant":
        """Создаёт объект участника из строки результата запроса."""
        return cls(
            name=row["name"],
            tournament_id=row["tournament_id"],
            participant_id=row["id"],
        )

    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "tournament_id": self.tournament_id,
        }

    def __str__(self) -> str:
        return f"Участник #{self.id}: {self.name}"

    def __repr__(self) -> str:
        return (
            f"Participant(id={self.id!r}, name={self.name!r}, "
            f"tournament_id={self.tournament_id!r})"
        )
