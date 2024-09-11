# Generated by Django 3.2.6 on 2024-09-09 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20240909_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='acta_reunion',
            name='AR_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actas_reunion', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_contratista_tarea_financiera',
            name='AEC_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_financiera_moneda1', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_contratista_tarea_general',
            name='AEC_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_general_moneda1', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_contratista_tarea_ingenieria',
            name='AEC_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_ingenieria_moneda1', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_tarea_financiera',
            name='AE_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_financiera_moneda2', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_tarea_general',
            name='AE_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_general', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_empleado_tarea_ingenieria',
            name='AE_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_ingenieria', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_recurso_tarea_financiera',
            name='ART_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_recurso_financiera', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_recurso_tarea_general',
            name='ART_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_recurso_general', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='asignacion_recurso_tarea_ingenieria',
            name='ART_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asignaciones_recurso_ingenieria', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='boleta_garantia',
            name='BG_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boletas_garantia', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='contrato_cliente',
            name='CC_MONEDA',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contratos', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='CO_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cotizaciones_moneda', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='estado_de_pago',
            name='EP_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='estados_de_pago_moneda', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='etapa',
            name='ET_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etapas', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='factura',
            name='FA_MONEDA',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='facturas', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='orden_venta',
            name='OV_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordenes_venta_moneda', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='proyecto_cliente',
            name='PC_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proyectos_cliente', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='tarea_financiera',
            name='TF_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tareas_financieras', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='tarea_general',
            name='TG_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tareas_generales', to='home.moneda', verbose_name='Moneda'),
        ),
        migrations.AddField(
            model_name='tarea_ingenieria',
            name='TI_MONEDA',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tareas_ingenieria', to='home.moneda', verbose_name='Moneda'),
        )
    ]
