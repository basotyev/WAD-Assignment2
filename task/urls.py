from django.urls import path
from .views import task_list, task_detail, task_create

urlpatterns = [
    path('', task_list, name='task_list'),
    path('<int:task_id>/', task_detail, name='task_detail'),
    path('create/', task_create, name='task_create'),
]