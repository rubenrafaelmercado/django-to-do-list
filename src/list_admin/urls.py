from django.urls import path
from . import views


urlpatterns = [
    path('show-list/', views.TaskAdmin.list_user_tasks, name='show_user_tasks'),    
    path('search-tasks/', views.TaskAdmin.search_user_tasks, name='search_user_tasks'),    
    path('admin-task/<int:task_id>/', views.TaskAdmin.admin_task, name='admin_task'),
    path('add-task/', views.TaskAdmin.add_task, name='add_task'),
    path('delete-task/<int:task_id>/', views.TaskAdmin.delete_task, name='delete_task'),        
]


