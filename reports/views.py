"""Представления для отчётов на основе SQL-запросов (ПР7)."""

from django.shortcuts import render

from database import get_connection
import sql_queries


def _get_connection():
    """Открывает соединение с базой данных."""
    return get_connection()


def report_index(request):
    """Главная страница отчётов со списком доступных отчётов."""
    return render(request, 'reports/index.html')


def tournament_list_report(request):
    """Отчёт: список всех турниров."""
    conn = _get_connection()
    try:
        tournaments = sql_queries.execute_query(
            conn, sql_queries.SQL_LIST_TOURNAMENTS
        )
    finally:
        conn.close()
    context = {'tournaments': tournaments}
    return render(request, 'reports/tournament_list.html', context)


def tournament_participants_report(request, tournament_id):
    """Отчёт: участники конкретного турнира."""
    conn = _get_connection()
    try:
        tournament = sql_queries.execute_query_one(
            conn, sql_queries.SQL_GET_TOURNAMENT_BY_ID, (tournament_id,)
        )
        if tournament is None:
            return render(request, '404.html', status=404)
        participants = sql_queries.execute_query(
            conn, sql_queries.SQL_LIST_PARTICIPANTS_BY_TOURNAMENT,
            (tournament_id,)
        )
    finally:
        conn.close()
    context = {
        'tournament': tournament,
        'participants': participants,
    }
    return render(request, 'reports/tournament_participants.html', context)


def tournament_matches_report(request, tournament_id):
    """Отчёт: матчи конкретного турнира с именами игроков."""
    conn = _get_connection()
    try:
        tournament = sql_queries.execute_query_one(
            conn, sql_queries.SQL_GET_TOURNAMENT_BY_ID, (tournament_id,)
        )
        if tournament is None:
            return render(request, '404.html', status=404)
        matches = sql_queries.execute_query(
            conn, sql_queries.SQL_LIST_MATCHES_BY_TOURNAMENT,
            (tournament_id,)
        )
    finally:
        conn.close()
    context = {
        'tournament': tournament,
        'matches': matches,
    }
    return render(request, 'reports/tournament_matches.html', context)


def tournament_results_report(request, tournament_id):
    """Отчёт: результаты матчей турнира."""
    conn = _get_connection()
    try:
        tournament = sql_queries.execute_query_one(
            conn, sql_queries.SQL_GET_TOURNAMENT_BY_ID, (tournament_id,)
        )
        if tournament is None:
            return render(request, '404.html', status=404)
        results = sql_queries.execute_query(
            conn, sql_queries.SQL_LIST_RESULTS_BY_TOURNAMENT,
            (tournament_id,)
        )
    finally:
        conn.close()
    context = {
        'tournament': tournament,
        'results': results,
    }
    return render(request, 'reports/tournament_results.html', context)


def tournament_stats_report(request, tournament_id):
    """Отчёт: статистика турнира (участники, сыгранные матчи, победы)."""
    conn = _get_connection()
    try:
        tournament = sql_queries.execute_query_one(
            conn, sql_queries.SQL_GET_TOURNAMENT_BY_ID, (tournament_id,)
        )
        if tournament is None:
            return render(request, '404.html', status=404)
        participants = sql_queries.execute_query(
            conn, sql_queries.SQL_LIST_PARTICIPANTS_WITH_WINS,
            (tournament_id,)
        )
        played = sql_queries.execute_query_one(
            conn, sql_queries.SQL_COUNT_PLAYED_MATCHES_BY_TOURNAMENT,
            (tournament_id,)
        )
        unplayed = sql_queries.execute_query_one(
            conn, sql_queries.SQL_COUNT_UNPLAYED_MATCHES_BY_TOURNAMENT,
            (tournament_id,)
        )
        participant_count = sql_queries.execute_query_one(
            conn, sql_queries.SQL_COUNT_PARTICIPANTS_BY_TOURNAMENT,
            (tournament_id,)
        )
    finally:
        conn.close()
    context = {
        'tournament': tournament,
        'participants': participants,
        'matches_played': played['total'] if played else 0,
        'matches_unplayed': unplayed['total'] if unplayed else 0,
        'participant_count': (
            participant_count['total'] if participant_count else 0
        ),
    }
    return render(request, 'reports/tournament_stats.html', context)


def overall_statistics_report(request):
    """Отчёт: общая статистика по всем турнирам."""
    conn = _get_connection()
    try:
        stats = sql_queries.execute_query_one(
            conn, sql_queries.SQL_OVERALL_TOURNAMENT_STATISTICS
        )
        tournaments_with_count = sql_queries.execute_query(
            conn, sql_queries.SQL_TOURNAMENTS_WITH_PARTICIPANT_COUNT
        )
        win_statistics = sql_queries.execute_query(
            conn, sql_queries.SQL_PARTICIPANT_WIN_STATISTICS
        )
    finally:
        conn.close()
    context = {
        'stats': dict(stats) if stats else {},
        'tournaments_with_count': tournaments_with_count,
        'win_statistics': win_statistics,
    }
    return render(request, 'reports/overall_statistics.html', context)

