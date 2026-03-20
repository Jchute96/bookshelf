import uuid
from django.db import migrations, models


def generate_uuids(apps, schema_editor):
    BookList = apps.get_model('lists', 'BookList')
    for booklist in BookList.objects.all():
        booklist.uuid = uuid.uuid4()
        booklist.save(update_fields=['uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]
    
    # Perform migration in 3 steps so it is compatible with SQLite

    operations = [
        
        # Add the uuid field with null=True so the rows do not need a value for it yet
        migrations.AddField(
            model_name='booklist',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        
        # Generate the unique uuids for each row
        migrations.RunPython(generate_uuids),
        
        # Add unique constraint to uuid field for each row
        migrations.AlterField(
            model_name='booklist',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
