"""Хранение сущности «Матч» в базе данных."""

import sqlite3

from models import Match


class MatchRepository:
    """Репозиторий матчей: доступ к таблице matches."""

    SELECT_WITH_NAMES = """
        SELECT m.id,
               m.tournament_id,
               m.round,
               m.player1_id,
               m.player2_id,
               m.is_played,
               p1.name AS player1_name,
               p2.name AS player2_name
        FROM matches AS m
        LEFT JOIN participants AS p1 ON p1.id = m.player1_id
        LEFT JOIN participants AS p2 ON p2.id = m.player2_id
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, match: Match) -> Match:
        """Сохраняет матч и возвращает его с присвоенным id."""
        cursor = self.connection.execute(
            """
            INSERT INTO matches
                (tournament_id, round, player1_id, player2_id, is_played)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                match.tournament_id,
                match.round_number,
                match.player1_id,
                match.player2_id,
                int(match.is_played),
            ),
        )
        self.connection.commit()
        match_id = cursor.lastrowid
        match.id = match_id
        if match_id is None:
            return match
        stored = self.get_by_id(match_id)
        return stored if stored is not None else match

    def get_by_id(self, match_id: int) -> Match | None:
        """Возвращает матч по id вместе с именами игроков."""
        row = self.connection.execute(
            f"{self.SELECT_WITH_NAMES} WHERE m.id = ?",
            (match_id,),
        ).fetchone()
        return Match.from_row(row) if row is not None else None

    def get_by_tournament(self, tournament_id: int) -> list[Match]:
        """Возвращает матчи турнира вместе с именами игроков."""
        rows = self.connection.execute(
            f"{self.SELECT_WITH_NAMES} "
            "WHERE m.tournament_id = ? ORDER BY m.id",
            (tournament_id,),
        ).fetchall()
        return [Match.from_row(row) for row in rows]

    def set_played(self, match_id: int, is_played: bool = True) -> None:
        """Отмечает матч как сыгранный или несыгранный."""
        self.connection.execute(
            "UPDATE matches SET is_played = ? WHERE id = ?",
            (int(is_played), match_id),
        )
        self.connection.commit()

    def delete_by_tournament(self, tournament_id: int) -> None:
        """Удаляет все матчи турнира."""
        self.connection.execute(
            "DELETE FROM matches WHERE tournament_id = ?",
            (tournament_id,),
        )
        self.connection.commit()
