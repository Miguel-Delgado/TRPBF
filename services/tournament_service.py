"""Бизнес-логика турнира: жеребьёвка, матчи и результаты."""

import random
import sqlite3

from models import (
    STATUS_FINISHED,
    Match,
    Participant,
    Result,
    Tournament,
)
from repositories import (
    MatchRepository,
    ParticipantRepository,
    ResultRepository,
    TournamentRepository,
)


class TournamentService:
    """Сервис, объединяющий репозитории и правила предметной области."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.tournaments = TournamentRepository(connection)
        self.participants = ParticipantRepository(connection)
        self.matches = MatchRepository(connection)
        self.results = ResultRepository(connection)

    # --- Турниры ---
    def create_tournament(self, name: str) -> Tournament:
        """Создаёт новый турнир."""
        return self.tournaments.add(Tournament(name))

    def list_tournaments(self) -> list[Tournament]:
        """Возвращает список всех турниров."""
        return self.tournaments.get_all()

    def get_tournament(self, tournament_id: int) -> Tournament | None:
        """Возвращает турнир по id."""
        return self.tournaments.get_by_id(tournament_id)

    def finish_tournament(self, tournament_id: int) -> None:
        """Отмечает турнир завершённым."""
        self.tournaments.update_status(tournament_id, STATUS_FINISHED)

    # --- Участники ---
    def add_participant(
        self,
        tournament_id: int,
        name: str,
    ) -> Participant:
        """Регистрирует участника в турнире."""
        return self.participants.add(
            Participant(name, tournament_id)
        )

    def list_participants(self, tournament_id: int) -> list[Participant]:
        """Возвращает участников турнира."""
        return self.participants.get_by_tournament(tournament_id)

    # --- Жеребьёвка и матчи ---
    def draw_matches(self, tournament_id: int) -> list[Match]:
        """
        Формирует матчи первого тура.

        Участники перемешиваются и разбиваются на пары. При нечётном
        числе участников последний получает проход (bye): пара
        создаётся с пустым вторым игроком (NULL в БД).
        """
        participants = self.participants.get_by_tournament(tournament_id)
        if len(participants) < 2:
            raise ValueError(
                "Для жеребьёвки нужно не менее двух участников."
            )

        self.results.delete_by_tournament(tournament_id)
        self.matches.delete_by_tournament(tournament_id)

        shuffled = list(participants)
        random.shuffle(shuffled)

        created: list[Match] = []
        for index in range(0, len(shuffled), 2):
            first = shuffled[index]
            second = (
                shuffled[index + 1] if index + 1 < len(shuffled) else None
            )
            match = Match(
                tournament_id=tournament_id,
                round_number=1,
                player1_id=first.id,
                player2_id=second.id if second is not None else None,
            )
            created.append(self.matches.add(match))
        return created

    def list_matches(self, tournament_id: int) -> list[Match]:
        """Возвращает матчи турнира с именами игроков."""
        return self.matches.get_by_tournament(tournament_id)

    # --- Результаты ---
    def record_result(
        self,
        match: Match,
        winner_side: int = 1,
        score: str = "",
    ) -> Result:
        """Сохраняет результат матча и определяет победителя."""
        if match.id is None:
            raise ValueError("Матч не сохранён в базе данных.")

        if match.is_bye:
            winner_id = match.winner_id()
        elif winner_side == 1:
            winner_id = match.player1_id
        elif winner_side == 2:
            winner_id = match.player2_id
        else:
            raise ValueError("Сторона победителя должна быть 1 или 2.")

        self.matches.set_played(match.id, True)
        return self.results.add(Result(match.id, winner_id, score))

    def list_results(self, tournament_id: int) -> list[Result]:
        """Возвращает результаты матчей турнира."""
        return self.results.get_by_tournament(tournament_id)

    def standings(self, tournament_id: int) -> list[tuple[str, int]]:
        """Возвращает список (имя участника, число побед) по убыванию."""
        wins: dict[str, int] = {
            participant.name: 0
            for participant in self.participants.get_by_tournament(
                tournament_id
            )
        }
        for result in self.results.get_by_tournament(tournament_id):
            if result.winner_name in wins:
                wins[result.winner_name] += 1
        return sorted(wins.items(), key=lambda item: (-item[1], item[0]))
