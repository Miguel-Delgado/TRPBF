"""Сущность «Турнир»: объектная модель и создание таблицы в БД."""

import sqlite3
from datetime import datetime

STATUS_ACTIVE = "active"
STATUS_FINISHED = "finished"

DEFAULT_NAME = "Турнир без названия"


class Tournament:
    """Турнир, объединяющий участников, матчи и результаты."""

    TABLE_NAME = "tournaments"

    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS tournaments (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT    NOT NULL,
            status     TEXT    NOT NULL DEFAULT 'active',
            created_at TEXT    NOT NULL
        )
    """

    CREATE_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS idx_tournaments_status
            ON tournaments (status)
    """

    def __init__(
        self,
        name: str,
        tournament_id: int | None = None,
        status: str = STATUS_ACTIVE,
        created_at: str | None = None,
    ) -> None:
        self.id = tournament_id
        self.name = name.strip() or DEFAULT_NAME
        self.status = status
        self.created_at = created_at or datetime.now().isoformat(
            timespec="seconds"
        )

    @classmethod
    def create_table(cls, connection: sqlite3.Connection) -> None:
        """Создаёт таблицу турниров и её индексы, если их ещё нет."""
        connection.execute(cls.CREATE_TABLE_SQL)
        connection.execute(cls.CREATE_INDEX_SQL)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Tournament":
        """Создаёт объект турнира из строки результата запроса."""
        return cls(
            name=row["name"],
            tournament_id=row["id"],
            status=row["status"],
            created_at=row["created_at"],
        )

    def is_active(self) -> bool:
        """Возвращает True, если турнир ещё не завершён."""
        return self.status == STATUS_ACTIVE

    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        return f"Турнир #{self.id}: {self.name} [{self.status}]"

    def __repr__(self) -> str:
        return (
            f"Tournament(id={self.id!r}, name={self.name!r}, "
            f"status={self.status!r})"
        )
