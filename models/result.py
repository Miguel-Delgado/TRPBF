"""Сущность «Результат»: объектная модель и создание таблицы в БД."""

import sqlite3
from datetime import datetime


class Result:
    """Результат сыгранного матча."""

    TABLE_NAME = "results"

    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS results (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id   INTEGER NOT NULL UNIQUE,
            winner_id  INTEGER,
            score      TEXT    NOT NULL DEFAULT '',
            created_at TEXT    NOT NULL,
            FOREIGN KEY (match_id)
                REFERENCES matches (id) ON DELETE CASCADE,
            FOREIGN KEY (winner_id)
                REFERENCES participants (id) ON DELETE SET NULL
        )
    """

    CREATE_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS idx_results_winner
            ON results (winner_id)
    """

    def __init__(
        self,
        match_id: int,
        winner_id: int | None = None,
        score: str = "",
        result_id: int | None = None,
        created_at: str | None = None,
        winner_name: str | None = None,
    ) -> None:
        self.id = result_id
        self.match_id = match_id
        self.winner_id = winner_id
        self.score = score
        self.created_at = created_at or datetime.now().isoformat(
            timespec="seconds"
        )
        self.winner_name = winner_name

    @classmethod
    def create_table(cls, connection: sqlite3.Connection) -> None:
        """Создаёт таблицу результатов и её индексы."""
        connection.execute(cls.CREATE_TABLE_SQL)
        connection.execute(cls.CREATE_INDEX_SQL)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Result":
        """Создаёт объект результата из строки результата запроса."""
        columns = row.keys()
        winner_name = (
            row["winner_name"] if "winner_name" in columns else None
        )
        return cls(
            match_id=row["match_id"],
            winner_id=row["winner_id"],
            score=row["score"],
            result_id=row["id"],
            created_at=row["created_at"],
            winner_name=winner_name,
        )

    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return {
            "id": self.id,
            "match_id": self.match_id,
            "winner_id": self.winner_id,
            "score": self.score,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        if self.winner_name:
            winner = self.winner_name
        elif self.winner_id is not None:
            winner = f"id {self.winner_id}"
        else:
            winner = "не определён"
        score = f", счёт {self.score}" if self.score else ""
        return f"Результат матча #{self.match_id}: победитель {winner}{score}"

    def __repr__(self) -> str:
        return (
            f"Result(id={self.id!r}, match_id={self.match_id!r}, "
            f"winner_id={self.winner_id!r})"
        )
