"""Точка входа приложения «Система организации турниров»."""

from app import TournamentApp
from database import init_db
from services import TournamentService


def main() -> None:
    """Готовит базу данных и запускает консольное приложение."""
    connection = init_db()
    try:
        service = TournamentService(connection)
        TournamentApp(service).run()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
