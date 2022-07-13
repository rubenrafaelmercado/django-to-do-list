import random
from .task_statuses import TASK_STATUSES
from .models import Task
from .forms import TaskAdminForm, UserTasksSearchForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

#from django.forms.models import model_to_dict
from django.core import serializers


from datetime import datetime, timezone, timedelta



class TaskAdmin():

    @login_required    
    @require_http_methods(['GET','POST'])
    def search_user_tasks( request ):
        messages = {}
        field_values={}
        tasks = TaskAdmin.get_user_tasks_with_is_expired(request.user.id)
        if not tasks:
            messages['title'] = { 'type':'danger','text':'There are no tasks created yet'}
            http_status = 202
        else:
            http_status = 200
            if request.method == 'POST':            
                form = UserTasksSearchForm(request.POST)
                if form.is_valid():
                    field_values = form.cleaned_data
                    name = form.cleaned_data['name']
                    description = form.cleaned_data['description']
                    status = form.cleaned_data['status']

                    if name == '' and  description == '' and (status!='' and status!='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(status=status)
                    elif name == '' and  description == '' and (status=='' or status=='A'):
                        tasks = Task.objects.filter(user=request.user)                    
                    elif name == '' and  description != '' and  (status=='' or status=='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(description__contains=description)
                    elif name == '' and description != '' and (status!='' and status!='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(status=status) \
                            & Task.objects.filter(description__contains=description)
                    elif name != '' and  description == '' and  (status=='' or status=='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(name__contains=name)
                    elif name != '' and  description == '' and  (status!='' and status!='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(name__contains=name) \
                            & Task.objects.filter(status=status)
                    elif name != '' and  description != '' and  (status=='' or status=='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(name__contains=name) \
                            & Task.objects.filter(description__contains=description)
                    elif name != '' and description != '' and  (status!='' and status!='A'):
                        tasks = Task.objects.filter(user=request.user) \
                            & Task.objects.filter(name__contains=name) \
                            & Task.objects.filter(status=status) \
                            & Task.objects.filter(description__contains=description)
                
                if not tasks:
                    messages['title'] = { 'type':'secondary','text':'There are no tasks found'}
                    http_status = 202
                else:
                    messages['title'] = { 'type':'success','text': 'It was found ' + str(len(tasks)) + ' tasks'}
                    http_status = 200
        return render(request,'search_user_tasks.html',
                     {'tasks':tasks, 'messages':messages, 'field_values':field_values},
                      status = http_status)


    def get_user_tasks_with_is_expired( user_id ):
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
    @require_http_methods(['GET'])
    def show_user_tasks( request ):
        tasks = TaskAdmin.get_user_tasks_with_is_expired(request.user.id)
        messages = {}
        if not tasks:
            messages['secondary_title'] = { 'type':'danger','text':'There are no tasks to list'}
            http_status = 202
        else:
            http_status = 200
        if 'feedback_message_type' in request.session and 'feedback_message_text' in request.session:            
            messages['title'] = { 'type':request.session['feedback_message_type'],
                                  'text':request.session['feedback_message_text']}
            del request.session['feedback_message_type']
            del request.session['feedback_message_text']
        return render(request , 'show_user_tasks.html', {'tasks':tasks, 'messages':messages}, status = http_status)
    
    def query_set_to_dictionary( query_set, attributes ):
        dictionary_set = {}
        for query_object in query_set:
            dictionary = {}
            for attribute in  attributes:                
                dictionary[attribute] = getattr(query_object,attribute)
            dictionary_set[query_object.id] = dictionary
        return dictionary_set


    @login_required    
    @require_http_methods(['GET'])
    def show_user_tasks_from_api_rest( request ): 
        messages = {}      
        http_status = 200
        if 'feedback_message_type' in request.session and 'feedback_message_text' in request.session:            
            messages['title'] = { 'type':request.session['feedback_message_type'],
                                  'text':request.session['feedback_message_text']}
            del request.session['feedback_message_type']
            del request.session['feedback_message_text']
        return render(request , 
                    'show_user_tasks_from_api_rest.html',
                    {'messages':messages, 'use_api_rest': True },
                     status = http_status )


    @login_required    
    @require_http_methods(['GET'])
    def get_user_tasks_api_rest( request ):                
        tasks_query_set = TaskAdmin.get_user_tasks_with_is_expired(request.user.id)
        if not tasks_query_set:
            tasks_dictionary = { 'message':'There are no tasks to list'}
            http_status = 202
        else:
            i = 0            
            task_statuses_dictionary = dict(TASK_STATUSES)
            for task in tasks_query_set:
                tasks_query_set[i].status_description = task_statuses_dictionary[task.status]
                tasks_query_set[i].due_date_time = task.due_date_time.strftime('%b-%d-%Y %H:%M')
                tasks_query_set[i].created_date = task.created_date.strftime ('%b-%d-%Y')
                i += 1
            attributes = [ 'id', 'name', 'due_date_time', 'status_description', 'created_date', 'description', 'is_expired']
            tasks_dictionary = TaskAdmin.query_set_to_dictionary( tasks_query_set, attributes )
            http_status = 200
        return JsonResponse(tasks_dictionary, status=http_status)
       
    @login_required
    @require_http_methods(['GET', 'POST'])    
    def admin_task( request, task_id=None  ):
        messages = {}        
        try:
            task = Task.objects.get(pk=task_id)                 
        except ObjectDoesNotExist:
            messages['title'] = {'type':'danger','text':'Task non-existent'}
            task = {}
            http_status = 400
        else:                            
            if task.user.id != request.user.id:
                messages['title'] = {'type':'danger','text':'Task not accessible'}
                task = {}
                http_status = 403       
        if request.method == 'GET' and  task:            
            http_status = 200            
            form_fields = ['name', 'description', 'status', 'comment', 'due_date_time']
            for field in form_fields:
                messages[field] = {'texts':[], 'input_css_class':'', 'message_css_class':'d-none'}        
        if request.method == 'POST' and  task:
            form = TaskAdminForm( task, request.user, request.POST)            
            if form.is_valid():                                
                form.save( taskToUpdate=task )                
                messages['title'] = {'type':'success', 'text':'Task updated'}
                http_status = 201
            else:
                messages['title'] = {'type':'danger', 'text':'Please revise this data'}
                http_status = 400            
                field_values = {}
                for field in form:                    
                    form_messages = [] 
                    for error_message in field.errors:
                        form_messages.append(error_message )
                    messages[field.html_name]= {'input_css_class':'', 'message_css_class':'d-none', 'texts':[]}
                    if form_messages:
                        messages[field.html_name]= {
                            'input_css_class':'is-invalid',
                            'message_css_class':'invalid-feedback',
                            'texts':form_messages}
                    field_value = field.value()                
                    setattr(task,field.html_name, '')
                    if field_value:
                        setattr(task,field.html_name, field_value)
            task.due_date_time = datetime.strptime(task.due_date_time, '%Y-%m-%dT%H:%M')
        return render(request , 'admin_task.html',{'task': task, 'messages': messages}, status=http_status)
        
    @login_required
    @require_http_methods(['POST'])
    def delete_task( request, task_id=None ):
        messages={}
        if request.method == 'POST':            
            try:
                task = Task.objects.get(pk=task_id)                 
            except ObjectDoesNotExist:
                messages['title'] = {'type':'danger','text':'Task non-existent'}
                http_status = 400                 
            else:                            
                if task.user.id != request.user.id:
                    messages['title'] = {'type':'danger','text':'Task not accessible'}
                    http_status = 403                    
                else:
                    task.delete()
                    messages['title'] = {'type':'success','text':'Task deleted'}
                    http_status = 201            
        else:
            messages['title'] = {'type':'danger','text':'Method not permitted'}
        request.session['feedback_message_type'] = messages['title']['type']
        request.session['feedback_message_text'] = messages['title']['text']        
        return redirect('show_user_tasks')
        
    
    @login_required
    @require_http_methods(['GET'])
    def add_task( request ):
        messages = {}
        task = Task(name = 'Unnamed task ' + str(random.randrange(1000, 99999)),
                    due_date_time = datetime.now( timezone.utc ),
                    status = 'T', user = request.user)
        task.save()
        http_status = 302
        
        #request.session['current_process'] = 'add_task'
        #return redirect('admin_task', task_id = task.id )
       
        messages['title'] = {'type':'success', 'text':'New task created, complete it to finish'}
        task.name = ''
        task.due_date_time = ''
        
        form_fields = ['name', 'description', 'status', 'comment', 'due_date_time']
        for field in form_fields:
            messages[field] = {'texts':[], 'input_css_class':'', 'message_css_class':'d-none'} 
        return render(request , 'admin_task.html',{'task': task, 'messages': messages}, status = http_status) 



        
