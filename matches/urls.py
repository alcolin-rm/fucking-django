from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.matches_list, name='matches_list'),          # /matches/
    path('live/', views.matches_live, name='matches_live'),    # /matches/live/
    path('future/', views.matches_future, name='matches_future'),  # /matches/future/
    path('<int:id>/', views.match_detail, name='match_detail'), # /matches/<id>/
]