# Generated by Django 5.2.1 on 2025-05-20 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apl', '0007_servicio_mostrar_boton_consulta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='mostrar_boton_consulta',
        ),
    ]
