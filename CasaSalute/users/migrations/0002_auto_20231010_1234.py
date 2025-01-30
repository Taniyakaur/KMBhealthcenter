from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # Remove this AddField operation since the column already exists
        # migrations.AddField(
        #     model_name='medico',
        #     name='specializzazione',
        #     field=models.CharField(max_length=255, null=True, blank=True),
        # ),
    ]