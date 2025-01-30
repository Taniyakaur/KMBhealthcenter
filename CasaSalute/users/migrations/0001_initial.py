from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Paziente',
            fields=[
                ('username', models.CharField(max_length=150, unique=True, primary_key=True)),
                ('codice_sanitario', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('nome', models.CharField(max_length=255)),
                ('cognome', models.CharField(max_length=255)),
                ('data_di_nascita', models.DateField(null=True, blank=True)),
                ('indirizzo', models.TextField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('username', models.CharField(max_length=150, unique=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('nome', models.CharField(max_length=255)),
                ('cognome', models.CharField(max_length=255)),
                ('data_di_nascita', models.DateField(null=True, blank=True)),
                ('specializzazione', models.CharField(max_length=255, null=True, blank=True)),
                ('telefono', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(null=True, blank=True)),
                ('pazienti_convenzionati', models.ManyToManyField('Paziente', related_name='medici_convenzionati', blank=True)),
                ('medici_sostituibili', models.ManyToManyField('self', symmetrical=False, related_name='medici_sostituti', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Infermiere',
            fields=[
                ('username', models.CharField(max_length=150, unique=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('nome', models.CharField(max_length=255)),
                ('cognome', models.CharField(max_length=255)),
                ('data_di_nascita', models.DateField(null=True, blank=True)),
                ('telefono', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Segreteria',
            fields=[
                ('username', models.CharField(max_length=150, unique=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('nome', models.CharField(max_length=255)),
                ('cognome', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(null=True, blank=True)),
            ],
        ),
    ]