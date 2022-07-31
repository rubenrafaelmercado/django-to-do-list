from list_admin.tests.faker_providers import TaskFakerProvider
from .factories import TaskFactory
from .password import TEST_PASSWORD
import pytest, uuid, factory
from list_admin.models import Task
from ddf import G
from faker import Faker
from datetime import datetime, timedelta, timezone

#I must improve this 2 lines
fake = Faker()
fake.add_provider(TaskFakerProvider)


@pytest.fixture
def get_password():
    def create_password():
        return TEST_PASSWORD
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
def make_dynamic_task( make_user):
    """It returns a function to make a automatic fake task
    according to model configuration or received kwargs.
    It doesn't consider validation restrictions.
    It should use make_user() to obtain a known user password to can test the login    
    """
    def create_task(**kwargs):
        if 'user' not in kwargs:            
            kwargs['user'] = make_user()
        task = G(Task, **kwargs)        
        return task
    return create_task

    
@pytest.fixture
def make_fake_task(db, make_user):
    """It returns a function to make a automatic fake task
    according to faker configuration or received kwargs.
    The faker should consider validation restrictions.
    It should use make_user() to obtain a known user password to can test the login    
    """
    def create_fake_task(**kwargs):
        new_due_date_time = datetime.now( timezone.utc ) + timedelta(minutes = 180)
        if 'user' not in kwargs:            
            user = make_user()
        return Task.objects.create(
            name=fake.task_name(),
            status=fake.task_status(),            
            due_date_time=new_due_date_time,
            description='Description X',
            comment='Comment X',
            user=user
            )
    return create_fake_task
    

