from django.contrib import admin
from .models import Match, Player

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'location', 'start_time', 'score1', 'score2', 'winner')
    list_filter = ('location', 'start_time')
    search_fields = ('team1', 'team2', 'location')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'team')
    search_fields = ('first_name', 'last_name', 'team')