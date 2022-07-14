from django.urls import resolve
from urllib.parse import urlparse
from list_admin.models import Task
from list_admin.views import TaskAdmin
from datetime import datetime, timedelta, timezone
from faker import Faker
from faker_providers import TaskFakerProvider
      
import pytest, string, uuid

import random                 # all methods and clasess from random file  | use random.choice()
#from random import choice    # only choice method from random file | use choice()

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

fake = Faker()
fake.add_provider(TaskFakerProvider)

@pytest.fixture
def get_password():
    def create_password():
        return 'a-strong-test-pass'
    return create_password    

@pytest.fixture
def make_user(db, django_user_model, get_password):
    def create_user(**kwargs):
        kwargs['password'] = get_password()
        if 'username' not in kwargs:            
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return create_user


@pytest.fixture
def make_task(db, make_user):
    def create_task(**kwargs):
        if 'user' not in kwargs:            
            kwargs['user'] = make_user()    
        return Task.objects.create(**kwargs)
    return create_task


@pytest.fixture
def make_fake_task(db, make_user):
    def create_fake_task(**kwargs):
        new_due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180)
        if 'user' not in kwargs:            
            user = make_user()
        return Task.objects.create(
            name=fake.task_name(),
            status='T',
            due_date_time=new_due_date_time,
            description='Description X',
            comment='Comment X',
            user=user
            )
    return create_fake_task
    

@pytest.mark.django_db
def test_unauthenticated_user_admin_task_view(client, make_task):
           
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')

    client.login(username='', password='' )

    new_due_date_time = task.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': 'Comment X',
    }
        
    view = {'url_name':'admin_task', 'methods': ['get', 'post'] , 'params':[task.id] }
    
    url = reverse('admin_task', args=[task.id])    
    get_response = client.get(url)
    post_response = client.post( url, new_task_data )    
    assert get_response.status_code == 302 and post_response.status_code == 302


@pytest.mark.django_db
def test_authenticated_authorized_user_admin_task_view(client, make_task, get_password):
    
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')
    
    client.login(username=task.user.username, password=get_password() )
    
    new_due_date_time = task.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }
    
    url = reverse('admin_task', args=[task.id])    
    get_response = client.get(url)
    post_response = client.post( url, new_task_data )    
    assert get_response.status_code == 200 and post_response.status_code == 201


@pytest.mark.django_db
def test_authenticated_authorized_user_admin_task_view_with_faker(client, make_fake_task, get_password):
    
    task = make_fake_task()    
    print(task.name)
    client.login(username=task.user.username, password=get_password() )
    
    new_due_date_time = task.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }
    
    url = reverse('admin_task', args=[task.id])    
    get_response = client.get(url)
    post_response = client.post( url, new_task_data )    
    assert get_response.status_code == 200 and post_response.status_code == 201

