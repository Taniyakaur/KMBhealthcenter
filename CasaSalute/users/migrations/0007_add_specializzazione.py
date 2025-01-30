# filepath: /Users/taniyakaur/Documents/GitHub/Project/CasaSalute/users/migrations/0007_add_specializzazione.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_specializzazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='specializzazione',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]