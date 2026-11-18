from django import forms
from .models import Tournament, Participant, Match, Result


class TournamentForm(forms.ModelForm):
    """Форма для создания и редактирования турнира."""

    class Meta:
        model = Tournament
        fields = ['name', 'status']
        labels = {
            'name': 'Название турнира',
            'status': 'Статус',
        }
        help_texts = {
            'name': 'Введите название турнира',
            'status': 'active — турнир открыт, finished — турнир завершен',
        }
        error_messages = {
            'name': {
                'max_length': 'Название турнира слишком длинное',
            },
        }


class ParticipantForm(forms.ModelForm):
    """Форма для добавления участника турнира."""

    class Meta:
        model = Participant
        fields = ['tournament', 'name']
        labels = {
            'tournament': 'Турнир',
            'name': 'Имя участника',
        }
        help_texts = {
            'tournament': 'Выберите турнир из списка',
            'name': 'Введите имя участника',
        }
        error_messages = {
            'name': {
                'max_length': 'Имя участника слишком длинное',
            },
        }


class MatchForm(forms.ModelForm):
    """Форма для создания матча."""

    class Meta:
        model = Match
        fields = ['tournament', 'round', 'player1', 'player2', 'is_played']
        labels = {
            'tournament': 'Турнир',
            'round': 'Раунд',
            'player1': 'Игрок 1',
            'player2': 'Игрок 2',
            'is_played': 'Сыгран',
        }
        help_texts = {
            'tournament': 'Выберите турнир',
            'round': 'Номер раунда',
            'player1': 'Имя первого игрока',
            'player2': 'Имя второго игрока',
            'is_played': 'Является ли матч сыгранным',
        }
        error_messages = {
            'round': {
                'min_value': 'Номер раунда не может быть меньше 1',
            },
        }


class ResultForm(forms.ModelForm):
    """Форма для ввода результата матча."""

    class Meta:
        model = Result
        fields = ['match', 'winner', 'score']
        labels = {
            'match': 'Матч',
            'winner': 'Победитель',
            'score': 'Счет',
        }
        help_texts = {
            'match': 'Выберите матч',
            'winner': 'Выберите победителя',
            'score': 'Введите счет матча',
        }
        error_messages = {
            'score': {
                'max_length': 'Счет слишком длинный',
            },
        }
