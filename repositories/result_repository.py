"""Хранение сущности «Результат» в базе данных."""

import sqlite3

from models import Result


class ResultRepository:
    """Репозиторий результатов: доступ к таблице results."""

    SELECT_WITH_NAMES = """
        SELECT r.id,
               r.match_id,
               r.winner_id,
               r.score,
               r.created_at,
               p.name AS winner_name
        FROM results AS r
        LEFT JOIN participants AS p ON p.id = r.winner_id
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, result: Result) -> Result:
        """Сохраняет результат и возвращает его с присвоенным id."""
        cursor = self.connection.execute(
            """
            INSERT INTO results (match_id, winner_id, score, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                result.match_id,
                result.winner_id,
                result.score,
                result.created_at,
            ),
        )
        self.connection.commit()
        result.id = cursor.lastrowid
        stored = self.get_by_match(result.match_id)
        return stored if stored is not None else result

    def get_by_match(self, match_id: int) -> Result | None:
        """Возвращает результат матча вместе с именем победителя."""
        row = self.connection.execute(
            f"{self.SELECT_WITH_NAMES} WHERE r.match_id = ?",
            (match_id,),
        ).fetchone()
        return Result.from_row(row) if row is not None else None

    def get_by_tournament(self, tournament_id: int) -> list[Result]:
        """Возвращает результаты всех матчей турнира."""
        rows = self.connection.execute(
            f"""
            {self.SELECT_WITH_NAMES}
            WHERE r.match_id IN (
                SELECT id FROM matches WHERE tournament_id = ?
            )
            ORDER BY r.id
            """,
            (tournament_id,),
        ).fetchall()
        return [Result.from_row(row) for row in rows]

    def delete_by_tournament(self, tournament_id: int) -> None:
        """Удаляет результаты всех матчей турнира."""
        self.connection.execute(
            """
            DELETE FROM results
            WHERE match_id IN (
                SELECT id FROM matches WHERE tournament_id = ?
            )
            """,
            (tournament_id,),
        )
        self.connection.commit()
