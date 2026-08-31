from django.contrib import admin
from .models import Match, Player, SportTournament

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'location', 'start_time', 'score1', 'score2', 'winner', 'tournament')
    list_filter = ('location', 'start_time', 'tournament')
    search_fields = ('team1', 'team2', 'location', 'tournament__name')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team')
    search_fields = ('first_name', 'last_name', 'team')

@admin.register(SportTournament)
class SportTournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)