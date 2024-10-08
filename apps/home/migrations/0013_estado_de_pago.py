# Generated by Django 5.0.4 on 2024-09-03 10:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_asignacion_empleado_contratista_tarea_financiera_aec_costo_real_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ESTADO_DE_PAGO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EP_CNUMERO', models.CharField(max_length=20, unique=True, verbose_name='Número de estado de pago')),
                ('EP_FFECHA', models.DateField(verbose_name='Fecha de estado de pago')),
                ('EP_CESTADO', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('RECHAZADO', 'Rechazado')], max_length=20, verbose_name='Estado')),
                ('EP_NTOTAL', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Total')),
                ('EP_COBSERVACIONES', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('EP_FFECHA_CREACION', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('EP_FFECHA_MODIFICACION', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('EP_CESTADO_PAGO', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PARCIAL', 'Parcial'), ('COMPLETO', 'Completo')], default='PENDIENTE', max_length=20, verbose_name='Estado de pago')),
                ('EP_NMONTO_PAGADO', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Monto pagado')),
                ('EP_FFECHA_ULTIMO_PAGO', models.DateField(blank=True, null=True, verbose_name='Fecha del último pago')),
                ('EP_CUSUARIO_CREADOR', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estados_de_pago_creados', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('EP_CUSUARIO_MODIFICADOR', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estados_de_pago_modificados', to=settings.AUTH_USER_MODEL, verbose_name='Usuario modificador')),
                ('EP_PROYECTO', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados_de_pago', to='home.proyecto_cliente', verbose_name='Proyecto cliente')),
            ],
            options={
                'verbose_name': 'Estado de Pago',
                'verbose_name_plural': 'Estados de Pago',
                'db_table': 'ESTADO_DE_PAGO',
            },
        ),
    ]
