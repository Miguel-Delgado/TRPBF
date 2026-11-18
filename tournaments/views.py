"""Представления приложения tournaments."""

from django.shortcuts import render

from database import get_connection
from services import TournamentService


def _get_service():
    """Создаёт сервис турнира с соединением к БД."""
    connection = get_connection()
    return TournamentService(connection), connection


def tournament_list(request):
    """Страница списка всех турниров."""
    service, connection = _get_service()
    try:
        tournaments = service.list_tournaments()
    finally:
        connection.close()
    context = {
        'tournaments': tournaments,
    }
    return render(request, 'tournaments/list.html', context)


def tournament_detail(request, tournament_id):
    """Страница отдельного турнира с участниками и матчами."""
    service, connection = _get_service()
    try:
        tournament = service.get_tournament(tournament_id)
        if tournament is None:
            return render(request, '404.html', status=404)
        participants = service.list_participants(tournament_id)
        matches = service.list_matches(tournament_id)
    finally:
        connection.close()
    context = {
        'tournament': tournament,
        'participants': participants,
        'matches': matches,
    }
    return render(request, 'tournaments/detail.html', context)
