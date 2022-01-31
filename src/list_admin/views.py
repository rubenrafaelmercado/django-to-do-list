#from .forms import ListAdminForm
from .models import Task
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test


from datetime import datetime, timezone, timedelta


class TaskAdmin():


    '''
    def owned_resource_required(function=None):
        def is_owned_resource(user_to_verify):
            return user.id == user_to_verify.id 
        actual_decorator = user_passes_test(is_owned_resource)
        if function:
            return actual_decorator(function)
        else:
            return actual_decorator
    @owned_resource_required
    '''

    
    @login_required    
    def list_user_tasks( request ):
        
        tasks = Task.objects.filter(user=request.user.id)
               
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

        #raise Exception ( tasks )

        return render(request , 'show_user_tasks.html',
                {'tasks': tasks,
                'title' : 'To do list',}
                )

    @login_required    
    def admin_task( request, pk=None  ):
        if pk:
            return HttpResponse(  'view /edit'  )
        else:
            return HttpResponse(  'bad request'  )



    @login_required    
    def add_task( request ):        
            return HttpResponse(  'add'  )



