# Generated by Django 5.1 on 2024-09-06 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_proyecto_cliente_pc_npresupuesto_moneda_extranjera_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto_cliente',
            name='PC_NPRESUPUESTO_MONEDA_EXTRANJERA',
        ),
    ]
