from django.urls import path
from . import views

urlpatterns = [
    path('quiz/select/', views.quiz_select, name='quiz_select'),
    path('quiz/<int:pk>/', views.quiz_take, name='quiz_take'),
    path('quiz/<int:pk>/report/', views.quiz_report, name='quiz_report'),
]
