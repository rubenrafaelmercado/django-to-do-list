import factory
from list_admin.models import Task
from .faker_providers import TaskFakerProvider
from .password import TEST_PASSWORD
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker
from datetime import datetime, timedelta, timezone

#I must improve this 2 lines
fake = Faker()
fake.add_provider(TaskFakerProvider)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = fake.first_name()    
    password = make_password(TEST_PASSWORD)

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task
    name=fake.task_name()
    status=fake.task_status()
    due_date_time=datetime.now( timezone.utc ) + timedelta(minutes = 60)
    description='Description X'
    comment='Comment X'    
    user=factory.SubFactory(UserFactory)

               
    






