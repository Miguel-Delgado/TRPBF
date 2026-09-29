"""Хранение сущности «Участник» в базе данных."""

import sqlite3

from models import Participant


class ParticipantRepository:
    """Репозиторий участников: доступ к таблице participants."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, participant: Participant) -> Participant:
        """Сохраняет участника и возвращает его с присвоенным id."""
        cursor = self.connection.execute(
            """
            INSERT INTO participants (tournament_id, name)
            VALUES (?, ?)
            """,
            (participant.tournament_id, participant.name),
        )
        self.connection.commit()
        participant.id = cursor.lastrowid
        return participant

    def get_by_id(self, participant_id: int) -> Participant | None:
        """Возвращает участника по id или None, если его нет."""
        row = self.connection.execute(
            "SELECT * FROM participants WHERE id = ?",
            (participant_id,),
        ).fetchone()
        return Participant.from_row(row) if row is not None else None

    def get_by_tournament(self, tournament_id: int) -> list[Participant]:
        """Возвращает участников указанного турнира."""
        rows = self.connection.execute(
            """
            SELECT * FROM participants
            WHERE tournament_id = ?
            ORDER BY id
            """,
            (tournament_id,),
        ).fetchall()
        return [Participant.from_row(row) for row in rows]

    def count_by_tournament(self, tournament_id: int) -> int:
        """Возвращает количество участников турнира."""
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS total FROM participants
            WHERE tournament_id = ?
            """,
            (tournament_id,),
        ).fetchone()
        return int(row["total"])

    def delete_by_tournament(self, tournament_id: int) -> None:
        """Удаляет всех участников турнира."""
        self.connection.execute(
            "DELETE FROM participants WHERE tournament_id = ?",
            (tournament_id,),
        )
        self.connection.commit()
