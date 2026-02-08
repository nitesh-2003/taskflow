from django.urls import path
from . import views

urlpatterns = [
    path('kanban/<int:project_id>/', views.kanban_board, name='kanban'),
    path('create/<int:project_id>/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task_status, name='update_task_status'),
]
