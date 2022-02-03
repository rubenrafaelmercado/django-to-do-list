from .task_statuses import TASK_STATUSES
from .models import Task
from django.forms import ModelForm
from django import forms
from datetime import datetime, timezone, timedelta
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from django.db.models import Q


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    class Meta:
        fields = ['name', 'descrption', 'status', 'comment', 'user', 'due_date_time']

class TaskAdminForm( forms.Form ):
    name = forms.CharField(max_length=50)    
    description = forms.CharField(max_length=300, required=False)
    status = forms.ChoiceField(choices=TASK_STATUSES)
    comment = forms.CharField(max_length=400, required=False)    
    due_date_time = forms.DateTimeField()
    #utc_offset_minutes = forms.IntegerField(required=False)

    def __init__(self, task, user, *args, **kwargs):
        super(TaskAdminForm, self).__init__(*args, **kwargs)
        self.user = user
        self.task = task
          
    def clean_name(self):
        data = self.cleaned_data["name"]        
        if len(data) < 2 or len(data) > 50:
            raise ValidationError('Name should be from 2 up to 50 characters')        
                
        if self.task.id:
            repeatedTasks = Task.objects.filter(user=self.user) \
                        & Task.objects.filter(name=data) \
                        & ( Task.objects.filter(status='P') | Task.objects.filter(status='T') ) \
                        & Task.objects.filter(~Q(id=self.task.id))
        else:
            epeatedTasks = Task.objects.filter(user=self.user) \
                        & Task.objects.filter(name=data) \
                        & ( Task.objects.filter(status='P') | Task.objects.filter(status='T') )
        if len( repeatedTasks ) >= 1:
            raise ValidationError('There is other task with same name and status "to do" or "in progress"')
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        if  len(data) > 300:
            raise ValidationError('Description should be up to 300 characters')              
        return data

    def clean_comment(self):
        data = self.cleaned_data["comment"]
        if len(data) > 400:
            raise ValidationError('Comment should be to 400 characters')
        return data

    def clean_status(self):
        data = self.cleaned_data["status"]
        notValidStatus = True
        for status in TASK_STATUSES:        
            if status[0] == data: notValidStatus = False 
        if notValidStatus:
            raise ValidationError('Status value is not valid')
        return data

    def clean_due_date_time(self):
        data = self.cleaned_data["due_date_time"]
        if data == '':
            raise ValidationError('Due date and time should not be empty')
        if data < self.task.created_date:
            raise ValidationError('Due date and time should be after creation date and time')
        return data
    
    def save(self, commit=True, taskToUpdate=None):
        for field in self:
            setattr(taskToUpdate,field.html_name, field.value())
        if commit:
            taskToUpdate.save()
        return taskToUpdate


class UserTasksSearchForm( forms.Form ):
    name = forms.CharField(required=False)    
    description = forms.CharField(required=False)    
    status = forms.CharField(required=False)

    def clean_name(self):
        data = self.cleaned_data["name"]
        if len(data) > 30: data = data[0:30]        
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        if len(data) > 30: data = data[0:30]        
        return data
    
    def clean_status(self):
        data = self.cleaned_data["status"]
        notValidStatus = True
        statuses = TASK_STATUSES + ('A', 'All')
        for status in TASK_STATUSES:        
            if status[0] == data: notValidStatus = False 
        if notValidStatus: data=''
        return data    