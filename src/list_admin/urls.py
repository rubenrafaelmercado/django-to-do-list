from django.urls import path
from . import views


urlpatterns = [
    path('show-list/', views.TaskAdmin.list_user_tasks, name='show_list'),    
    path('admin-task/<int:pk>/', views.TaskAdmin.admin_task, name='admin_task'),
    path('add-task/', views.TaskAdmin.add_task, name='add_task'),        
]


