import uuid
from django.db import migrations, models


def generate_uuids(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    for book in Book.objects.all():
        book.uuid = uuid.uuid4()
        book.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_book_purchase_link'),
    ]

    # Perform migration in 3 steps so it is compatible with SQLite for development
    operations = [
        
        # Add the uuid field with null=True so the rows do not need a value for it yet
        migrations.AddField(
            model_name='book',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        
        # Generate the unique uuids for each row
        migrations.RunPython(generate_uuids),
        
        # Add unique constraint to uuid field for each row
        migrations.AlterField(
            model_name='book',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]