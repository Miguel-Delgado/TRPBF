"""Сущность «Матч»: объектная модель и создание таблицы в БД."""

import sqlite3

BYE_NAME = "None_name"


class Match:
    """Матч (пара участников) в рамках турнира."""

    TABLE_NAME = "matches"

    CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS matches (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            round         INTEGER NOT NULL DEFAULT 1,
            player1_id    INTEGER,
            player2_id    INTEGER,
            is_played     INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (tournament_id)
                REFERENCES tournaments (id) ON DELETE CASCADE,
            FOREIGN KEY (player1_id)
                REFERENCES participants (id) ON DELETE SET NULL,
            FOREIGN KEY (player2_id)
                REFERENCES participants (id) ON DELETE SET NULL
        )
    """

    CREATE_INDEX_SQL = """
        CREATE INDEX IF NOT EXISTS idx_matches_tournament
            ON matches (tournament_id, round)
    """

    def __init__(
        self,
        tournament_id: int,
        round_number: int = 1,
        player1_id: int | None = None,
        player2_id: int | None = None,
        is_played: bool = False,
        match_id: int | None = None,
        player1_name: str | None = None,
        player2_name: str | None = None,
    ) -> None:
        self.id = match_id
        self.tournament_id = tournament_id
        self.round_number = round_number
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.is_played = is_played
        self.player1_name = player1_name
        self.player2_name = player2_name

    @classmethod
    def create_table(cls, connection: sqlite3.Connection) -> None:
        """Создаёт таблицу матчей и её индексы."""
        connection.execute(cls.CREATE_TABLE_SQL)
        connection.execute(cls.CREATE_INDEX_SQL)

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Match":
        """Создаёт объект матча из строки результата запроса."""
        columns = row.keys()
        return cls(
            tournament_id=row["tournament_id"],
            round_number=row["round"],
            player1_id=row["player1_id"],
            player2_id=row["player2_id"],
            is_played=bool(row["is_played"]),
            match_id=row["id"],
            player1_name=(
                row["player1_name"] if "player1_name" in columns else None
            ),
            player2_name=(
                row["player2_name"] if "player2_name" in columns else None
            ),
        )

    @property
    def is_bye(self) -> bool:
        """Возвращает True, если одному из игроков не нашлось пары."""
        return self.player1_id is None or self.player2_id is None

    def winner_id(self) -> int | None:
        """Возвращает победителя прохода (bye) или None для матча."""
        if not self.is_bye:
            return None
        return self.player1_id or self.player2_id

    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return {
            "id": self.id,
            "tournament_id": self.tournament_id,
            "round": self.round_number,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "is_played": self.is_played,
        }

    def _player_label(self, name: str | None, player_id: int | None) -> str:
        if player_id is None:
            return BYE_NAME
        return name or f"id {player_id}"

    def __str__(self) -> str:
        first = self._player_label(self.player1_name, self.player1_id)
        second = self._player_label(self.player2_name, self.player2_id)
        status = "сыгран" if self.is_played else "не сыгран"
        identity = f"#{self.id}" if self.id is not None else "(новый)"
        return (
            f"Матч {identity} (тур {self.round_number}): "
            f"{first} vs {second} [{status}]"
        )

    def __repr__(self) -> str:
        return (
            f"Match(id={self.id!r}, tournament_id={self.tournament_id!r}, "
            f"player1_id={self.player1_id!r}, "
            f"player2_id={self.player2_id!r})"
        )
