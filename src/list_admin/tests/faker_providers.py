#from faker import Faker
from faker.providers import BaseProvider
import random
#from .task_statuses import TASK_STATUSES

#fake = Faker()

class TaskFakerProvider (BaseProvider):
    
    def task_name(self):
        return f'Task {str(random.randrange(1000, 99999))}'
        
    #def statusFaker():

