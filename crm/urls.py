from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('records/', views.record_list, name='record_list'),
    path('records/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/create/', views.record_create, name='record_create'),
    path('records/<int:pk>/update/', views.record_update, name='record_update'),
    path('records/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('events/', views.event_list, name='event_list'),
]
