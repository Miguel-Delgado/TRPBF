"""Пакет репозиториев: доступ к данным сущностей в базе."""

from repositories.match_repository import MatchRepository
from repositories.participant_repository import ParticipantRepository
from repositories.result_repository import ResultRepository
from repositories.tournament_repository import TournamentRepository

__all__ = [
    "MatchRepository",
    "ParticipantRepository",
    "ResultRepository",
    "TournamentRepository",
]
