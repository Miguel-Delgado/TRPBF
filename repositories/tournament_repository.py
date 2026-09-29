"""Хранение сущности «Турнир» в базе данных."""

import sqlite3

from models import Tournament


class TournamentRepository:
    """Репозиторий турниров: доступ к таблице tournaments."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, tournament: Tournament) -> Tournament:
        """Сохраняет турнир и возвращает его с присвоенным id."""
        cursor = self.connection.execute(
            """
            INSERT INTO tournaments (name, status, created_at)
            VALUES (?, ?, ?)
            """,
            (tournament.name, tournament.status, tournament.created_at),
        )
        self.connection.commit()
        tournament.id = cursor.lastrowid
        return tournament

    def get_by_id(self, tournament_id: int) -> Tournament | None:
        """Возвращает турнир по id или None, если его нет."""
        row = self.connection.execute(
            "SELECT * FROM tournaments WHERE id = ?",
            (tournament_id,),
        ).fetchone()
        return Tournament.from_row(row) if row is not None else None

    def get_all(self) -> list[Tournament]:
        """Возвращает все турниры, отсортированные по id."""
        rows = self.connection.execute(
            "SELECT * FROM tournaments ORDER BY id"
        ).fetchall()
        return [Tournament.from_row(row) for row in rows]

    def update_status(self, tournament_id: int, status: str) -> None:
        """Изменяет статус турнира."""
        self.connection.execute(
            "UPDATE tournaments SET status = ? WHERE id = ?",
            (status, tournament_id),
        )
        self.connection.commit()

    def delete(self, tournament_id: int) -> None:
        """Удаляет турнир вместе со связанными данными (ON DELETE CASCADE)."""
        self.connection.execute(
            "DELETE FROM tournaments WHERE id = ?",
            (tournament_id,),
        )
        self.connection.commit()
