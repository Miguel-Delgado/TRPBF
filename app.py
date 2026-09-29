"""Консольный интерфейс системы организации турниров."""

from models import Match
from services import TournamentService
from utils import input_int, input_name

MENU = """
=============== МЕНЮ ===============
 1 - Создать новый турнир
 2 - Показать список турниров
 3 - Выбрать активный турнир
 4 - Добавить участников
 5 - Показать участников
 6 - Провести жеребьёвку
 7 - Показать матчи
 8 - Внести результат матча
 9 - Показать результаты и зачёт
 0 - Выход
====================================
"""

SEPARATOR = "=" * 50


class TournamentApp:
    """Консольное приложение: меню, ввод и вывод информации."""

    def __init__(self, service: TournamentService) -> None:
        self.service = service
        self.active_tournament_id: int | None = None

    def run(self) -> None:
        """Главный цикл консольного меню."""
        print(SEPARATOR)
        print("   Добро пожаловать в систему организации турниров!")
        print(SEPARATOR)
        self._select_last_tournament()

        handlers = {
            1: self._create_tournament,
            2: self._list_tournaments,
            3: self._choose_tournament,
            4: self._add_participants,
            5: self._show_participants,
            6: self._draw_matches,
            7: self._show_matches,
            8: self._record_result,
            9: self._show_results,
        }

        while True:
            print(MENU)
            choice = input_int("Выберите пункт меню: ", minimum=0)
            if choice == 0:
                print("Спасибо за использование! До встречи.")
                return
            handler = handlers.get(choice)
            if handler is None:
                print("Ошибка: неизвестный пункт меню.")
                continue
            handler()

    # --- Служебные методы ---
    def _select_last_tournament(self) -> None:
        tournaments = self.service.list_tournaments()
        if not tournaments:
            print("Сохранённых турниров нет. Создайте новый (пункт 1).")
            return
        last = tournaments[-1]
        self.active_tournament_id = last.id
        print(f"Активный турнир: '{last.name}' (id: {last.id}).")

    def _require_tournament(self) -> int | None:
        if self.active_tournament_id is None:
            print("Сначала создайте или выберите турнир (пункты 1 или 3).")
            return None
        return self.active_tournament_id

    @staticmethod
    def _print_matches(matches: list[Match]) -> None:
        for number, match in enumerate(matches, 1):
            print(f"  {number}. {match}")

    # --- Пункты меню ---
    def _create_tournament(self) -> None:
        print("\n--- Создание турнира ---")
        name = input_name("Введите название турнира: ")
        tournament = self.service.create_tournament(name)
        self.active_tournament_id = tournament.id
        print(f"Турнир '{tournament.name}' создан (id: {tournament.id}).")

    def _list_tournaments(self) -> None:
        tournaments = self.service.list_tournaments()
        print("\nСписок турниров:")
        if not tournaments:
            print("  (пока пусто)")
            return
        for tournament in tournaments:
            mark = ""
            if tournament.id == self.active_tournament_id:
                mark = "  <- активный"
            print(f"  id {tournament.id}: {tournament.name} "
                  f"[{tournament.status}]{mark}")

    def _choose_tournament(self) -> None:
        tournaments = self.service.list_tournaments()
        if not tournaments:
            print("Сохранённых турниров нет.")
            return
        self._list_tournaments()
        tournament_id = input_int("Введите id турнира: ")
        if self.service.get_tournament(tournament_id) is None:
            print("Турнир с таким id не найден.")
            return
        self.active_tournament_id = tournament_id
        print(f"Выбран турнир id {tournament_id}.")

    def _add_participants(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        print("\n--- Добавление участников ---")
        count = input_int(
            "Введите количество участников (целое число > 0): "
        )
        for number in range(1, count + 1):
            name = input_name(
                f"Введите имя участника #{number}: ",
                f"Участник {number}",
            )
            participant = self.service.add_participant(
                tournament_id, name
            )
            print(f"  Добавлен: {participant.name} "
                  f"(id: {participant.id})")

    def _show_participants(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        participants = self.service.list_participants(tournament_id)
        print("\nСписок участников:")
        if not participants:
            print("  (пока пусто)")
            return
        for number, participant in enumerate(participants, 1):
            print(f"  {number}. {participant}")

    def _draw_matches(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        print("\n--- Жеребьёвка ---")
        try:
            matches = self.service.draw_matches(tournament_id)
        except ValueError as error:
            print(f"Ошибка: {error}")
            return
        print(f"Сформировано матчей: {len(matches)}")
        self._print_matches(matches)

    def _show_matches(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        matches = self.service.list_matches(tournament_id)
        if not matches:
            print("Матчи не сформированы. Выполните жеребьёвку (пункт 6).")
            return
        print("\nМатчи турнира:")
        self._print_matches(matches)

    def _record_result(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        matches = self.service.list_matches(tournament_id)
        if not matches:
            print("Матчи не сформированы. Выполните жеребьёвку (пункт 6).")
            return
        self._print_matches(matches)
        number = input_int("Введите номер матча: ")
        if number > len(matches):
            print("Матча с таким номером нет.")
            return
        match = matches[number - 1]
        if match.is_played:
            print("Результат этого матча уже внесён.")
            return

        if match.is_bye:
            winner_side = 1
            score = "bye"
            winner = match.player1_name or match.player2_name
            print(f"Проход (bye): {winner} получает победу без игры.")
        else:
            winner_side = input_int("Кто победил? (1 или 2): ")
            if winner_side not in (1, 2):
                print("Ошибка: нужно ввести 1 или 2.")
                return
            score = input_name("Введите счёт (например, 2:1): ", "2:0")

        result = self.service.record_result(match, winner_side, score)
        print(f"Результат сохранён: {result}")

    def _show_results(self) -> None:
        tournament_id = self._require_tournament()
        if tournament_id is None:
            return
        results = self.service.list_results(tournament_id)
        print("\nРезультаты матчей:")
        if not results:
            print("  (результатов пока нет)")
        for result in results:
            print(f"  {result}")

        print("\nЗачёт (число побед):")
        standings = self.service.standings(tournament_id)
        if not standings:
            print("  (пока пусто)")
            return
        for place, (name, wins) in enumerate(standings, 1):
            print(f"  {place}. {name} — {wins} побед(ы)")
