from django.contrib import admin

from .models import Match, Participant, Result, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Admin configuration for Tournament model."""

    list_display = ('name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {'fields': ('name', 'status')}),
        ('Даты', {'fields': ('created_at',)}),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related()


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    """Admin configuration for Participant model."""

    list_display = ('name', 'tournament', 'get_tournament_name')
    list_filter = ('tournament',)
    search_fields = ('name',)
    ordering = ('tournament', 'name')
    raw_id_fields = ('tournament',)

    def get_tournament_name(self, obj):
        """Display tournament name for participant."""
        return obj.tournament.name if obj.tournament else '-'

    get_tournament_name.short_description = 'Турнир'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('tournament')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Admin configuration for Match model."""

    list_display = ('__str__', 'tournament', 'round', 'is_played')
    list_filter = ('tournament', 'is_played')
    search_fields = ('tournament__name', 'round')
    ordering = ('tournament', 'round')
    raw_id_fields = ('player1', 'player2', 'tournament')

    def get_players(self, obj):
        p1_name = obj.player1.name if obj.player1 else '—'
        p2_name = obj.player2.name if obj.player2 else '—'
        players_text = f'{p1_name} vs {p2_name}'
        return players_text[:32] + '...' if len(players_text) > 32 else players_text

    get_players.short_description = 'Игроки'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('tournament', 'player1')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Admin configuration for Result model."""

    list_display = ('__str__', 'match', 'winner_display', 'score')
    list_filter = ('match__tournament', 'created_at')
    search_fields = ('match__tournament__name', 'score')
    ordering = ('-created_at',)
    raw_id_fields = ('match', 'winner')
    date_hierarchy = 'created_at'

    def winner_display(self, obj):
        """Display winner name."""
        if obj.winner:
            return obj.winner.name
        return '—'

    winner_display.short_description = 'Победитель'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('match', 'winner')
