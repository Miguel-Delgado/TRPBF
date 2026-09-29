"""Конфигурация pytest: пути импорта и общие фикстуры базы данных."""

import pytest

from database import init_db
from services import TournamentService


@pytest.fixture()
def connection():
    """Открывает соединение с тестовой базой данных в памяти."""
    conn = init_db(":memory:")
    yield conn
    conn.close()


@pytest.fixture()
def service(connection):
    """Создаёт сервис турнира поверх тестовой базы данных."""
    return TournamentService(connection)
