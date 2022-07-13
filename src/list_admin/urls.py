from django.urls import path
from . import views


urlpatterns = [
    path('search-tasks/', views.TaskAdmin.search_user_tasks, name='search_user_tasks'),    
    path('admin-task/<int:task_id>/', views.TaskAdmin.admin_task, name='admin_task'),
    path('add-task/', views.TaskAdmin.add_task, name='add_task'),
    path('delete-task/<int:task_id>/', views.TaskAdmin.delete_task, name='delete_task'),     

    #without API
    #path('show-tasks/', views.TaskAdmin.show_user_tasks, name='show_user_tasks'),    
    #with API
    path('show-tasks/', views.TaskAdmin.show_user_tasks_from_api_rest, name='show_user_tasks'),    
    
    path('get-tasks-api/', views.TaskAdmin.get_user_tasks_api_rest, name='get_user_tasks_api_rest'),    

    
]