"""

@pytest.mark.django_db
def test_authenticated_unauthorized_user_admin_task_view(client, make_task, make_user, get_password):
    user_1 = make_user()
    client.login(username=user_1.username, password=get_password() )
    user_2 = make_user()
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A',
        user = user_2)
    new_due_date_time = task.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }    
    url = reverse('admin_task', args=[task.id])    
    get_response = client.get(url)
    post_response = client.post( url, new_task_data )    
    assert get_response.status_code == 403 and post_response.status_code == 403




@pytest.mark.django_db
def test_authenticated_authorized_user_admin_task_view(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')
    task_user = task.user
    client.login(username=task_user.username, password=get_password() )    
    new_due_date_time = task.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }
    view = {'url_name':'admin_task', 'methods': ['get', 'post'] , 'params':[task.id] }    
    url = reverse(view['url_name'], args=[view['params'][0]])
    get_status = 0
    if 'get' in view['methods']:
        response = client.get(url)
        get_status = response.status_code
    post_status = 0
    if 'post' in view['methods']:
        response = client.post( url, new_task_data )
        post_status = response.status_code
    assert get_status == 200 and post_status == 201





@pytest.mark.django_db
def test_authenticated_authorized_user_validation_error_admin_task_view(client, make_task, get_password, make_user):
    
    user = make_user()

    task_a = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A',
        user = user)
    
    task_x = make_task(
        name =  'Task X',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description X',
        comment =  'Comment X',
        user = user)
    
    client.login(username=task_a.user.username, password=get_password() )    
        
    new_due_date_time = task_a.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')

    invalid_due_date_time = task_a.created_date - timedelta(minutes = 10)
    invalid_due_date_time  = datetime.strftime(invalid_due_date_time , '%Y-%m-%dT%H:%M')

    def get_randon_text( text_long ):
        letters = string.ascii_letters
        return ( ''.join(random.choice(letters) for i in range( text_long )) )
    
    invalid_description_for_long = get_randon_text(301)
    invalid_comment_for_long = get_randon_text(401)
    invalid_name_for_long = get_randon_text(1)
    invalid_status = 'X'

    new_tasks_data =[        
        {'name': invalid_name_for_long,
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task B',
        'status': invalid_status,
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},       
        {'name': 'Task C',
        'status': 'T',
        'due_date_time': invalid_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task D',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': invalid_description_for_long,
        'comment': 'Comment X'},
        {'name': 'Task E',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': invalid_comment_for_long },
        {'name': 'Task X',
        'status': 'P',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': 'Comment X'},
    ]
    
    for new_task_data in new_tasks_data:    
        url = reverse('admin_task', args=[task_a.id])
        response = client.post( url, new_task_data)
        if response.status_code == 201: break   
    assert response.status_code == 400


@pytest.mark.django_db
def test_authenticated_authorized_user_not_validation_error_admin_task_view(client, make_task, make_user, get_password):
    
    user = make_user()

    task_a = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A',
        user = user)
    
    task_x = make_task(
        name =  'Task X',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description X',
        comment =  'Comment X',
        user = user)
    
    client.login(username=task_a.user.username, password=get_password() )    

    task_a.due_date_time = datetime.strftime(task_a.due_date_time, '%Y-%m-%dT%H:%M') 

    new_due_date_time = task_a.created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')

    def get_randon_text( text_long ):
        letters = string.ascii_letters
        return ( ''.join(random.choice(letters) for i in range( text_long )) )
    
    new_description = get_randon_text(300)    
    new_comment = get_randon_text(250)
    new_name = 'Task X'
    new_status = 'C'

    new_tasks_data =[                
        {'name': new_name,
        'status': new_status,
        'due_date_time': task_a.due_date_time,        
        'description': task_a.description,
        'comment': task_a.comment},        
        {'name': task_a.name,
        'status': task_a.status,
        'due_date_time': new_due_date_time,        
        'description': task_a.description,
        'comment': task_a.comment},
        {'name': task_a.name,
        'status': task_a.status,
        'due_date_time': task_a.due_date_time,        
        'description': new_description,
        'comment': task_a.comment},
        {'name': task_a.name,
        'status': task_a.status,
        'due_date_time': task_a.due_date_time,        
        'description': task_a.description,
        'comment': new_comment},
        {'name': task_a.name,
        'status': task_a.status,
        'due_date_time': task_a.due_date_time,        
        'description': task_a.description,
        'comment': task_a.comment},
    ]
    
    for new_task_data in new_tasks_data:    
        url = reverse('admin_task', args=[task_a.id])
        response = client.post( url, new_task_data)
        if response.status_code != 201: break   
    assert response.status_code == 201

@pytest.mark.django_db
def test_authenticated_user_add_task_view(client, make_user, get_password):
    user = make_user()    
    client.login(username=user.username, password=get_password() )    

    url = reverse('add_task', args=[])
    response = client.get(url)
    new_added_task = True
    try:
        task = Task.objects.get(user=user)
    except ObjectDoesNotExist:
        new_added_task = False
    assert response.status_code == 302 and new_added_task

@pytest.mark.django_db
def test_unauthenticated_user_add_task_view(client, make_user):
    user = make_user()    
    client.login(username='', password='' )
    url = reverse('add_task', args=[])
    response = client.get(url)
    new_added_task = True
    try:
        task = Task.objects.get(user=user)
    except ObjectDoesNotExist:
        new_added_task = False
    assert response.status_code == 302 and not new_added_task

@pytest.mark.django_db
def test_authenticated_user_no_tasks_show_user_tasks_view(client, make_user, get_password):   
    user = make_user()    
    client.login(username=user.username, password=get_password() )       
    url = reverse('show_user_tasks')
    response = client.get(url)
    assert response.status_code == 202

pytest.mark.django_db
def test_authenticated_user_show_user_tasks_view(client, make_user, make_task, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')
    task_user = task.user
    client.login(username=task_user.username, password=get_password() )    
    url = reverse('show_user_tasks')
    response = client.get(url)
    assert response.status_code == 200 

#falta
#unauthorized unautenticated
#autenticated unauthorized   
#unauthorized autenticated    



@pytest.mark.django_db
def test_unauthenticated_user_show_user_tasks_view(client):    
    client.login(username='', password='')    
    url = reverse('show_user_tasks')
    response = client.get(url)
    redirect_parsed_url =  urlparse(response.url)
    redirect_url_name = resolve(redirect_parsed_url.path).url_name    
    assert response.status_code == 302 and redirect_url_name == 'login'

@pytest.mark.django_db
def test_authenticated_authorized_user_delete_task_view(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')    
    client.login(username=task.user.username, password=get_password() )
    url = reverse('delete_task', args=[task.id])
    response = client.post(url)
    redirect_parsed_url =  urlparse(response.url)
    redirect_url_name = resolve(redirect_parsed_url.path).url_name
    deleted_task = False
    try:
        task = Task.objects.get(id=task.id)
    except ObjectDoesNotExist:
        deleted_task = True
    assert response.status_code == 302 and deleted_task == True and redirect_url_name == 'show_user_tasks'
    

@pytest.mark.django_db
def test_authenticated_authorized_user_non_existent_task_delete_task_view(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')    
    client.login(username=task.user.username, password=get_password())
    non_existent_task_id = task.id + 1         
    url = reverse('delete_task', args=[non_existent_task_id])
    response = client.post(url)
    redirect_parsed_url =  urlparse(response.url)
    redirect_url_name = resolve(redirect_parsed_url.path).url_name
    assert response.status_code == 302 and redirect_url_name == 'show_user_tasks'

@pytest.mark.django_db
def test_authenticated_authorized_user_non_existent_task_delete_task_action(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')    
    client.login(username=task.user.username, password=get_password())
    non_existent_task_id = task.id + 1    
    with pytest.raises(Exception):
        non_existent_task = Task.objects.get(pk=non_existent_task_id)
        non_existent_task.delete()

@pytest.mark.django_db
def test_authenticated_unauthorized_user_delete_task_view(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')
    new_user = make_user()
    client.login(username=new_user.username, password=get_password())    
    url = reverse('delete_task', args=[task.id])
    response = client.post(url)
    redirect_parsed_url =  urlparse(response.url)
    redirect_url_name = resolve(redirect_parsed_url.path).url_name
    deleted_task = False
    try:
        task = Task.objects.get(id=task.id)
    except ObjectDoesNotExist:
        deleted_task = True
    assert response.status_code == 302 and deleted_task == False and redirect_url_name == 'show_user_tasks'

@pytest.mark.django_db
def test_unauthenticated_authorized_user_delete_task_view(client, make_task, make_user, get_password):
    task = make_task(
        name =  'Task A',
        status =  'T',
        due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180),
        description =  'Description A',
        comment =  'Comment A')    
    client.login(username='', password='' )
    url = reverse('delete_task', args=[task.id])
    response = client.post(url)
    redirect_parsed_url =  urlparse(response.url)
    redirect_url_name = resolve(redirect_parsed_url.path).url_name
    deleted_task = False
    try:
        task = Task.objects.get(id=task.id)
    except ObjectDoesNotExist:
        deleted_task = True
    assert response.status_code == 302 and deleted_task == False and redirect_url_name == 'login'


"""