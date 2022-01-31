
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):    

    dependencies = [ ('list_admin', '0001_initial') ]
    operations = [  migrations.RenameModel('ListAdmin', 'Task') ]

    
