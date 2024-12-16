# Generated by Django 5.1.4 on 2024-12-16 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pruebaZoo', '0002_persona_boleteria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Veterinario',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pruebaZoo.persona')),
                ('cedula', models.IntegerField()),
                ('especialialidad', models.CharField(max_length=100, verbose_name='Especialidad')),
                ('chequeo_realizado', models.BooleanField(default=False)),
                ('tratamiento_prescrito', models.BooleanField(default=False)),
            ],
            bases=('pruebaZoo.persona',),
        ),
    ]