"""Параметризованные SQL-запросы для системы организации турниров.

Все запросы используют параметризацию (знаки ?), чтобы предотвратить
инъекции SQL. Подключение к базе данных передаётся извне.
"""

from typing import Optional

# --- Запросы к таблице tournaments ---

SQL_LIST_TOURNAMENTS = """
    SELECT id, name, status, created_at
    FROM tournaments
    ORDER BY id
"""

SQL_GET_TOURNAMENT_BY_ID = """
    SELECT id, name, status, created_at
    FROM tournaments
    WHERE id = ?
"""

SQL_LIST_TOURNAMENTS_BY_STATUS = """
    SELECT id, name, status, created_at
    FROM tournaments
    WHERE status = ?
    ORDER BY id
"""

# --- Запросы к таблице participants ---

SQL_LIST_PARTICIPANTS_BY_TOURNAMENT = """
    SELECT id, tournament_id, name
    FROM participants
    WHERE tournament_id = ?
    ORDER BY id
"""

SQL_COUNT_PARTICIPANTS_BY_TOURNAMENT = """
    SELECT COUNT(*) AS total
    FROM participants
    WHERE tournament_id = ?
"""

SQL_LIST_PARTICIPANTS_WITH_WINS = """
    SELECT p.id, p.name, p.tournament_id, COUNT(r.id) AS wins
    FROM participants AS p
    LEFT JOIN results AS r ON r.winner_id = p.id
    WHERE p.tournament_id = ?
    GROUP BY p.id, p.name, p.tournament_id
    ORDER BY wins DESC, p.name
"""

# --- Запросы к таблице matches ---

SQL_LIST_MATCHES_BY_TOURNAMENT = """
    SELECT m.id, m.tournament_id, m.round, m.player1_id, m.player2_id,
           m.is_played,
           p1.name AS player1_name,
           p2.name AS player2_name
    FROM matches AS m
    LEFT JOIN participants AS p1 ON p1.id = m.player1_id
    LEFT JOIN participants AS p2 ON p2.id = m.player2_id
    WHERE m.tournament_id = ?
    ORDER BY m.id
"""

SQL_LIST_MATCHES_BY_ROUND = """
    SELECT m.id, m.tournament_id, m.round, m.player1_id, m.player2_id,
           m.is_played,
           p1.name AS player1_name,
           p2.name AS player2_name
    FROM matches AS m
    LEFT JOIN participants AS p1 ON p1.id = m.player1_id
    LEFT JOIN participants AS p2 ON p2.id = m.player2_id
    WHERE m.tournament_id = ? AND m.round = ?
    ORDER BY m.id
"""

SQL_COUNT_PLAYED_MATCHES_BY_TOURNAMENT = """
    SELECT COUNT(*) AS total
    FROM matches
    WHERE tournament_id = ? AND is_played = 1
"""

SQL_COUNT_UNPLAYED_MATCHES_BY_TOURNAMENT = """
    SELECT COUNT(*) AS total
    FROM matches
    WHERE tournament_id = ? AND is_played = 0
"""

# --- Запросы к таблице results ---

SQL_LIST_RESULTS_BY_TOURNAMENT = """
    SELECT r.id, r.match_id, r.winner_id, r.score, r.created_at,
           p.name AS winner_name,
           m.round AS match_round
    FROM results AS r
    JOIN matches AS m ON m.id = r.match_id
    LEFT JOIN participants AS p ON p.id = r.winner_id
    WHERE m.tournament_id = ?
    ORDER BY r.id
"""

SQL_GET_RESULT_BY_MATCH = """
    SELECT r.id, r.match_id, r.winner_id, r.score, r.created_at,
           p.name AS winner_name
    FROM results AS r
    LEFT JOIN participants AS p ON p.id = r.winner_id
    WHERE r.match_id = ?
"""

# --- Агрегирующие запросы (GROUP BY, HAVING, COUNT, AVG) ---

SQL_TOURNAMENTS_WITH_PARTICIPANT_COUNT = """
    SELECT t.id, t.name, t.status, t.created_at,
           COUNT(p.id) AS participant_count
    FROM tournaments AS t
    LEFT JOIN participants AS p ON p.tournament_id = t.id
    GROUP BY t.id, t.name, t.status, t.created_at
    ORDER BY t.id
"""

SQL_TOURNAMENTS_WITH_MIN_PARTICIPANTS = """
    SELECT t.id, t.name, t.status, t.created_at,
           COUNT(p.id) AS participant_count
    FROM tournaments AS t
    LEFT JOIN participants AS p ON p.tournament_id = t.id
    GROUP BY t.id, t.name, t.status, t.created_at
    HAVING COUNT(p.id) > ?
    ORDER BY participant_count DESC
"""

SQL_OVERALL_TOURNAMENT_STATISTICS = """
    SELECT
        COUNT(DISTINCT t.id) AS total_tournaments,
        COUNT(p.id) AS total_participants,
        COUNT(m.id) AS total_matches,
        COUNT(r.id) AS total_results,
        AVG(COUNT(p.id)) OVER () AS avg_participants_per_tournament
    FROM tournaments AS t
    LEFT JOIN participants AS p ON p.tournament_id = t.id
    LEFT JOIN matches AS m ON m.tournament_id = t.id
    LEFT JOIN results AS r ON r.match_id = m.id
"""

SQL_PARTICIPANT_WIN_STATISTICS = """
    SELECT p.id, p.name,
           COUNT(r.id) AS wins
    FROM participants AS p
    LEFT JOIN results AS r ON r.winner_id = p.id
    GROUP BY p.id, p.name
    HAVING COUNT(r.id) > 0
    ORDER BY wins DESC, p.name
"""


def execute_query(
    connection,
    query: str,
    params: Optional[tuple] = None,
) -> list:
    """Выполняет параметризованный SQL-запрос и возвращает список строк."""
    cursor = connection.execute(query, params or ())
    return cursor.fetchall()


def execute_query_one(
    connection,
    query: str,
    params: Optional[tuple] = None,
):
    """Выполняет запрос и возвращает одну строку или None."""
    cursor = connection.execute(query, params or ())
    return cursor.fetchone()