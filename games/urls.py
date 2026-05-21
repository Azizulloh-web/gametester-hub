from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views_api import GameListAPI, GameDetailAPI

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('add-game/', views.add_game, name='add_game'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('game/<int:pk>/edit/', views.edit_game, name='edit_game'),
    path('game/<int:pk>/delete/', views.delete_game, name='delete_game'),
    path('game/<int:pk>/like/', views.like_game, name='like_game'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='games/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('api/games/', GameListAPI.as_view(), name='api-game-list'),
    path('api/games/<int:pk>/', GameDetailAPI.as_view(), name='api-game-detail'),
]

