from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20231010_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='data_di_nascita',
            field=models.DateField(null=True, blank=True, default=django.utils.timezone.now),
        ),
    ]