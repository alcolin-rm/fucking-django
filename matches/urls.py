from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('<int:id>/', views.match_detail, name='match_detail'),
    # если используете классовый view, то:
    # path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
]