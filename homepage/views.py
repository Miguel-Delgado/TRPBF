"""Представления приложения homepage."""

from django.shortcuts import render

from database import get_connection
from services import TournamentService


def _get_service():
    """Создаёт сервис турнира с соединением к БД."""
    connection = get_connection()
    return TournamentService(connection), connection


def home(request):
    """Главная страница системы организации турниров."""
    service, connection = _get_service()
    try:
        tournaments = service.list_tournaments()
    finally:
        connection.close()
    context = {
        'tournaments': tournaments,
    }
    return render(request, 'homepage/home.html', context)


def error_404(request, exception=None):
    """Страница ошибки 404."""
    return render(request, '404.html', status=404)
