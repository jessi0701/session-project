from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/',views.detail, name='detail'),
    path('<int:movie_id>/like/',views.like, name='like'),
    path('<int:id>/scores/new/', views.score_create, name='score_create'),
    path('<int:movie_id>/scores/<int:score_id>/delete/', views.score_delete, name='score_delete'),
    path('<int:movie_id>/scores/<int:score_id>/edit/', views.score_edit, name='score_edit'),
    path('search/',views.search, name='search'),
    path('search/',views.search, name='search'),
    path('classification/', views.classification, name='classification'),
    ]