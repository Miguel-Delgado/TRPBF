"""Представления приложения matches."""

from django.shortcuts import render

from database import get_connection
from services import TournamentService


def _get_service():
    """Создаёт сервис турнира с соединением к БД."""
    connection = get_connection()
    return TournamentService(connection), connection


def match_list(request, tournament_id=None):
    """Список матчей (всех или для конкретного турнира)."""
    service, connection = _get_service()
    try:
        if tournament_id is not None:
            tournament = service.get_tournament(tournament_id)
            if tournament is None:
                return render(request, '404.html', status=404)
            matches = service.list_matches(tournament_id)
            context = {
                'matches': matches,
                'tournament': tournament,
            }
        else:
            # Все матчи всех турниров
            tournaments = service.list_tournaments()
            all_matches = []
            for tournament in tournaments:
                assert tournament.id is not None
                matches = service.list_matches(tournament.id)
                all_matches.extend((tournament, m) for m in matches)
            context = {
                'all_matches': all_matches,
            }
    finally:
        connection.close()
    return render(request, 'matches/list.html', context)
