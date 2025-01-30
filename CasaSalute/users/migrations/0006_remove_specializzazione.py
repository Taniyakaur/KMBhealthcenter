from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_infermiere_indirizzo_infermiere_reparto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medico',
            name='specializzazione',
        ),
    ]