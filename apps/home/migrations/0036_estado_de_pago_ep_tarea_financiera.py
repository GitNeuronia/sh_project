# Generated by Django 5.0.4 on 2024-09-12 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20240910_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado_de_pago',
            name='EP_TAREA_FINANCIERA',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estados_de_pago', to='home.tarea_financiera', verbose_name='Tarea financiera'),
        ),
    ]
