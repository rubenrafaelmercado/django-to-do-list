#from .forms import ListAdminForm
from .models import Task
from .forms import TaskAdminForm
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from datetime import datetime, timezone, timedelta


class TaskAdmin():


    def get_user_tasks_with_expired_state( user_id ):
        tasks = Task.objects.filter(user=user_id)               
        def add_expired_state(tasks):
            now = datetime.now( timezone.utc )
            i = 0
            for task in tasks:
                expired = False
                if now >= task.due_date_time and (task.status == 'T' or task.status == 'P'):
                    expired = True            
                tasks[i].is_expired = expired
                i += 1
            return tasks        
        if tasks:
            tasks = add_expired_state(tasks)
        else:
            tasks = {}        
        return tasks
    
    @login_required    
    def list_user_tasks( request ):
        tasks = TaskAdmin.get_user_tasks_with_expired_state(request.user.id)
        return render(request , 'show_user_tasks.html', {'tasks': tasks,'page_title' : 'To do list'})

    
    @login_required    
    def admin_task( request, task_id=None  ):

        page_title = 'Admin task'
        messages = {}
        
        try:
            task = Task.objects.get(pk=task_id)                 
        except ObjectDoesNotExist:
            messages['title'] = {'type':'danger','text':'This task does not exist'}
            task = {}
            status_code = 400
        else:                            
            if task.user.id != request.user.id:
                messages['title'] = {'type':'danger','text':'This task is not accessible'}
                task = {}
                status_code = 400

        if request.method == 'GET' and  task:
            status_code = 200
        
        if request.method == 'POST' and  task:
            form = TaskAdminForm( task, request.user, request.POST)
            if form.is_valid():                
                messages['title'] = {'type': 'success', 'text': 'Task successfully updated'}                
                form.save( taskToUpdate=task )
                status_code = 201
            else:
                messages['title'] = {'type': 'danger', 'text': 'Please correct this errors'}
                status_code = 400            
                field_values = {}
                for field in form:
                    error_messages = [] 
                    for error_message in field.errors:
                        error_messages.append(error_message )
                    if not error_messages:
                        error_messages = ['']
                    messages[field.html_name] = error_messages
                    
                    field_value = field.value()                
                    setattr(task,field.html_name, '')
                    if field_value:
                        setattr(task,field.html_name, field.value())
            task.due_date_time = datetime.strptime(task.due_date_time, '%Y-%m-%dT%H:%M')

        return render(request , 'admin_task.html',
                    {'task': task, 'page_title':page_title, 'messages': messages},
                    status = status_code 
                    )
    
    
    @login_required    
    def add_task( request ):
        if request.method == 'POST':        
            return HttpResponse(  'add'  )



    
    @login_required    
    def delete_task( request, task_id=None ):
        messages={}
        if request.method == 'POST':            
            try:
                task = Task.objects.get(pk=task_id)                 
            except ObjectDoesNotExist:
                messages['title'] = {'type':'danger','text':'The task to delete does not exist'}                 
            else:                            
                if task.user.id != request.user.id:
                    messages['title'] = {'type':'danger','text':'The task to delete is not accessible'}                    
                else:
                    task.delete()
                    messages['title'] = {'type':'success','text':'Task deleted successfully'}            
        else:
            messages['title'] = {'type':'danger','text':'Method to delete do not permitted'}
        tasks = TaskAdmin.get_user_tasks_with_expired_state(request.user.id)
        return render(request ,
                        'show_user_tasks.html', 
                    {'tasks':tasks,'page_title':'To do list','messages':messages})

        





    