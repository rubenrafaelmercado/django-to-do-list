from .models import Task
from .views import TaskAdmin
from datetime import datetime, timedelta, timezone
import pytest, random, string, uuid
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

@pytest.fixture
def password():
   return 'a-strong-test-pass'

@pytest.fixture
def user(db, django_user_model, password):
    def make_user(**kwargs):
        kwargs['password'] = password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def tasks(db, user):      
    task_objects = []   
    now = datetime.now( timezone.utc )    
    now_plus_3_hours = now + timedelta(minutes = 180)    
    user = user()    
    tasks_data = [ 
        { 
        'name': 'Task A',
        'status': 'T',
        'due_date_time': now_plus_3_hours,
        'description': 'Description A',
        'comment': 'Comment A',
        'user':user},
        { 
        'name': 'Task B',
        'status': 'P',
        'due_date_time': now_plus_3_hours,
        'description': 'Description B',
        'comment': 'Comment B',
        'user':user},
        { 
        'name': 'Task C',
        'status': 'D',
        'due_date_time': now_plus_3_hours,
        'description': 'Description C',
        'comment': 'Comment C',
        'user':user},
        { 
        'name': 'Task D',
        'status': 'C',
        'due_date_time': now_plus_3_hours,
        'description': 'Description D',
        'comment': 'Comment D',
        'user':user},
        { 
        'name': 'Task E',
        'status': 'T',
        'due_date_time': now_plus_3_hours,
        'description': 'Description E',
        'comment': 'Comment E',
        'user':user}
    ]
    for task_data in tasks_data:        
        task_objects.append( Task.objects.create(**task_data ) )
    return task_objects

