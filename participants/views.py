"""Представления приложения participants."""

from django.shortcuts import render

from database import get_connection
from services import TournamentService


def _get_service():
    """Создаёт сервис турнира с соединением к БД."""
    connection = get_connection()
    return TournamentService(connection), connection


def participant_list(request, tournament_id=None):
    """Список участников (всех или для конкретного турнира)."""
    service, connection = _get_service()
    try:
        if tournament_id is not None:
            tournament = service.get_tournament(tournament_id)
            if tournament is None:
                return render(request, '404.html', status=404)
            participants = service.list_participants(tournament_id)
            context = {
                'participants': participants,
                'tournament': tournament,
            }
        else:
            # Все участники всех турниров — соберём из каждого турнира
            tournaments = service.list_tournaments()
            all_participants = []
            for tournament in tournaments:
                participants = service.list_participants(tournament.id)
                for p in participants:
                    all_participants.append((tournament, p))
            context = {
                'all_participants': all_participants,
            }
    finally:
        connection.close()
    return render(request, 'participants/list.html', context)
