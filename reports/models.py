"""Модели Django для системы организации турниров (ПР9).

Эти модели переводят доступ к данным с raw SQL на Django ORM,
при этом сохраняют совместимость с существующей SQLite-базой данных.
Таблицы создавались вручную до ПР9, поэтому в Meta классах установлен
managed = False, а db_table указывает на существующие таблицы.
"""

from django.db import models


class Tournament(models.Model):
    """Турнир: основная сущность соревнования."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название турнира',
        help_text='Название турнира (уникальное)'
    )
    status = models.CharField(
        max_length=20,
        default='active',
        verbose_name='Статус',
        help_text='active — турнир открыт, finished — турнир завершен'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        db_table = 'tournaments'
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        # managed = False так как таблица уже существует в базе данных
        # Django не будет создавать/убирать таблицу при миграциях

    def __str__(self):
        return f"Турнир #{self.pk}: {self.name} [{self.status}]"

    def is_active(self) -> bool:
        """Проверка: турнир еще не завершен."""
        return self.status == 'active'


class Participant(models.Model):
    """Участник турнира."""
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='participants',
        verbose_name='Турнир'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Имя участника'
    )

    class Meta:
        db_table = 'participants'
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f"Участник #{self.pk}: {self.name}"

    def get_tournament(self):
        """Получить турнир participanta."""
        return self.tournament


class Match(models.Model):
    """Матч в рамках турнира."""
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='matches',
        verbose_name='Турнир'
    )
    round = models.IntegerField(
        default=1,
        verbose_name='Раунд'
    )
    player1 = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matches_as_player1',
        verbose_name='Игрок 1'
    )
    player2 = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='matches_as_player2',
        verbose_name='Игрок 2'
    )
    is_played = models.BooleanField(
        default=False,
        verbose_name='Сыгран'
    )

    class Meta:
        db_table = 'matches'
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'

    def __str__(self):
        p1 = self.player1.name if self.player1 else '—'
        p2 = self.player2.name if self.player2 else '—'
        status = 'сыгран' if self.is_played else 'не сыгран'
        return f"Матч {self.round}: {p1} vs {p2} [{status}]"

    def is_bye(self) -> bool:
        """Проверка: у одного из игроков не нашлась пара."""
        return self.player1 is None or self.player2 is None

    def winner_id(self):
        """Получить ID победителя прохода (bye)."""
        if self.is_bye:
            p1_id = self.player1.id if self.player1 else None
            p2_id = self.player2.id if self.player2 else None
            return p1_id or p2_id
        return None


class Result(models.Model):
    """Результат сыгранного матча."""
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Матч'
    )
    winner = models.ForeignKey(
        Participant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='results_as_winner',
        verbose_name='Победитель'
    )
    score = models.CharField(
        max_length=10,
        default='',
        verbose_name='Счет'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата результата'
    )

    class Meta:
        db_table = 'results'
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        if self.winner:
            winner_name = self.winner.name
        elif self.winner_id is not None:
            winner_name = f'id {self.winner_id}'
        else:
            winner_name = 'не определен'
        score_text = f', счет {self.score}' if self.score else ''
        result_head = 'Результат матча #' + str(self.match_id) + ': '
        result_text = result_head + winner_name + score_text
        return result_text
