"""Подключение к базе данных SQLite и инициализация схемы."""

import sqlite3
from pathlib import Path

from models import Match, Participant, Result, Tournament

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DB_FILE = DATA_DIR / "tournament.db"

MEMORY_DB = ":memory:"


def get_connection(
    db_path: str | Path = DEFAULT_DB_FILE,
) -> sqlite3.Connection:
    """Открывает соединение с базой данных SQLite."""
    path = Path(db_path)
    if str(path) != MEMORY_DB:
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: str | Path = DEFAULT_DB_FILE) -> sqlite3.Connection:
    """
    Создаёт таблицы всех сущностей и возвращает соединение.

    Схема строится самими сущностями: у каждой модели есть метод
    create_table(), который создаёт свою таблицу и её индексы.
    """
    connection = get_connection(db_path)
    for entity in (Tournament, Participant, Match, Result):
        entity.create_table(connection)
    connection.commit()
    return connection
