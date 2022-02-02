
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
        #self.fields['user'].widget.attrs.update('hidden', '1')        

    class Meta:
        fields = ['name', 'descrption', 'status', 'comment', 'user', 'due_date_time']


class TaskAdminForm( forms.Form ):
    name = forms.CharField(max_length=50)    
    description = forms.CharField(max_length=300)
    status = forms.ChoiceField(choices=TASK_STATUSES)
    comment = forms.CharField(max_length=400)    
    due_date_time = forms.DateTimeField()
    utc_offset_minutes = forms.IntegerField()

    def __init__(self, task, user, *args, **kwargs):
        super(TaskAdminForm, self).__init__(*args, **kwargs)
        self.user = user
        self.task = task
      
    '''
    name: largo, no vacío,  no igual nombre con To do o In progress 
    status: T,D,P,C
    descripción y comentario: largo
    due: no vacío, posterior a fecha de creación
    '''

    def clean_name(self):
        data = self.cleaned_data["name"]        
        if len(data) < 3 or len(data) > 50:
            raise ValidationError('Name should be from 2 up to 50 characters')        
        repeatedTask = Task.objects.filter(user=self.user) \
                     & Task.objects.filter(name=data) \
                     & ( Task.objects.filter(status='P') | Task.objects.filter(status='T') ) \
                     & Task.objects.filter(~Q(id=self.task.id))
        if len( repeatedTask ) >= 1:
            raise ValidationError('There is other task with same name "to do" or "in progress"')
        return data

    def clean_description(self):
        data = self.cleaned_data["description"]
        if len(data) == 1 or len(data) == 2 or len(data) > 300:
            raise ValidationError('Name should be from 2 up to 300 characters')              
        return data

    def clean_comment(self):
        data = self.cleaned_data["comment"]
        if len(data) == 1 or len(data) == 2 or len(data) > 400:
            raise ValidationError('Name should be from 2 up to 400 characters')
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
            raise ValidationError('Due date should not be empty')

        if data < self.task.created_date:
            raise ValidationError('Due date and time should be after current date and time')
        return data


    


    '''
    def get_form_options( self ):
        
        form_options = {}
        form_options['dict'] = {'member': {}, 'book': {} }
        form_options['list'] = {'member': [], 'book': [] }
        
        members = Member.objects.filter(status='A')
        for member in members:
            form_options['list']['member'].append( { 'id' : member.id, 'value' : member.name } )
            form_options['dict']['member'][member.id] = { 'id' : member.id , 'value' : member.name }             
        
        books = Book.objects.filter(status='A')
        for book in books:            
            form_options['list']['book'].append( { 'id' : book.id, 'value' : book.name } )
            form_options['dict']['book'][book.id] = { 'id' : book.id , 'value' : book.name }        

        return form_options
       
    '''

    '''
    def clean(self):
        cleaned_data = super().clean()
        
        utc_offset_minutes = cleaned_data.get('utc_offset_minutes')
        due_date = cleaned_data.get('due_date')
        due_date = due_date + timedelta(minutes = utc_offset_minutes)
        now = datetime.now()

        #now = datetime.now(timezone.utc)            
        #tz = pytz.timezone('UTC')
        #due_date = make_aware(due_date, pytz.timezone('UTC'))
        
        if due_date <= now:
            message = 'Due time must be after current time'
            self.add_error('due_date', message)
        

        if due_date == '':     
            message = 'Due time was not informated'
            self.add_error('due_date', message)
    
        return due_date
    
        
    def clean_book(self):
        data = self.cleaned_data["book"]
        
        try:
            book = Book.objects.get(pk = data)
        except Book.DoesNotExist:
            raise ValidationError('Book identification is not valid')
        
        if book.status != 'A':
            raise ValidationError('Book is not available')
        
        if data == '':
            raise ValidationError('Book identification was not provided')

        return data

    def clean_member(self):
        
        data = self.cleaned_data["member"]
        
        if data == "":
            raise ValidationError('Member identfication was not provided')
                
        try:
            member = Member.objects.get(pk = data)
        except Member.DoesNotExist:
            raise ValidationError('Member identification is not valid')
        
        if member.status != 'A':
            raise ValidationError('Member has no "Activo" status')
        
        return data

    '''
    
    def save(self, commit=True, taskToUpdate=None):

        for field in self:
            setattr(taskToUpdate,field.html_name, field.value())        

        if commit:
            taskToUpdate.save()
        
        return taskToUpdate
    