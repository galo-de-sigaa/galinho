from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('alunos/<id>/turmas/', views.turmas, name='turmas'),
    path('alunos/<id>/turmas-disponiveis/', views.turmas_disponiveis, name='turmas_disponiveis'),
    path('login/', views.login, name='login'),
]