@pytest.mark.django_db
def test_unauthenticated_user_admin_task_view(client, tasks):
    new_due_date_time = tasks[0].created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': 'Comment X',
    }
    view = {'url_name':'admin_task', 'methods': ['get', 'post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    get_status = 0
    if 'get' in view['methods']:
        response = client.get(url)
        get_status = response.status_code
    post_status = 0
    if 'post' in view['methods']:
        response = client.post( url, new_task_data )
        post_status = response.status_code
    assert get_status == 302 and post_status == 302

@pytest.mark.django_db
def test_authenticated_unauthorized_user_admin_task_view(client, tasks, user, password):
    new_user = user()
    client.login(username=new_user.username, password=password )
    new_due_date_time = tasks[0].created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }
    view = {'url_name':'admin_task', 'methods': ['get', 'post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    get_status = 0
    if 'get' in view['methods']:
        response = client.get(url)
        get_status = response.status_code
    post_status = 0
    if 'post' in view['methods']:
        response = client.post( url, new_task_data )
        post_status = response.status_code
    assert get_status == 403 and post_status == 403

@pytest.mark.django_db
def test_authenticated_authorized_user_admin_task_view(client, tasks, user, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password )    
    new_due_date_time = tasks[0].created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_task_data = {
        'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X',
    }
    view = {'url_name':'admin_task', 'methods': ['get', 'post'] , 'params':[tasks[0].id] }    
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
def test_authenticated_authorized_user_validation_error_admin_task_view(client, tasks, user, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password )    
    new_due_date_time = tasks[0].created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    invalid_new_due_date_time = datetime.strftime(tasks[0].created_date, '%Y-%m-%dT%H:%M')
    def get_randon_text( text_long ):
        letters = string.ascii_letters
        return ( ''.join(random.choice(letters) for i in range( text_long )) )
    invalid_description_for_long = get_randon_text(301)
    invalid_comment_for_long = get_randon_text(401)
    new_tasks_data =[
        {'name': 'Task B',
        'status': 'T',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task E',
        'status': 'P',
        'due_date_time': new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task C',
        'status': 'T',
        'due_date_time': invalid_new_due_date_time,        
        'description': 'Description X',
        'comment': 'Comment X'},
        {'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': invalid_description_for_long,
        'comment': 'Comment X'},
        {'name': 'Task Y',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': invalid_comment_for_long },
        {'name': 'B',
        'status': 'P',
        'due_date_time': new_due_date_time,
        'description': 'Description X',
        'comment': 'Comment X'},
    ]
    view = {'url_name':'admin_task', 'methods': ['post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])    
    for new_task_data in new_tasks_data:    
        response = client.post( url, new_task_data)
        if response.status_code != 400: break   
    assert response.status_code == 400 

    for new_task_data in new_tasks_data:    
        response = client.post( url, new_task_data)
        if response.status_code != 400: break   

@pytest.mark.django_db
def test_authenticated_authorized_user_not_validation_error_admin_task_view(client, tasks, user, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password )
    new_due_date_time = tasks[0].created_date + timedelta(minutes = 10)
    new_due_date_time = datetime.strftime(new_due_date_time, '%Y-%m-%dT%H:%M')
    new_tasks_data =[
        {'name': 'Task B',
        'status': 'D',
        'due_date_time': new_due_date_time,        
        'description': 'Description B',
        'comment': 'Comment B'},
        {'name': 'Task Y',
        'status': 'P',
        'due_date_time': new_due_date_time,        
        'description': 'Description Y',
        'comment': 'Comment Y'},
        {'name': 'Task Z',
        'status': 'P',
        'due_date_time': new_due_date_time,
        'description': 'Description Z',
        'comment': 'Comment Z'},
        {'name': 'Task X',
        'status': 'T',
        'due_date_time': new_due_date_time,
        'description': 'Description M',
        'comment': 'Comment M'},
        {'name': 'Task Y',
        'status': 'D',
        'due_date_time': new_due_date_time,
        'description': 'Description Y',
        'comment': 'Comment Y'},
        {'name': 'Task E ',
        'status': 'C',
        'due_date_time': new_due_date_time,
        'description': 'Description E',
        'comment': 'Comment E'},
    ]
    view = {'url_name':'admin_task', 'methods': ['post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    for new_task_data in new_tasks_data:    
        response = client.post( url, new_task_data)
        if response.status_code != 201: break                
    assert response.status_code == 201

@pytest.mark.django_db
def test_authenticated_user_add_task_view(client, user, password):
    new_user = user()    
    client.login(username=new_user.username, password=password )    
    view = {'url_name':'add_task', 'methods': ['get'] , 'params':[] }    
    url = reverse(view['url_name'])
    response = client.get(url)
    new_task = True
    try:
        task = Task.objects.get(user=new_user)
    except ObjectDoesNotExist:
        new_task = False
    assert response.status_code == 302 and new_task == True

@pytest.mark.django_db
def test_unauthenticated_user_add_task_view(client, user):
    new_user = user()
    view = {'url_name':'add_task', 'methods': ['get'] , 'params':[] }    
    url = reverse(view['url_name'])
    response = client.get(url)
    new_task = True
    try:
        task = Task.objects.get(user=new_user)
    except ObjectDoesNotExist:
        new_task = False
    assert response.status_code == 302 and new_task == False

@pytest.mark.django_db
def test_authenticated_user_no_tasks_list_user_tasks_view(client, user, password):
    new_user = user()    
    client.login(username=new_user.username, password=password )    
    view = {'url_name':'show_user_tasks', 'methods': ['get'] , 'params':[] }    
    url = reverse(view['url_name'])
    response = client.get(url)
    assert response.status_code == 202


pytest.mark.django_db
def test_authenticated_user_list_user_tasks_view(client, user, tasks, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password )
    view = {'url_name':'show_user_tasks', 'methods': ['get'] , 'params':[] }    
    url = reverse(view['url_name'])
    response = client.get(url)
    assert response.status_code == 200 

@pytest.mark.django_db
def test_unauthenticated_user_list_user_tasks_view(client, user, password):
    new_user = user()        
    view = {'url_name':'show_user_tasks', 'methods': ['get'] , 'params':[] }    
    url = reverse(view['url_name'])
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_authenticated_authorized_user_delete_task_view(client, tasks, user, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password )
    view = {'url_name':'delete_task', 'methods': ['post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    response = client.post(url)
    deleted_task = False
    try:
        task = Task.objects.get(id=view['params'][0])
    except ObjectDoesNotExist:
        deleted_task = True
    assert response.status_code == 302 and deleted_task == True
    

@pytest.mark.django_db
def test_authenticated_authorized_user_non_existent_task_delete_task_view(client, tasks, user, password):
    task_user = tasks[0].user
    client.login(username=task_user.username, password=password)
    non_existent_task_id = len(tasks) + 1    
    view = {'url_name':'delete_task', 'methods': ['post'] , 'params':[non_existent_task_id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    response = client.post(url)
    non_existent_task = False
    try:
        task = Task.objects.get(id=non_existent_task_id)
    except ObjectDoesNotExist:
        non_existent_task = True
    assert response.status_code == 302 and non_existent_task == True

@pytest.mark.django_db
def test_authenticated_unauthorized_user_delete_task_view(client, tasks, user, password):
    new_user = user()
    client.login(username=new_user.username, password=password)    
    view = {'url_name':'delete_task', 'methods': ['post'] , 'params':[tasks[0].id] }
    url = reverse(view['url_name'], args=[view['params'][0]])
    response = client.post(url)
    deleted_task = False
    try:
        task = Task.objects.get(id=view['params'][0])
    except ObjectDoesNotExist:
        deleted_task = True
    assert response.status_code == 302 and deleted_task == False





