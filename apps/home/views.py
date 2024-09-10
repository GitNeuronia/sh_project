# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Módulos de Python estándar
import json
import mimetypes
import os
import re
import logging
import base64
import requests
import traceback
from django.conf import settings
from decimal import Decimal
from xhtml2pdf import pisa
from io import BytesIO
# Módulos de Django
from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import FieldError
from django.db import connection
from django.db.utils import DatabaseError
from django.db.models import (
    Avg, Case, Count, DecimalField, ExpressionWrapper, F, Func,
    IntegerField, Q, Sum, Value, When
)
from django.db.models.functions import Coalesce, Least, Cast, Greatest
from django.http import (
    FileResponse, HttpResponse, HttpResponseBadRequest,
    HttpResponseNotFound, HttpResponseRedirect, JsonResponse
)
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.loader import render_to_string, get_template
from django.urls import reverse
from django.utils.encoding import smart_str
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

# Módulos locales
from apps.home.models import *
from .forms import *
from .models import *

logger = logging.getLogger(__name__)


#lista de objetos
model_urls = {
    "REGION": "REGION_UPDATE",
    "PROVINCIA": "PROVINCIA_UPDATE",
    "COMUNA": "COMUNA_UPDATE",
    #"SYSTEM_LOG": "url",
    "PARAMETRO": "PARAMETRO_UPDATE",
    "TIPO_CAMBIO": "TC_UPDATE",
    #"ALERTA": "url",
    "ROL": "ROL_UPDATE",
    "CATEGORIA_PROYECTO": "CATEGORIA_PROYECTO_UPDATE",
    "CATEGORIA_CLIENTE": "CATEGORIA_CLIENTE_UPDATE",
    "TIPO_PROYECTO": "TIPO_PROYECTO_UPDATE",
    "PERMISO": "PERMISO_UPDATE",
    "PERMISO_ROL": "PERMISO_ROL_UPDATE",
    "USUARIO_ROL": "USUARIO_ROL_UPDATE",
    "CLIENTE": "CLIENTE_UPDATE",
    "CONTACTO_CLIENTE": "CONTACTO_CLIENTE_UPDATE",
    "DIRECCION_CLIENTE": "DIRECCION_CLIENTE_UPDATE",
    "PRODUCTO": "PRODUCTO_UPDATE",
    "COTIZACION": "COTIZACION_LISTONE",
    #"COTIZACION_DETALLE": "url",
    "ORDEN_VENTA": "ORDEN_VENTA_LISTONE",
    #"ORDEN_VENTA_DETALLE": "url",
    "FACTURA": "FACTURA_LISTONE",
    #"FACTURA_DETALLE": "url",
    "UNIDAD_NEGOCIO": "UNIDAD_NEGOCIO_UPDATE",
    "PROYECTO_CLIENTE": "PROYECTO_CLIENTE_LISTONE",
    "ETAPA": "ETAPA_UPDATE",
    "ESTADO_DE_PAGO": "EDP_LISTONE",
    #"ESTADO_DE_PAGO_DETALLE": "url",
    "FICHA_CIERRE": "FC_LISTONE",
    #"FICHA_CIERRE_DETALLE": "url",
    "EMPLEADO": "EMPLEADO_UPDATE",
    "EMPLEADO_CONTRATISTA": "EMPLEADO_EXTERNO_UPDATE",
    "TAREA_GENERAL": "TAREA_GENERAL_LISTONE",
    "TAREA_INGENIERIA": "TAREA_INGENIERIA_LISTONE",
    "TAREA_FINANCIERA": "TAREA_FINANCIERA_LISTONE",
    #"ETAPA_ADJUNTO": "url",
    # "ASIGNACION_EMPLEADO_TAREA_INGENIERIA": "url",
    # "ASIGNACION_EMPLEADO_TAREA_FINANCIERA": "url",
    # "ASIGNACION_EMPLEADO_TAREA_GENERAL": "url",
    # "ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA": "url",
    # "ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA": "url",
    # "ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL": "url",
    # "ASIGNACION_RECURSO_TAREA_GENERAL": "url",
    # "ASIGNACION_RECURSO_TAREA_INGENIERIA": "url",
    # "ASIGNACION_RECURSO_TAREA_FINANCIERA": "url",
     "ACTA_REUNION": "ACTA_REUNION_UPDATE",
    #"PROYECTO_ADJUNTO": "url",
    "BOLETA_GARANTIA": "BOLETA_GARANTIA_UPDATE",
    # "TAREA_GENERAL_DEPENDENCIA": "url",
    # "TAREA_FINANCIERA_DEPENDENCIA": "url",
    # "TAREA_INGENIERIA_DEPENDENCIA": "url",
    "QUERY": "QUERY_UPDATE"
}

@login_required(login_url="/login/")
def index(request):
    
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class WeightedAvg(Func):
    function = 'SUM'
    template = '(%(expressions)s) / NULLIF(SUM(%(weight)s), 0)'
    
    def __init__(self, expression, weight, **extras):
        super().__init__(
            expression * weight,
            weight=weight,
            output_field=DecimalField(),
            **extras
        )

def proyecto_index(request):
    fecha_actual = datetime.datetime.now()
    proyectos = PROYECTO_CLIENTE.objects.all()

    # Calcular estadísticas generales
    estadisticas = proyectos.aggregate(
        total_proyectos=Count('id'),
        proyectos_activos=Count('id', filter=~Q(PC_CESTADO__iexact='Cerrado')),
        total_presupuesto=Coalesce(Sum('PC_NPRESUPUESTO'), Decimal('0')),
        total_costo_real=Coalesce(Sum('PC_NCOSTO_REAL'), Decimal('0')),
        promedio_margen=Coalesce(Avg('PC_NMARGEN'), Decimal('0')),
    )

    # Agregar estadísticas de EdP
    estadisticas_edp = ESTADO_DE_PAGO.objects.aggregate(
        total_edp=Coalesce(Sum('EP_NTOTAL'), Decimal('0')),
        total_pagado=Coalesce(Sum('EP_NMONTO_PAGADO'), Decimal('0')),
    )
    estadisticas['total_saldo_edp'] = estadisticas_edp['total_edp'] - estadisticas_edp['total_pagado']

    # Preparar datos para el gráfico y la tabla de proyectos
    proyectos_data = proyectos.annotate(
        alerta_fecha=Case(
            When(PC_FFECHA_FIN_REAL__isnull=True, PC_FFECHA_FIN_ESTIMADA__lt=fecha_actual, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        alerta_costo=Case(
            When(PC_NCOSTO_REAL__gt=F('PC_NCOSTO_ESTIMADO'), then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        porcentaje_avance=Coalesce(
            Avg(
                Case(
                    When(tareas_generales_proyecto__TG_NPROGRESO__isnull=False, 
                            then='tareas_generales_proyecto__TG_NPROGRESO'),
                    When(tareas_ingenieria_proyecto__TI_NPROGRESO__isnull=False, 
                            then='tareas_ingenieria_proyecto__TI_NPROGRESO'),
                    When(tareas_financieras_proyecto__TF_NPROGRESO__isnull=False, 
                            then='tareas_financieras_proyecto__TF_NPROGRESO'),
                    output_field=DecimalField()
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=5, decimal_places=2)
        ),
        alerta_prioridad=Case(
            When(Q(alerta_fecha=1) | Q(alerta_costo=1), then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    ).values(
        'id', 'PC_CCODIGO', 'PC_CNOMBRE', 'PC_CESTADO', 'PC_NPRESUPUESTO', 'PC_NCOSTO_REAL', 
        'PC_NCOSTO_ESTIMADO', 'PC_FFECHA_INICIO', 'PC_FFECHA_FIN_ESTIMADA', 'PC_FFECHA_FIN_REAL', 
        'alerta_fecha', 'alerta_costo', 'porcentaje_avance', 'alerta_prioridad'
    ).order_by('-alerta_prioridad', 'PC_FFECHA_FIN_ESTIMADA')

    # Preparar datos de EdP por proyecto
    proyectos_edp = PROYECTO_CLIENTE.objects.annotate(
        total_edp=Coalesce(Sum('estados_de_pago__EP_NTOTAL'), Decimal('0')),
        pendiente=Coalesce(Sum(Case(
            When(estados_de_pago__EP_CESTADO='PENDIENTE', then=F('estados_de_pago__EP_NTOTAL')),
            default=0,
            output_field=DecimalField()
        )), Decimal('0')),
        aprobado=Coalesce(Sum(Case(
            When(estados_de_pago__EP_CESTADO='APROBADO', then=F('estados_de_pago__EP_NTOTAL')),
            default=0,
            output_field=DecimalField()
        )), Decimal('0')),
        rechazado=Coalesce(Sum(Case(
            When(estados_de_pago__EP_CESTADO='RECHAZADO', then=F('estados_de_pago__EP_NTOTAL')),
            default=0,
            output_field=DecimalField()
        )), Decimal('0')),
        monto_pagado=Coalesce(Sum('estados_de_pago__EP_NMONTO_PAGADO'), Decimal('0'))
    ).annotate(
        porcentaje_pagado=Case(
            When(total_edp=0, then=0),
            default=F('monto_pagado') * 100 / F('total_edp'),
            output_field=DecimalField(max_digits=5, decimal_places=2)
        )
    ).values('PC_CNOMBRE', 'total_edp', 'pendiente', 'aprobado', 'rechazado', 'monto_pagado', 'porcentaje_pagado')

    # Filtrar y preparar datos de proyectos activos
    proyectos_activos = list(proyectos.filter(~Q(PC_CESTADO__iexact='Cerrado')).annotate(
        porcentaje_avance=Coalesce(
            Avg(
                Case(
                    When(tareas_generales_proyecto__TG_NPROGRESO__isnull=False, 
                            then='tareas_generales_proyecto__TG_NPROGRESO'),
                    When(tareas_ingenieria_proyecto__TI_NPROGRESO__isnull=False, 
                            then='tareas_ingenieria_proyecto__TI_NPROGRESO'),
                    When(tareas_financieras_proyecto__TF_NPROGRESO__isnull=False, 
                            then='tareas_financieras_proyecto__TF_NPROGRESO'),
                    output_field=DecimalField()
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=5, decimal_places=2)
        )
    ).values(
        'id', 'PC_CCODIGO', 'PC_CNOMBRE', 'PC_FFECHA_INICIO', 'PC_FFECHA_FIN_ESTIMADA', 
        'PC_NPRESUPUESTO', 'PC_NCOSTO_REAL', 'PC_CESTADO', 'porcentaje_avance'
    ))

    # Convertir las fechas a strings y los Decimales a float
    for proyecto in proyectos_activos:
        if proyecto['PC_FFECHA_INICIO']:
            proyecto['PC_FFECHA_INICIO'] = proyecto['PC_FFECHA_INICIO'].strftime('%Y-%m-%d')
        if proyecto['PC_FFECHA_FIN_ESTIMADA']:
            proyecto['PC_FFECHA_FIN_ESTIMADA'] = proyecto['PC_FFECHA_FIN_ESTIMADA'].strftime('%Y-%m-%d')
        proyecto['PC_NPRESUPUESTO'] = float(proyecto['PC_NPRESUPUESTO'])
        proyecto['PC_NCOSTO_REAL'] = float(proyecto['PC_NCOSTO_REAL'])
        proyecto['porcentaje_avance'] = min(float(proyecto['porcentaje_avance']), 100)

    context = {
        'estadisticas': estadisticas,
        'proyectos': proyectos_data,
        'fecha_actual': fecha_actual,
        'chart_labels': [p['PC_CCODIGO'] for p in proyectos_data],
        'chart_presupuestos': [float(p['PC_NPRESUPUESTO']) for p in proyectos_data],
        'chart_costos_reales': [float(p['PC_NCOSTO_REAL']) for p in proyectos_data],
        'proyectos_activos': json.dumps(proyectos_activos, cls=DecimalEncoder),
        'proyectos_edp': proyectos_edp,
    }

    return render(request, 'home/proyecto_index.html', context)

def api_proyectos_edp(request):
    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        queryset = PROYECTO_CLIENTE.objects.annotate(
            total_edp=Coalesce(Sum('estados_de_pago__EP_NTOTAL'), Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))),
            pendiente=Coalesce(Sum(Case(
                When(estados_de_pago__EP_CESTADO='PENDIENTE', 
                     then=ExpressionWrapper(F('estados_de_pago__EP_NTOTAL'), output_field=DecimalField(max_digits=20, decimal_places=2))),
                default=Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))
            )), Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))),
            aprobado=Coalesce(Sum(Case(
                When(estados_de_pago__EP_CESTADO='APROBADO', 
                     then=ExpressionWrapper(F('estados_de_pago__EP_NTOTAL'), output_field=DecimalField(max_digits=20, decimal_places=2))),
                default=Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))
            )), Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))),
            rechazado=Coalesce(Sum(Case(
                When(estados_de_pago__EP_CESTADO='RECHAZADO', 
                     then=ExpressionWrapper(F('estados_de_pago__EP_NTOTAL'), output_field=DecimalField(max_digits=20, decimal_places=2))),
                default=Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))
            )), Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))),
            monto_pagado=Coalesce(Sum('estados_de_pago__EP_NMONTO_PAGADO'), Value(0, output_field=DecimalField(max_digits=20, decimal_places=2)))
        )

        if search_value:
            queryset = queryset.filter(PC_CNOMBRE__icontains=search_value)

        total_records = queryset.count()
        queryset = queryset[start:start+length]

        data = []
        for proyecto in queryset:
            total_edp = float(proyecto.total_edp)
            monto_pagado = float(proyecto.monto_pagado)
            
            if total_edp > 0:
                porcentaje_pagado = (monto_pagado / total_edp) * 100
            else:
                porcentaje_pagado = 0

            logger.debug(f"Proyecto: {proyecto.PC_CNOMBRE}")
            logger.debug(f"Total EdP: {total_edp}")
            logger.debug(f"Monto Pagado: {monto_pagado}")
            logger.debug(f"Porcentaje Pagado: {porcentaje_pagado:.2f}%")
            logger.debug("--------------------")

            data.append({
                'PC_CNOMBRE': proyecto.PC_CNOMBRE,
                'total_edp': total_edp,
                'pendiente': float(proyecto.pendiente),
                'aprobado': float(proyecto.aprobado),
                'rechazado': float(proyecto.rechazado),
                'monto_pagado': monto_pagado,
                'porcentaje_pagado': round(porcentaje_pagado, 2)
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data
        })

    except Exception as e:
        logger.exception("Error in api_proyectos_edp")
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def crear_log(usuario, accion, descripcion):
    try:
        SYSTEM_LOG.objects.create(
            USER_CREATOR_ID=usuario,
            LG_ACTION=accion,
            LG_DESCRIPTION=descripcion,
            LG_TIMESTAMP=datetime.datetime.now()
        )
    except Exception as e:
        print(f"Error al crear el log: {str(e)}")

def has_auth(user, permission_name):
    try:
        # Get the user's roles
        user_roles = USUARIO_ROL.objects.filter(UR_CUSUARIO=user, UR_BACTIVO=True)
        
        # Check if the user has the ADMIN role
        if user_roles.filter(UR_CROL__RO_CNOMBRE='ADMIN').exists():
            return True
        
        # Check if any of the user's roles have the required permission
        for user_role in user_roles:
            permission_exists = PERMISO_ROL.objects.filter(
                PR_CROL=user_role.UR_CROL,
                PR_CPERMISO__PE_CNOMBRE=permission_name,
                PR_BACTIVO=True,
                PR_CPERMISO__PE_BACTIVO=True
            ).exists()
            
            if permission_exists:
                return True
        
        return False
    except Exception as e:
        print(f"Error checking authorization: {str(e)}")
        return False

def MONEDA_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = MONEDA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/MONEDA/mon_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def MONEDA_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formMONEDA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Moneda', f'Se creó la moneda: {form.instance.MO_CMONEDA}')
                messages.success(request, 'Moneda guardada correctamente')
                return redirect('/mon_listall/')
            else:
                print(f"Form is not valid: {form.errors}")
                
        form = formMONEDA()
        ctx = {
            'form': form
        }
        return render(request, 'home/MONEDA/mon_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def MONEDA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        moneda = MONEDA.objects.get(id=pk)
        if request.method == 'POST':
            form = formMONEDA(request.POST, instance=moneda)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Moneda', f'Se actualizó la moneda: {form.instance.MO_CMONEDA}')
                messages.success(request, 'Moneda actualizada correctamente')
                return redirect('/mon_listall/')
        form = formMONEDA(instance=moneda)
        ctx = {
            'form': form
        }
        return render(request, 'home/MONEDA/mon_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')


def REGION_LISTALL(request):
    if not has_auth(request.user, 'VER_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = REGION.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/REGION/reg_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def REGION_ADDONE(request):
    if not has_auth(request.user, 'ADD_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formREGION(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Región', f'Se creó la región: {form.instance.RG_CNOMBRE}')
                messages.success(request, 'Región guardada correctamente')
                return redirect('/reg_listall/')
                
        form = formREGION()
        ctx = {
            'form': form
        }
        return render(request, 'home/REGION/reg_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def REGION_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        region = REGION.objects.get(id=pk)
        if request.method == 'POST':
            form = formREGION(request.POST, instance=region)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Región', f'Se actualizó la región: {form.instance.RG_CNOMBRE}')
                messages.success(request, 'Región actualizada correctamente')
                return redirect('/reg_listall/')
        form = formREGION(instance=region)
        ctx = {
            'form': form
        }
        return render(request, 'home/REGION/reg_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROVINCIA_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PROVINCIA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PROVINCIA/prov_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROVINCIA_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formPROVINCIA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Provincia', f'Se creó la provincia: {form.instance.PV_CNOMBRE}')
                messages.success(request, 'Provincia guardada correctamente')
                return redirect('/prov_listall/')
        form = formPROVINCIA()
        ctx = {
            'form': form
        }
        return render(request, 'home/PROVINCIA/prov_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROVINCIA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        provincia = PROVINCIA.objects.get(id=pk)
        if request.method == 'POST':
            form = formPROVINCIA(request.POST, instance=provincia)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Provincia', f'Se actualizó la provincia: {form.instance.PV_CNOMBRE}')
                messages.success(request, 'Provincia actualizada correctamente')
                return redirect('/prov_listall/')
        form = formPROVINCIA(instance=provincia)
        ctx = {
            'form': form
        }
        return render(request, 'home/PROVINCIA/prov_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COMUNA_LISTALL(request):
    if not has_auth(request.user, 'VER_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = COMUNA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/COMUNA/com_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COMUNA_ADDONE(request):
    if not has_auth(request.user, 'ADD_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formCOMUNA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Comuna', f'Se creó la comuna: {form.instance.COM_CNOMBRE}')
                messages.success(request, 'Comuna guardada correctamente')
                return redirect('/com_listall/')
        form = formCOMUNA()
        ctx = {
            'form': form
        }
        return render(request, 'home/COMUNA/com_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COMUNA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_UBICACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        comuna = COMUNA.objects.get(id=pk)
        if request.method == 'POST':
            form = formCOMUNA(request.POST, instance=comuna)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Comuna', f'Se actualizó la comuna: {form.instance.COM_CNOMBRE}')
                messages.success(request, 'Comuna actualizada correctamente')
                return redirect('/com_listall/')
        form = formCOMUNA(instance=comuna)
        ctx = {
            'form': form
        }
        return render(request, 'home/COMUNA/com_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PARAMETRO_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PARAMETRO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PARAMETRO/param_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PARAMETRO_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formPARAMETRO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Parámetro', f'Se creó el parámetro: {form.instance.PM_CDESCRIPCION}')
                messages.success(request, 'Parámetro guardado correctamente')
                return redirect('/param_listall/')
        form = formPARAMETRO()
        ctx = {
            'form': form
        }
        return render(request, 'home/PARAMETRO/param_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PARAMETRO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        parametro = PARAMETRO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPARAMETRO(request.POST, instance=parametro)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Parámetro', f'Se actualizó el parámetro: {form.instance.PM_CDESCRIPCION}')
                messages.success(request, 'Parámetro actualizado correctamente')
                return redirect('/param_listall/')
        form = formPARAMETRO(instance=parametro)
        ctx = {
            'form': form
        }
        return render(request, 'home/PARAMETRO/param_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ROL_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = ROL.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/ROL/rol_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ROL_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formROL(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Rol', f'Se creó el rol: {form.instance.RO_CNOMBRE}')
                messages.success(request, 'Rol guardado correctamente')
                return redirect('/rol_listall/')
        form = formROL()
        ctx = {
            'form': form
        }
        return render(request, 'home/ROL/rol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ROL_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        rol = ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formROL(request.POST, instance=rol)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Rol', f'Se actualizó el rol: {form.instance.RO_CNOMBRE}')
                messages.success(request, 'Rol actualizado correctamente')
                return redirect('/rol_listall/')
        form = formROL(instance=rol)
        ctx = {
            'form': form
        }
        return render(request, 'home/ROL/rol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_PROYECTO_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = CATEGORIA_PROYECTO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/CATEGORIA_PROYECTO/catproy_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_PROYECTO_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formCATEGORIA_PROYECTO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Categoría de Proyecto', f'Se creó la categoría de proyecto: {form.instance.CA_CNOMBRE}')
                messages.success(request, 'Categoría de proyecto guardada correctamente')
                return redirect('/catproy_listall/')
        form = formCATEGORIA_PROYECTO()
        ctx = {
            'form': form
        }
        return render(request, 'home/CATEGORIA_PROYECTO/catproy_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_PROYECTO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        categoria_proyecto = CATEGORIA_PROYECTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formCATEGORIA_PROYECTO(request.POST, instance=categoria_proyecto)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Categoría de Proyecto', f'Se actualizó la categoría de proyecto: {form.instance.CA_CNOMBRE}')
                messages.success(request, 'Categoría de proyecto actualizada correctamente')
                return redirect('/catproy_listall/')
        form = formCATEGORIA_PROYECTO(instance=categoria_proyecto)
        ctx = {
            'form': form
        }
        return render(request, 'home/CATEGORIA_PROYECTO/catproy_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_CLIENTE_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = CATEGORIA_CLIENTE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/CATEGORIA_CLIENTE/catcli_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_CLIENTE_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formCATEGORIA_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Categoría de Cliente', f'Se creó la categoría de cliente: {form.instance.CA_CNOMBRE}')
                messages.success(request, 'Categoría de cliente guardada correctamente')
                return redirect('/catcli_listall/')
        form = formCATEGORIA_CLIENTE()
        ctx = {
            'form': form
        }
        return render(request, 'home/CATEGORIA_CLIENTE/catcli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CATEGORIA_CLIENTE_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        categoria_cliente = CATEGORIA_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCATEGORIA_CLIENTE(request.POST, instance=categoria_cliente)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Categoría de Cliente', f'Se actualizó la categoría de cliente: {form.instance.CA_CNOMBRE}')
                messages.success(request, 'Categoría de cliente actualizada correctamente')
                return redirect('/catcli_listall/')
        form = formCATEGORIA_CLIENTE(instance=categoria_cliente)
        ctx = {
            'form': form
        }
        return render(request, 'home/CATEGORIA_CLIENTE/catcli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CLIENTE_MODAL(request, pk):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cliente = get_object_or_404(CLIENTE, id=pk)
        proyectos = PROYECTO_CLIENTE.objects.filter(PC_CNOMBRE=cliente)
        contactos = CONTACTO_CLIENTE.objects.filter(CC_CLIENTE=cliente)
        
        ctx = {
            'cliente': cliente,
            'proyectos': proyectos,
            'contactos': contactos
        }
        return render(request, 'home/CLIENTE/cliente_modal.html', ctx)
    except Exception as e:
        print(f"Error en CLIENTE_MODAL: {str(e)}")
        messages.error(request, f'Error al cargar la información del cliente: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)

def TIPO_PROYECTO_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = TIPO_PROYECTO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/TIPO_PROYECTO/tipoproy_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TIPO_PROYECTO_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formTIPO_PROYECTO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Tipo de Proyecto', f'Se creó el tipo de proyecto: {form.instance.TP_CNOMBRE}')
                messages.success(request, 'Tipo de proyecto guardado correctamente')
                return redirect('/tipoproy_listall/')
        form = formTIPO_PROYECTO()
        ctx = {
            'form': form
        }
        return render(request, 'home/TIPO_PROYECTO/tipoproy_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TIPO_PROYECTO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tipo_proyecto = TIPO_PROYECTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formTIPO_PROYECTO(request.POST, instance=tipo_proyecto)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Tipo de Proyecto', f'Se actualizó el tipo de proyecto: {form.instance.TP_CNOMBRE}')
                messages.success(request, 'Tipo de proyecto actualizado correctamente')
                return redirect('/tipoproy_listall/')
        form = formTIPO_PROYECTO(instance=tipo_proyecto)
        ctx = {
            'form': form
        }
        return render(request, 'home/TIPO_PROYECTO/tipoproy_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_LISTALL(request):
    if not has_auth(request.user, 'VER_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PERMISO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PERMISO/permiso_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_ADDONE(request):
    if not has_auth(request.user, 'ADD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formPERMISO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Permiso', f'Se creó el permiso: {form.instance.PE_CNOMBRE}')
                messages.success(request, 'Permiso guardado correctamente')
                return redirect('/permiso_listall/')
        form = formPERMISO()
        ctx = {
            'form': form
        }
        return render(request, 'home/PERMISO/permiso_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        permiso = PERMISO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPERMISO(request.POST, instance=permiso)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Permiso', f'Se actualizó el permiso: {form.instance.PE_CNOMBRE}')
                messages.success(request, 'Permiso actualizado correctamente')
                return redirect('/permiso_listall/')
        form = formPERMISO(instance=permiso)
        ctx = {
            'form': form
        }
        return render(request, 'home/PERMISO/permiso_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_ROL_LISTALL(request):
    if not has_auth(request.user, 'VER_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PERMISO_ROL.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PERMISO_ROL/permisorol_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_ROL_ADDONE(request):
    if not has_auth(request.user, 'ADD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formPERMISO_ROL(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Permiso de Rol', f'Se creó el permiso de rol: {form.instance.PR_CPERMISO} para el rol: {form.instance.PR_CROL}')
                messages.success(request, 'Permiso de rol guardado correctamente')
                return redirect('/permisorol_listall/')
        form = formPERMISO_ROL()
        ctx = {
            'form': form
        }
        return render(request, 'home/PERMISO_ROL/permisorol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PERMISO_ROL_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        permiso_rol = PERMISO_ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formPERMISO_ROL(request.POST, instance=permiso_rol)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Permiso de Rol', f'Se actualizó el permiso de rol: {form.instance.PR_CPERMISO} para el rol: {form.instance.PR_CROL}')
                messages.success(request, 'Permiso de rol actualizado correctamente')
                return redirect('/permisorol_listall/')
        form = formPERMISO_ROL(instance=permiso_rol)
        ctx = {
            'form': form
        }
        return render(request, 'home/PERMISO_ROL/permisorol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def USUARIO_ROL_LISTALL(request):
    if not has_auth(request.user, 'VER_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = USUARIO_ROL.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/USUARIO_ROL/usuariorol_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def USUARIO_ROL_ADDONE(request):
    if not has_auth(request.user, 'ADD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formUSUARIO_ROL(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Usuario de Rol', f'Se creó el usuario de rol: {form.instance.UR_CUSUARIO} para el rol: {form.instance.UR_CROL}')
                messages.success(request, 'Usuario rol guardado correctamente')
                return redirect('/usuariorol_listall/')
        form = formUSUARIO_ROL()
        ctx = {
            'form': form
        }
        return render(request, 'home/USUARIO_ROL/usuariorol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def USUARIO_ROL_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_AUTORIZACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        usuario_rol = USUARIO_ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formUSUARIO_ROL(request.POST, instance=usuario_rol)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Usuario de Rol', f'Se actualizó el usuario de rol: {form.instance.UR_CUSUARIO} para el rol: {form.instance.UR_CROL}')
                messages.success(request, 'Usuario rol actualizado correctamente')
                return redirect('/usuariorol_listall/')
        form = formUSUARIO_ROL(instance=usuario_rol)
        ctx = {
            'form': form
        }
        return render(request, 'home/USUARIO_ROL/usuariorol_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CLIENTE_LISTALL(request):
    if not has_auth(request.user, 'VER_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = CLIENTE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/CLIENTE/cliente_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CLIENTE_ADDONE(request):
    if not has_auth(request.user, 'ADD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formCLIENTE(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Cliente', f'Se creó el cliente: {form.instance.CL_CNOMBRE}')
                messages.success(request, 'Cliente guardado correctamente')
                return redirect('/cliente_listall/')
        form = formCLIENTE()
        ctx = {
            'form': form
        }
        return render(request, 'home/CLIENTE/cliente_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CLIENTE_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cliente = CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCLIENTE(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Cliente', f'Se actualizó el cliente: {form.instance.CL_CNOMBRE}')
                messages.success(request, 'Cliente actualizado correctamente')
                return redirect('/cliente_listall/')
        form = formCLIENTE(instance=cliente)
        ctx = {
            'form': form
        }
        return render(request, 'home/CLIENTE/cliente_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTACTO_CLIENTE_LISTALL(request):
    if not has_auth(request.user, 'VER_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = CONTACTO_CLIENTE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/CONTACTO_CLIENTE/contactocli_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTACTO_CLIENTE_ADDONE(request):
    if not has_auth(request.user, 'ADD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formCONTACTO_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Contacto de Cliente', f'Se creó el contacto de cliente: {form.instance.CC_CNOMBRE} para el cliente: {form.instance.CC_CLIENTE}')
                messages.success(request, 'Contacto de cliente guardado correctamente')
                return redirect('/contactocli_listall/')
        form = formCONTACTO_CLIENTE()
        ctx = {
            'form': form
        }
        return render(request, 'home/CONTACTO_CLIENTE/contactocli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTACTO_CLIENTE_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        contacto_cliente = CONTACTO_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCONTACTO_CLIENTE(request.POST, instance=contacto_cliente)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Contacto de Cliente', f'Se actualizó el contacto de cliente: {form.instance.CC_CNOMBRE} para el cliente: {form.instance.CC_CLIENTE}')
                messages.success(request, 'Contacto de cliente actualizado correctamente')
                return redirect('/contactocli_listall/')
        form = formCONTACTO_CLIENTE(instance=contacto_cliente)
        ctx = {
            'form': form
        }
        return render(request, 'home/CONTACTO_CLIENTE/contactocli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def DIRECCION_CLIENTE_LISTALL(request):
    if not has_auth(request.user, 'VER_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = DIRECCION_CLIENTE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/DIRECCION_CLIENTE/direccioncli_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def DIRECCION_CLIENTE_ADDONE(request):
    if not has_auth(request.user, 'ADD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formDIRECCION_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Dirección de Cliente', f'Se creó la dirección de cliente: {form.instance.DR_CDIRECCION} para el cliente: {form.instance.DR_CLIENTE}')
                messages.success(request, 'Dirección de cliente guardada correctamente')
                return redirect('/direccioncli_listall/')
        form = formDIRECCION_CLIENTE()
        ctx = {
            'form': form
        }
        return render(request, 'home/DIRECCION_CLIENTE/direccioncli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def DIRECCION_CLIENTE_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        direccion_cliente = DIRECCION_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formDIRECCION_CLIENTE(request.POST, instance=direccion_cliente)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Dirección de Cliente', f'Se actualizó la dirección de cliente: {form.instance.DR_CDIRECCION} para el cliente: {form.instance.DR_CLIENTE}')
                messages.success(request, 'Dirección de cliente actualizada correctamente')
                return redirect('/direccioncli_listall/')
        form = formDIRECCION_CLIENTE(instance=direccion_cliente)
        ctx = {
            'form': form
        }
        return render(request, 'home/DIRECCION_CLIENTE/direccioncli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PRODUCTO_LISTALL(request):
    if not has_auth(request.user, 'VER_PRODUCTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PRODUCTO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PRODUCTO/producto_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PRODUCTO_ADDONE(request):
    if not has_auth(request.user, 'ADD_PRODUCTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formPRODUCTO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Producto', f'Se creó el producto: {form.instance.PR_CNOMBRE}')
                messages.success(request, 'Producto guardado correctamente')
                return redirect('/producto_listall/')
        form = formPRODUCTO()
        ctx = {
            'form': form
        }
        return render(request, 'home/PRODUCTO/producto_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PRODUCTO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PRODUCTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        producto = PRODUCTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPRODUCTO(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Producto', f'Se actualizó el producto: {form.instance.PR_CNOMBRE}')
                messages.success(request, 'Producto actualizado correctamente')
                return redirect('/producto_listall/')
        form = formPRODUCTO(instance=producto)
        ctx = {
            'form': form
        }
        return render(request, 'home/PRODUCTO/producto_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_LISTALL(request):
    if not has_auth(request.user, 'VER_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = EMPLEADO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/EMPLEADO/empleado_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_ADDONE(request):
    if not has_auth(request.user, 'ADD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formEMPLEADO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Empleado', f'Se creó el empleado: {form.instance.EM_CNOMBRE}')
                messages.success(request, 'Empleado guardado correctamente')
                return redirect('/empleado_listall/')
        form = formEMPLEADO()
        ctx = {
            'form': form
        }
        return render(request, 'home/EMPLEADO/empleado_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        empleado = EMPLEADO.objects.get(id=pk)
        if request.method == 'POST':
            form = formEMPLEADO(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Empleado', f'Se actualizó el empleado: {form.instance.EM_CNOMBRE}')
                messages.success(request, 'Empleado actualizado correctamente')
                return redirect('/empleado_listall/')
        form = formEMPLEADO(instance=empleado)
        ctx = {
            'form': form
        }
        return render(request, 'home/EMPLEADO/empleado_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTRATISTA_LISTALL(request):
    if not has_auth(request.user, 'VER_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = CONTRATISTA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/CONTRATISTA/contratista_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTRATISTA_ADDONE(request):
    if not has_auth(request.user, 'ADD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formCONTRATISTA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Contratista', f'Se creó el contratista: {form.instance.CO_CNOMBRE}')
                messages.success(request, 'Contratista guardado correctamente')
                return redirect('/contratista_listall/')
        form = formCONTRATISTA()
        ctx = {
            'form': form
        }
        return render(request, 'home/CONTRATISTA/contratista_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def CONTRATISTA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        contratista = CONTRATISTA.objects.get(id=pk)
        if request.method == 'POST':
            form = formCONTRATISTA(request.POST, instance=contratista)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Contratista', f'Se actualizó el contratista: {form.instance.CO_CNOMBRE}')
                messages.success(request, 'Contratista actualizado correctamente')
                return redirect('/contratista_listall/')
        form = formCONTRATISTA(instance=contratista)
        ctx = {
            'form': form
        }
        return render(request, 'home/CONTRATISTA/contratista_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_EXTERNO_LISTALL(request):
    if not has_auth(request.user, 'VER_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = EMPLEADO_CONTRATISTA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/EMPLEADO_CONTRATISTA/empleado_externo_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_EXTERNO_ADDONE(request):
    if not has_auth(request.user, 'ADD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formEMPLEADO_CONTRATISTA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Empleado Externo', f'Se creó el empleado externo: {form.instance.EC_CNOMBRE}')
                messages.success(request, 'Empleado externo guardado correctamente')
                return redirect('/empleado_externo_listall/')
        form = formEMPLEADO_CONTRATISTA()
        ctx = {
            'form': form
        }
        return render(request, 'home/EMPLEADO_CONTRATISTA/empleado_externo_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EMPLEADO_EXTERNO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PERSONAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        empleado_externo = EMPLEADO_CONTRATISTA.objects.get(id=pk)
        if request.method == 'POST':
            form = formEMPLEADO_CONTRATISTA(request.POST, instance=empleado_externo)
            if form.is_valid():
                empleado = form.save(commit=False)
                empleado.EC_CUSUARIO_MODIFICADOR = request.user
                empleado.save()
                crear_log(request.user, 'Actualizar Empleado Externo', f'Se actualizó el empleado externo: {form.instance.EC_CNOMBRE}')
                messages.success(request, 'Empleado externo actualizado correctamente')
                return redirect('/empleado_externo_listall/')
        else:
            # Asegúrate de que las fechas se carguen correctamente en el formulario
            initial_data = {
                'EC_FFECHA_CONTRATACION': empleado_externo.EC_FFECHA_CONTRATACION.strftime('%Y-%m-%d') if empleado_externo.EC_FFECHA_CONTRATACION else None,
                'EC_CFECHA_NACIMIENTO': empleado_externo.EC_CFECHA_NACIMIENTO.strftime('%Y-%m-%d') if empleado_externo.EC_CFECHA_NACIMIENTO else None,
            }
            form = formEMPLEADO_CONTRATISTA(instance=empleado_externo, initial=initial_data)
        
        ctx = {
            'form': form,
            'empleado_externo': empleado_externo
        }
        return render(request, 'home/EMPLEADO_CONTRATISTA/empleado_externo_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ETAPA_LISTALL(request):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = ETAPA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/ETAPA/etapa_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ETAPA_ADDONE(request):
    if not has_auth(request.user, 'ADD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formETAPA(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Etapa', f'Se creó la etapa: {form.instance.ET_CNOMBRE}')
                messages.success(request, 'Etapa guardada correctamente')
                return redirect('/etapa_listall/')
        form = formETAPA()
        ctx = {
            'form': form
        }
        return render(request, 'home/ETAPA/etapa_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ETAPA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        etapa = ETAPA.objects.get(id=pk)
        if request.method == 'POST':
            form = formETAPA(request.POST, instance=etapa)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Etapa', f'Se actualizó la etapa: {form.instance.ET_CNOMBRE}')
                messages.success(request, 'Etapa actualizada correctamente')
                return redirect('/etapa_listall/')
        form = formETAPA(instance=etapa)
        ctx = {
            'form': form
        }
        return render(request, 'home/ETAPA/etapa_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

#--------------------------------------
#---------------PROYECOS---------------
#--------------------------------------

def PROYECTO_CLIENTE_LISTALL(request):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = PROYECTO_CLIENTE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROYECTO_CLIENTE_ADDONE(request):
    if not has_auth(request.user, 'ADD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    
    try:
        if request.method == 'POST':
            form = formPROYECTO_CLIENTE(request.POST)
           
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.PC_CUSUARIO_CREADOR = request.user
                            
                proyecto.save()
                crear_log(request.user, 'Crear Proyecto de Cliente', f'Se creó el proyecto de cliente: {proyecto.PC_CNOMBRE}')
                messages.success(request, 'Proyecto de cliente guardado correctamente')
                return redirect('/proycli_listall/')
            else:
                # Si el formulario no es válido, imprimir los errores para depuración
                print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo {field}: {error}')
        else:
            form = formPROYECTO_CLIENTE()
        
        ctx = {
            'form': form,
            'state': 'add'
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_addone.html', ctx)
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        messages.error(request, f'Error al procesar la solicitud: {str(e)}')
        return redirect('/')
def PROYECTO_CLIENTE_UPDATE(request, pk, page):
    if not has_auth(request.user, 'UPD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        proyecto = PROYECTO_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formPROYECTO_CLIENTE(request.POST, instance=proyecto)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.PC_CUSUARIO_MODIFICADOR = request.user
                proyecto.save()
                crear_log(request.user, 'Actualizar Proyecto de Cliente', f'Se actualizó el proyecto de cliente: {form.instance.PC_CNOMBRE}')
                messages.success(request, 'Proyecto de cliente actualizado correctamente')
                if page == 1:
                    return redirect('/proycli_listone/'+str(proyecto.id)+'/')
                else:
                    return redirect('/proycli_listall/')
        else:
            # Convertir las fechas a formato de cadena para el formulario
            proyecto.PC_FFECHA_INICIO = proyecto.PC_FFECHA_INICIO.strftime('%Y-%m-%d') if proyecto.PC_FFECHA_INICIO else None
            proyecto.PC_FFECHA_FIN_ESTIMADA = proyecto.PC_FFECHA_FIN_ESTIMADA.strftime('%Y-%m-%d') if proyecto.PC_FFECHA_FIN_ESTIMADA else None
            proyecto.PC_FFECHA_FIN_REAL = proyecto.PC_FFECHA_FIN_REAL.strftime('%Y-%m-%d') if proyecto.PC_FFECHA_FIN_REAL else None
            form = formPROYECTO_CLIENTE(instance=proyecto)
        ctx = {
            'form': form
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROYECTO_CLIENTE_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        proyecto = PROYECTO_CLIENTE.objects.get(id=pk)
        tareas_general = TAREA_GENERAL.objects.filter(TG_PROYECTO_CLIENTE=proyecto)
        tareas_ingenieria = TAREA_INGENIERIA.objects.filter(TI_PROYECTO_CLIENTE=proyecto)
        tareas_financiera = TAREA_FINANCIERA.objects.filter(TF_PROYECTO_CLIENTE=proyecto)
        
        dependencias_general = TAREA_GENERAL_DEPENDENCIA.objects.filter(TD_TAREA_SUCESORA__in=tareas_general)
        dependencias_ingenieria = TAREA_INGENIERIA_DEPENDENCIA.objects.filter(TD_TAREA_SUCESORA__in=tareas_ingenieria)
        dependencias_financiera = TAREA_FINANCIERA_DEPENDENCIA.objects.filter(TD_TAREA_SUCESORA__in=tareas_financiera)        
        
        asignacion_empleado_general = ASIGNACION_EMPLEADO_TAREA_GENERAL.objects.filter(AE_TAREA__in=tareas_general)
        asignacion_empleado_ingenieria = ASIGNACION_EMPLEADO_TAREA_INGENIERIA.objects.filter(AE_TAREA__in=tareas_ingenieria)
        asignacion_empleado_financiera = ASIGNACION_EMPLEADO_TAREA_FINANCIERA.objects.filter(AE_TAREA__in=tareas_financiera)
        
        asignacion_recurso_general = ASIGNACION_RECURSO_TAREA_GENERAL.objects.filter(ART_TAREA__in=tareas_general)
        asignacion_recurso_ingenieria = ASIGNACION_RECURSO_TAREA_INGENIERIA.objects.filter(ART_TAREA__in=tareas_ingenieria)
        asignacion_recurso_financiera = ASIGNACION_RECURSO_TAREA_FINANCIERA.objects.filter(ART_TAREA__in=tareas_financiera)
        
        asignacion_contratista_general = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL.objects.filter(AEC_TAREA__in=tareas_general)
        asignacion_contratista_ingenieria = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA.objects.filter(AEC_TAREA__in=tareas_ingenieria)
        asignacion_contratista_financiera = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA.objects.filter(AEC_TAREA__in=tareas_financiera)
        
        costo_real_proyecto = 0
        horas_reales_proyecto = 0

        # Función auxiliar para comprobar asignaciones en cero
        def tiene_asignacion_cero(tarea, asignaciones_empleado, asignaciones_recurso, asignaciones_contratista):
            return (
                asignaciones_empleado.filter(AE_TAREA=tarea, AE_HORAS_REALES=0).exists() or
                asignaciones_empleado.filter(AE_TAREA=tarea, AE_COSTO_TOTAL=0).exists() or
                asignaciones_recurso.filter(ART_TAREA=tarea, ART_HORAS_REALES=0).exists() or
                asignaciones_recurso.filter(ART_TAREA=tarea, ART_COSTO_TOTAL=0).exists() or
                asignaciones_contratista.filter(AEC_TAREA=tarea, AEC_HORAS_REALES=0).exists() or
                asignaciones_contratista.filter(AEC_TAREA=tarea, AEC_COSTO_TOTAL=0).exists()
            )

        for tarea in tareas_general:
            tarea.TG_NPROGRESO = int(round(float(tarea.TG_NPROGRESO)))
            print(tarea.TG_NPROGRESO)
            tarea.tiene_asignacion_cero = tiene_asignacion_cero(
                tarea, asignacion_empleado_general, asignacion_recurso_general, asignacion_contratista_general
            )
            if tarea.TG_NPROGRESO == 100 and tarea.TG_NDURACION_REAL is not None and tarea.TG_NDURACION_REAL > 0:                
                horas_reales_proyecto += tarea.TG_NDURACION_REAL    

                if asignacion_empleado_general.filter(AE_TAREA=tarea).exists():
                    for asignacion in asignacion_empleado_general.filter(AE_TAREA=tarea):
                        costo_real_proyecto += asignacion.AE_COSTO_TOTAL
                if asignacion_recurso_general.filter(ART_TAREA=tarea).exists():
                    for asignacion in asignacion_recurso_general.filter(ART_TAREA=tarea):
                        costo_real_proyecto += asignacion.ART_COSTO_REAL
                if asignacion_contratista_general.filter(AEC_TAREA=tarea).exists():
                    for asignacion in asignacion_contratista_general.filter(AEC_TAREA=tarea):
                        costo_real_proyecto += asignacion.AEC_COSTO_TOTAL

        for tarea in tareas_ingenieria:
            tarea.TI_NPROGRESO = int(round(float(tarea.TI_NPROGRESO)))
            tarea.tiene_asignacion_cero = tiene_asignacion_cero(
                tarea, asignacion_empleado_ingenieria, asignacion_recurso_ingenieria, asignacion_contratista_ingenieria
            )
            if tarea.TI_NPROGRESO == 100 and tarea.TI_NDURACION_REAL is not None and tarea.TI_NDURACION_REAL > 0:
                horas_reales_proyecto += tarea.TI_NDURACION_REAL
                
                if asignacion_empleado_ingenieria.filter(AE_TAREA=tarea).exists():
                    for asignacion in asignacion_empleado_ingenieria.filter(AE_TAREA=tarea):
                        costo_real_proyecto += asignacion.AE_COSTO_TOTAL
                if asignacion_recurso_ingenieria.filter(ART_TAREA=tarea).exists():
                    for asignacion in asignacion_recurso_ingenieria.filter(ART_TAREA=tarea):
                        costo_real_proyecto += asignacion.ART_COSTO_REAL
                if asignacion_contratista_ingenieria.filter(AEC_TAREA=tarea).exists():
                    for asignacion in asignacion_contratista_ingenieria.filter(AEC_TAREA=tarea):
                        costo_real_proyecto += asignacion.AEC_COSTO_TOTAL

        for tarea in tareas_financiera:
            tarea.TF_NPROGRESO = int(round(float(tarea.TF_NPROGRESO)))
            tarea.tiene_asignacion_cero = tiene_asignacion_cero(
                tarea, asignacion_empleado_financiera, asignacion_recurso_financiera, asignacion_contratista_financiera
            )
            if tarea.TF_NPROGRESO == 100 and tarea.TF_NDURACION_REAL is not None and tarea.TF_NDURACION_REAL > 0:
                horas_reales_proyecto += tarea.TF_NDURACION_REAL
                
                if asignacion_empleado_financiera.filter(AE_TAREA=tarea).exists():
                    for asignacion in asignacion_empleado_financiera.filter(AE_TAREA=tarea):
                        costo_real_proyecto += asignacion.AE_COSTO_TOTAL
                if asignacion_recurso_financiera.filter(ART_TAREA=tarea).exists():
                    for asignacion in asignacion_recurso_financiera.filter(ART_TAREA=tarea):
                        costo_real_proyecto += asignacion.ART_COSTO_REAL
                if asignacion_contratista_financiera.filter(AEC_TAREA=tarea).exists():
                    for asignacion in asignacion_contratista_financiera.filter(AEC_TAREA=tarea):
                        costo_real_proyecto += asignacion.AEC_COSTO_TOTAL
        if horas_reales_proyecto != proyecto.PC_NHORAS_REALES:
            print('horas_reales_proyecto', horas_reales_proyecto)
            print('proyecto.PC_NHORAS_REALES', proyecto.PC_NHORAS_REALES)
            proyecto.PC_NHORAS_REALES = horas_reales_proyecto
            proyecto.save()
        if costo_real_proyecto != proyecto.PC_NCOSTO_REAL:
            print('costo_real_proyecto', costo_real_proyecto)
            print('proyecto.PC_NCOSTO_REAL', proyecto.PC_NCOSTO_REAL)            
            proyecto.PC_NCOSTO_REAL = costo_real_proyecto
            proyecto.save()
        max_costo = max(proyecto.PC_NCOSTO_REAL, proyecto.PC_NCOSTO_ESTIMADO)
        ctx = {
            'proyecto': proyecto,
            'tareas_general': tareas_general,
            'tareas_ingenieria': tareas_ingenieria,
            'tareas_financiera': tareas_financiera,
            'dependencias_general': dependencias_general,
            'dependencias_ingenieria': dependencias_ingenieria,
            'dependencias_financiera': dependencias_financiera,
            'costo_real_proyecto': costo_real_proyecto,
            'horas_reales_proyecto': horas_reales_proyecto,
            'max_costo': max_costo
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_listone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

# ----------PROYECTO MODAL DOCUMENTOS--------------

def PROYECTO_CLIENTE_DOCUMENTOS_MODAL(request, pk):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        proyecto = get_object_or_404(PROYECTO_CLIENTE, id=pk)
        documentos = PROYECTO_ADJUNTO.objects.filter(PA_PROYECTO=proyecto)
        
        form = formPROYECTO_ADJUNTO()
        form.fields['PA_CARCHIVO'].widget.attrs.update({
            'class': 'd-none',
            'id': 'file-upload'
        })
        # Inicializar el campo PA_PROYECTO con el proyecto actual
        # if proyecto:
        #     form.fields['PA_PROYECTO'].initial = proyecto
        #     form.fields['PA_PROYECTO'].widget = forms.HiddenInput()
        # # form.fields['PA_PROYECTO'].initial = proyecto
        # form.fields['PA_PROYECTO'].widget = forms.HiddenInput()
        
        ctx = {
            'proyecto': proyecto,
            'documentos': documentos,
            'form': form
        }
        return render(request, 'home/PROYECTO_CLIENTE/PROYECTO_ADJUNTO/proycli_adjunto_listall.html', ctx)
    except Exception as e:
        print(f"Error en PROYECTO_CLIENTE_DOCUMENTOS_MODAL: {str(e)}")
        messages.error(request, f'Error al cargar la documentación del proyecto: {str(e)}')
        return JsonResponse({'error': str(e)}, status=400)

def PROYECTO_CLIENTE_DOCUMENTOS_MODAL_ADDONE(request, pk):
    if not has_auth(request.user, 'ADD_PROYECTOS_CLIENTES'):
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción'}, status=403)
    
    try:
        proyecto = get_object_or_404(PROYECTO_CLIENTE, id=pk)
        form = formPROYECTO_ADJUNTO(request.POST, request.FILES)
        
        if form.is_valid():
            nuevo_documento = form.save(commit=False)
            nuevo_documento.PA_PROYECTO = proyecto
            nuevo_documento.PA_CUSUARIO_CREADOR = request.user
            nuevo_documento.save()
            
            crear_log(request.user, 'Agregar Documento a Proyecto', f'Se agregó el documento {nuevo_documento.PA_CNOMBRE} al proyecto {proyecto.PC_CNOMBRE}')
            
            return JsonResponse({'success': True, 'message': 'Documento agregado correctamente'})
        else:
            return JsonResponse({'success': False, 'error': 'Formulario inválido', 'errors': form.errors}, status=400)
    
    except Exception as e:
        print(f"Error en PROYECTO_CLIENTE_DOCUMENTOS_MODAL_ADDONE: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def PROYECTO_CLIENTE_DOCUMENTOS_MODAL_UPDATE(request, pk):
    if not has_auth(request.user, 'EDIT_PROYECTOS_CLIENTES'):
        return JsonResponse({'error': 'No tienes permiso para realizar esta acción'}, status=403)
    
    try:
        documento = get_object_or_404(PROYECTO_ADJUNTO, id=pk)
        
        if request.method == 'POST':
            form = formPROYECTO_ADJUNTO(request.POST, request.FILES, instance=documento)
            
            if form.is_valid():
                documento_editado = form.save(commit=False)
                documento_editado.PA_CUSUARIO_MODIFICADOR = request.user
                documento_editado.save()
                
                crear_log(request.user, 'Actualizar Documento de Proyecto', f'Se editó el documento {documento_editado.PA_CNOMBRE} del proyecto {documento_editado.PA_PROYECTO.PC_CNOMBRE}')
                
                return JsonResponse({'success': True, 'message': 'Documento editado correctamente'})
            else:
                return JsonResponse({'success': False, 'error': 'Formulario inválido', 'errors': form.errors}, status=400)
        
        else:  # GET request
            form = formPROYECTO_ADJUNTO(instance=documento)
            return JsonResponse({
                'success': True,
                'documento': {
                    'id': documento.id,
                    'PA_CNOMBRE': documento.PA_CNOMBRE,
                    'PA_CDESCRIPCION': documento.PA_CDESCRIPCION,
                    'PA_CTIPO': documento.PA_CTIPO,
                    'PA_CARCHIVO': documento.PA_CARCHIVO.url if documento.PA_CARCHIVO else None,
                    'PA_CARCHIVO_nombre': documento.PA_CARCHIVO.name if documento.PA_CARCHIVO else None,
                }
            })
    
    except Exception as e:
        print(f"Error en PROYECTO_CLIENTE_DOCUMENTOS_MODAL_UPDATE: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def get_documento(request, documento_id):
    try:
        documento = PROYECTO_ADJUNTO.objects.get(id=documento_id)
        data = {
            'success': True,
            'documento': {
                'PA_CNOMBRE': documento.PA_CNOMBRE,
                'PA_CDESCRIPCION': documento.PA_CDESCRIPCION,
                'PA_CTIPO': documento.PA_CTIPO,
                'PA_CARCHIVO': documento.PA_CARCHIVO.name if documento.PA_CARCHIVO else None,
            }
        }
        return JsonResponse(data)
    except PROYECTO_ADJUNTO.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Documento no encontrado'}, status=404)

def PROYECTO_CLIENTE_DOCUMENTOS_DOWNLOAD(request, documento_id):
    if not has_auth(request.user, 'VER_PROYECTOS'):  # Asumimos que existe esta función de verificación de permisos
        messages.error(request, 'No tienes permiso para descargar este archivo')
        return redirect('/')
    
    try:
        adjunto = get_object_or_404(PROYECTO_ADJUNTO, pk=documento_id)
        
        if not adjunto.PA_CARCHIVO:
            return HttpResponseNotFound('El archivo no existe')

        file_path = adjunto.PA_CARCHIVO.path
        if not os.path.exists(file_path):
            return HttpResponseNotFound('El archivo no existe en el sistema de archivos')

        # Obtener el nombre original del archivo
        original_filename = os.path.basename(adjunto.PA_CARCHIVO.name)
        
        # Determinar el tipo MIME
        content_type, encoding = mimetypes.guess_type(file_path)
        content_type = content_type or 'application/octet-stream'
        
        # Abrir el archivo en modo binario
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type=content_type)
        
        # Configurar los encabezados de la respuesta
        response['Content-Disposition'] = f'attachment; filename="{original_filename}"'
        
        # Añadir el tamaño del archivo al encabezado
        response['Content-Length'] = os.path.getsize(file_path)
        
        return response
    except Exception as e:
        # Registrar el error para debugging        
        return HttpResponseNotFound('Error al descargar el archivo')
# ----------PROYECTO MODAL DOCUMENTOS--------------

#--------------------------------------
#---------------PROYECOS---------------
#--------------------------------------

#--------------------------------------
#----------------TAREAS----------------
#--------------------------------------

# ----------TAREA GENERAL--------------

def TAREA_GENERAL_LISTALL(request):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tareas_generales = TAREA_GENERAL.objects.all()
        ctx = {
            'tareas_generales': tareas_generales
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_GENERAL_ADDONE(request, page):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        form = formTAREA_GENERAL()
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_GENERAL()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_GENERAL()

        if request.method == 'POST':
            form = formTAREA_GENERAL(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TG_CUSUARIO_CREADOR = request.user                                                
                tarea.save()
                crear_log(request.user, 'Crear Tarea General', f'Se creó la tarea general: {tarea.TG_CNOMBRE}')
                # Manejar asignaciones múltiples
                empleados_ids = request.POST.getlist('empleados')
                contratistas_ids = request.POST.getlist('contratistas')                
                recursos_json = request.POST.get('recursos_json')

                # Asignar empleados
                for empleado_id in empleados_ids:
                    id_emp = EMPLEADO.objects.get(id=empleado_id)
                    asignacion = ASIGNACION_EMPLEADO_TAREA_GENERAL(
                        AE_TAREA=tarea,
                        AE_EMPLEADO=id_emp,
                        AE_CESTADO = 'ASIGNADO',
                        AE_CUSUARIO_CREADOR = request.user,
                        AE_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,  
                        AE_FFECHA_FINALIZACION=tarea.TG_FFECHA_FIN_ESTIMADA                      
                    )
                    crear_log(request.user, 'Crear Asignación de Empleado a Tarea General', f'Se creó la asignación de empleado a tarea general: {tarea.TG_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                    asignacion.save()

                # Asignar contratistas
                for contratista_id in contratistas_ids:
                    id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                    asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL(
                        AEC_TAREA=tarea,
                        AEC_EMPLEADO=id_emp,
                        AEC_CESTADO = 'ASIGNADO',
                        AEC_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,
                        AEC_FFECHA_FINALIZACION=tarea.TG_FFECHA_FIN_ESTIMADA,
                        AEC_CUSUARIO_CREADOR=request.user
                    )
                    crear_log(request.user, 'Crear Asignación de Contratista a Tarea General', f'Se creó la asignación de contratista a tarea general: {tarea.TG_CNOMBRE} para el contratista: {id_emp.EC_CNOMBRE}')
                    asignacion.save()

                # Procesar recursos                
                if recursos_json:
                    recursos = json.loads(recursos_json)
                    for recurso in recursos:
                        id_rec = PRODUCTO.objects.get(id=recurso['id'])
                        asignacion = ASIGNACION_RECURSO_TAREA_GENERAL(
                            ART_TAREA=tarea,
                            ART_PRODUCTO=id_rec,
                            ART_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,
                            ART_CUSUARIO_CREADOR=request.user,
                            ART_CANTIDAD=int(float(recurso['cantidad'])),
                            ART_COSTO_UNITARIO=int(float(recurso['costo'])),
                            ART_COSTO_TOTAL = int(float(recurso['costo'])) * int(float(recurso['cantidad']))
                        )
                        crear_log(request.user, 'Crear Asignación de Recurso a Tarea General', f'Se creó la asignación de recurso a tarea general: {tarea.TG_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
                        asignacion.save()

                messages.success(request, 'Tarea general guardada correctamente con las asignaciones seleccionadas')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TG_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_general_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')
        


        ctx = {
            'form': form,
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,
            
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_GENERAL_UPDATE(request, pk, page=1):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_GENERAL.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_GENERAL(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TG_CUSUARIO_MODIFICADOR = request.user
                tarea.save()
                crear_log(request.user, 'Actualizar Tarea General', f'Se actualizó la tarea general: {tarea.TG_CNOMBRE}')
                messages.success(request, 'Tarea general actualizada correctamente')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TG_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_general_listall/')
        else:
            # Asegúrate de que las fechas se carguen correctamente en el formulario
            initial_data = {
                'TG_FFECHA_INICIO': tarea.TG_FFECHA_INICIO.strftime('%Y-%m-%d') if tarea.TG_FFECHA_INICIO else None,
                'TG_FFECHA_FIN_ESTIMADA': tarea.TG_FFECHA_FIN_ESTIMADA.strftime('%Y-%m-%d') if tarea.TG_FFECHA_FIN_ESTIMADA else None,
                'TG_FFECHA_FIN_REAL': tarea.TG_FFECHA_FIN_REAL.strftime('%Y-%m-%d') if tarea.TG_FFECHA_FIN_REAL else None
            }
            form = formTAREA_GENERAL(instance=tarea, initial=initial_data)
        
        ctx = {
            'form': form,
            'tarea': tarea
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_update.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_GENERAL_UPDATE_ASIGNACIONES(request, pk, page):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_GENERAL.objects.get(id=pk)
        idproyecto = tarea.TG_PROYECTO_CLIENTE.id
        proyecto = PROYECTO_CLIENTE.objects.get(id=idproyecto)
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_GENERAL()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_GENERAL()

        # Cargar asignaciones existentes
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_GENERAL.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_GENERAL.objects.filter(ART_TAREA=tarea)

        if request.method == 'POST':
            # Manejar asignaciones múltiples
            empleados_ids = request.POST.getlist('empleados')
            contratistas_ids = request.POST.getlist('contratistas')                
            recursos_json = request.POST.get('recursos_json')

            # Eliminar asignaciones existentes
            ASIGNACION_EMPLEADO_TAREA_GENERAL.objects.filter(AE_TAREA=tarea).delete()
            ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL.objects.filter(AEC_TAREA=tarea).delete()
            ASIGNACION_RECURSO_TAREA_GENERAL.objects.filter(ART_TAREA=tarea).delete()

            # Asignar empleados
            for empleado_id in empleados_ids:
                id_emp = EMPLEADO.objects.get(id=empleado_id)
                asignacion = ASIGNACION_EMPLEADO_TAREA_GENERAL(
                    AE_TAREA=tarea,
                    AE_EMPLEADO=id_emp,
                    AE_CESTADO = 'ASIGNADO',
                    AE_CUSUARIO_CREADOR = request.user,
                    AE_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,  
                    AE_FFECHA_FINALIZACION=tarea.TG_FFECHA_FIN_ESTIMADA                      
                )
                crear_log(request.user, 'Actualizar Asignación de Empleado a Tarea General', f'Se actualizó la asignación de empleado a tarea general: {tarea.TG_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                asignacion.save()

            # Asignar contratistas
            for contratista_id in contratistas_ids:
                id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL(
                    AEC_TAREA=tarea,
                    AEC_EMPLEADO=id_emp,
                    AEC_CESTADO = 'ASIGNADO',
                    AEC_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,
                    AEC_FFECHA_FINALIZACION=tarea.TG_FFECHA_FIN_ESTIMADA,
                    AEC_CUSUARIO_CREADOR=request.user
                )
                crear_log(request.user, 'Actualizar Asignación de Contratista a Tarea General', f'Se actualizó la asignación de contratista a tarea general: {tarea.TG_CNOMBRE} para el contratista: {id_emp.EC_CNOMBRE}')
                asignacion.save()

            # Procesar recursos                
            if recursos_json:
                recursos = json.loads(recursos_json)
                for recurso in recursos:
                    id_rec = PRODUCTO.objects.get(id=recurso['id'])
                    asignacion = ASIGNACION_RECURSO_TAREA_GENERAL(
                        ART_TAREA=tarea,
                        ART_PRODUCTO=id_rec,
                        ART_FFECHA_ASIGNACION=tarea.TG_FFECHA_INICIO,
                        ART_CUSUARIO_CREADOR=request.user,
                        ART_CANTIDAD=int(float(recurso['cantidad'])),   
                        ART_COSTO_UNITARIO=int(float(recurso['costo'])),
                        ART_COSTO_TOTAL = int(float(recurso['costo'])) * int(float(recurso['cantidad']))
                    )
                    crear_log(request.user, 'Actualizar Asignación de Recurso a Tarea General', f'Se actualizó la asignación de recurso a tarea general: {tarea.TG_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
                    asignacion.save()

            messages.success(request, 'Asignaciones de la tarea general actualizadas correctamente')
            if page == 1:
                return redirect('/proycli_listone/'+str(tarea.TG_PROYECTO_CLIENTE.id)+'/')
            else:
                return redirect('/tarea_general_listall/')
        
        # Preparar datos para mostrar en el template
        empleados_asignados_ids = list(empleados_asignados.values_list('AE_EMPLEADO__id', flat=True))
        contratistas_asignados_ids = list(contratistas_asignados.values_list('AEC_EMPLEADO__id', flat=True))
        recursos_asignados_data = [
            {
                'id': str(recurso.ART_PRODUCTO.id),
                'nombre': recurso.ART_PRODUCTO.PR_CNOMBRE,
                'cantidad': str(recurso.ART_CANTIDAD),
                'costo': str(recurso.ART_COSTO_UNITARIO)
            } for recurso in recursos_asignados
        ]
        
        ctx = {
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,
            'tarea': tarea,
            'empleados_asignados_ids': empleados_asignados_ids,
            'contratistas_asignados_ids': contratistas_asignados_ids,
            'recursos_asignados_data': json.dumps(recursos_asignados_data),
            'page': page,
            'proyecto':proyecto
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_update_asignaciones.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_GENERAL_LISTONE(request, pk, page=1):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_GENERAL.objects.get(id=pk)
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_GENERAL.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_GENERAL.objects.filter(ART_TAREA=tarea)
        tarea.TG_NPROGRESO = int(round(float(tarea.TG_NPROGRESO)))
        ctx = {
            'tarea': tarea,
            'page': page,
            'empleados_asignados': empleados_asignados,
            'contratistas_asignados': contratistas_asignados,
            'recursos_asignados': recursos_asignados
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_listone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_GENERAL_DEPENDENCIA_ADDONE(request, pk):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_GENERAL.objects.get(id=pk)
        proyecto_actual = tarea.TG_PROYECTO_CLIENTE
        dependencia_existente = TAREA_GENERAL_DEPENDENCIA.objects.filter(TD_TAREA_PREDECESORA=tarea)
        if request.method == 'POST':
            form = formTAREA_GENERAL_DEPENDENCIA(request.POST)
            if form.is_valid():
                dependencia = form.save(commit=False)
                dependencia.TD_TAREA_PREDECESORA = tarea
                dependencia.save()
                crear_log(request.user, 'Crear Dependencia de Tarea General', f'Se creó la dependencia de tarea general: {tarea.TG_CNOMBRE} para la tarea: {dependencia.TD_TAREA_SUCESORA.TG_CNOMBRE}')
                messages.success(request, 'Dependencia agregada correctamente')
                return redirect('proycli_listone', pk=proyecto_actual.id)
        else:
            form = formTAREA_GENERAL_DEPENDENCIA()
        
        # Filtrar las tareas generales del proyecto actual
        tareas_sucesoras = TAREA_GENERAL.objects.filter(TG_PROYECTO_CLIENTE=proyecto_actual).exclude(id=tarea.id)
        form.fields['TD_TAREA_SUCESORA'].queryset = tareas_sucesoras
        
        ctx = {
            'form': form,
            'tarea': tarea,
            'dependencia_existente': dependencia_existente  
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_dependencia_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

# ----------TAREA INGENIERIA--------------

def TAREA_INGENIERIA_LISTALL(request):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tareas_ingenieria = TAREA_INGENIERIA.objects.all()
        ctx = {
            'tareas_ingenieria': tareas_ingenieria
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_ADDONE(request, page):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        form = formTAREA_INGENIERIA()
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_INGENIERIA()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_INGENIERIA()

        if request.method == 'POST':
            form = formTAREA_INGENIERIA(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TI_CUSUARIO_CREADOR = request.user
                crear_log(request.user, 'Crear Tarea de Ingeniería', f'Se creó la tarea de ingeniería: {tarea.TI_CNOMBRE}')
                tarea.save()

                # Manejar asignaciones múltiples
                empleados_ids = request.POST.getlist('empleados')
                contratistas_ids = request.POST.getlist('contratistas')                
                recursos_json = request.POST.get('recursos_json')

                # Asignar empleados
                for empleado_id in empleados_ids:
                    id_emp = EMPLEADO.objects.get(id=empleado_id)
                    asignacion = ASIGNACION_EMPLEADO_TAREA_INGENIERIA(
                        AE_TAREA=tarea,
                        AE_EMPLEADO=id_emp,
                        AE_CESTADO = 'ASIGNADO',
                        AE_CUSUARIO_CREADOR = request.user,
                        AE_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,  
                        AE_FFECHA_FINALIZACION=tarea.TI_FFECHA_FIN_ESTIMADA                      
                    )
                    crear_log(request.user, 'Crear Asignación de Empleado a Tarea de Ingeniería', f'Se creó la asignación de empleado a tarea de ingeniería: {tarea.TI_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                    asignacion.save()

                # Asignar contratistas
                for contratista_id in contratistas_ids:
                    id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                    asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA(
                        AEC_TAREA=tarea,
                        AEC_EMPLEADO=id_emp,
                        AEC_CESTADO = 'ASIGNADO',
                        AEC_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,
                        AEC_FFECHA_FINALIZACION=tarea.TI_FFECHA_FIN_ESTIMADA,
                        AEC_CUSUARIO_CREADOR=request.user
                    )
                    crear_log(request.user, 'Crear Asignación de Contratista a Tarea de Ingeniería', f'Se creó la asignación de contratista a tarea de ingeniería: {tarea.TI_CNOMBRE} para el contratista: {id_emp.EM_CNOMBRE}')
                    asignacion.save()

                # Procesar recursos                
                if recursos_json:
                    recursos = json.loads(recursos_json)
                    for recurso in recursos:
                        id_rec = PRODUCTO.objects.get(id=recurso['id'])
                        asignacion = ASIGNACION_RECURSO_TAREA_INGENIERIA(
                            ART_TAREA=tarea,
                            ART_PRODUCTO=id_rec,
                            ART_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,
                            ART_CUSUARIO_CREADOR=request.user,
                            ART_CANTIDAD=int(recurso['cantidad']),
                            ART_COSTO_UNITARIO=int(recurso['costo']),
                            ART_COSTO_TOTAL = int(recurso['costo']) * int(recurso['cantidad'])
                        )
                        crear_log(request.user, 'Crear Asignación de Recurso a Tarea de Ingeniería', f'Se creó la asignación de recurso a tarea de ingeniería: {tarea.TI_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
                        asignacion.save()

                messages.success(request, 'Tarea de ingeniería guardada correctamente con las asignaciones seleccionadas')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TI_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_ingenieria_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')
        

        
        ctx = {
            'form': form,
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,
            'page': page,
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_UPDATE(request, pk, page=1):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_INGENIERIA.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_INGENIERIA(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TI_CUSUARIO_MODIFICADOR = request.user
                tarea.save()
                crear_log(request.user, 'Actualizar Tarea de Ingeniería', f'Se actualizó la tarea de ingeniería: {tarea.TI_CNOMBRE}')
                messages.success(request, 'Tarea de ingeniería actualizada correctamente')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TI_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_ingenieria_listall/')
        else:
            initial_data = {
                'TI_FFECHA_INICIO': tarea.TI_FFECHA_INICIO.strftime('%Y-%m-%d') if tarea.TI_FFECHA_INICIO else None,
                'TI_FFECHA_FIN_ESTIMADA': tarea.TI_FFECHA_FIN_ESTIMADA.strftime('%Y-%m-%d') if tarea.TI_FFECHA_FIN_ESTIMADA else None,
            }
            form = formTAREA_INGENIERIA(instance=tarea, initial=initial_data)
        
        ctx = {
            'form': form,
            'tarea': tarea
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_update.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_UPDATE_ASIGNACIONES(request, pk, page):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_INGENIERIA.objects.get(id=pk)
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_INGENIERIA()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_INGENIERIA()

        # Cargar asignaciones existentes
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_INGENIERIA.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_INGENIERIA.objects.filter(ART_TAREA=tarea)

        if request.method == 'POST':
            # Manejar asignaciones múltiples
            empleados_ids = request.POST.getlist('empleados')
            contratistas_ids = request.POST.getlist('contratistas')                
            recursos_json = request.POST.get('recursos_json')

            # Eliminar asignaciones existentes
            ASIGNACION_EMPLEADO_TAREA_INGENIERIA.objects.filter(AE_TAREA=tarea).delete()
            ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA.objects.filter(AEC_TAREA=tarea).delete()
            ASIGNACION_RECURSO_TAREA_INGENIERIA.objects.filter(ART_TAREA=tarea).delete()

            # Asignar empleados
            for empleado_id in empleados_ids:
                id_emp = EMPLEADO.objects.get(id=empleado_id)
                asignacion = ASIGNACION_EMPLEADO_TAREA_INGENIERIA(
                    AE_TAREA=tarea,
                    AE_EMPLEADO=id_emp,
                    AE_CESTADO = 'ASIGNADO',
                    AE_CUSUARIO_CREADOR = request.user,
                    AE_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,  
                    AE_FFECHA_FINALIZACION=tarea.TI_FFECHA_FIN_ESTIMADA                      
                )
                crear_log(request.user, 'Actualizar Asignación de Empleado a Tarea de Ingeniería', f'Se actualizó la asignación de empleado a tarea de ingeniería: {tarea.TI_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                asignacion.save()

            # Asignar contratistas
            for contratista_id in contratistas_ids:
                id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA(
                    AEC_TAREA=tarea,
                    AEC_EMPLEADO=id_emp,
                    AEC_CESTADO = 'ASIGNADO',
                    AEC_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,
                    AEC_FFECHA_FINALIZACION=tarea.TI_FFECHA_FIN_ESTIMADA,
                    AEC_CUSUARIO_CREADOR=request.user
                )
                crear_log(request.user, 'Actualizar Asignación de Contratista a Tarea de Ingeniería', f'Se actualizó la asignación de contratista a tarea de ingeniería: {tarea.TI_CNOMBRE} para el contratista: {id_emp.EC_CNOMBRE}')
                asignacion.save()

            # Procesar recursos                
            if recursos_json:
                recursos = json.loads(recursos_json)
                for recurso in recursos:
                    id_rec = PRODUCTO.objects.get(id=recurso['id'])
                    asignacion = ASIGNACION_RECURSO_TAREA_INGENIERIA(
                        ART_TAREA=tarea,
                        ART_PRODUCTO=id_rec,
                        ART_FFECHA_ASIGNACION=tarea.TI_FFECHA_INICIO,
                        ART_CUSUARIO_CREADOR=request.user,
                        ART_CANTIDAD=int(float(recurso['cantidad'])),
                        ART_COSTO_UNITARIO=int(float(recurso['costo'])),
                        ART_COSTO_TOTAL = int(float(recurso['costo'])) * int(float(recurso['cantidad']))
                    )
                    crear_log(request.user, 'Actualizar Asignación de Recurso a Tarea de Ingeniería', f'Se actualizó la asignación de recurso a tarea de ingeniería: {tarea.TI_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
                    asignacion.save()

            messages.success(request, 'Asignaciones de la tarea de ingeniería actualizadas correctamente')
            if page == 1:
                return redirect('/proycli_listone/'+str(tarea.TI_PROYECTO_CLIENTE.id)+'/')
            else:
                return redirect('/tarea_ingenieria_listall/')
        
        # Preparar datos para mostrar en el template
        empleados_asignados_ids = list(empleados_asignados.values_list('AE_EMPLEADO__id', flat=True))
        contratistas_asignados_ids = list(contratistas_asignados.values_list('AEC_EMPLEADO__id', flat=True))
        recursos_asignados_data = [
            {
                'id': str(recurso.ART_PRODUCTO.id),
                'nombre': recurso.ART_PRODUCTO.PR_CNOMBRE,
                'cantidad': str(recurso.ART_CANTIDAD),
                'costo': str(recurso.ART_COSTO_UNITARIO)
            } for recurso in recursos_asignados
        ]
        
        ctx = {
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,
            'tarea': tarea,
            'empleados_asignados_ids': empleados_asignados_ids,
            'contratistas_asignados_ids': contratistas_asignados_ids,
            'recursos_asignados_data': json.dumps(recursos_asignados_data),
            'page': page
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_update_asignaciones.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_LISTONE(request, pk, page=1):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_INGENIERIA.objects.get(id=pk)
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_INGENIERIA.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_INGENIERIA.objects.filter(ART_TAREA=tarea)
        tarea.TI_NPROGRESO = int(round(float(tarea.TI_NPROGRESO)))
        ctx = {
            'tarea': tarea,
            'page': page,
            'empleados_asignados': empleados_asignados,
            'contratistas_asignados': contratistas_asignados,
            'recursos_asignados': recursos_asignados
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_listone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_DEPENDENCIA_ADDONE(request, pk):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_INGENIERIA.objects.get(id=pk)
        proyecto_actual = tarea.TI_PROYECTO_CLIENTE
        dependencia_existente = TAREA_INGENIERIA_DEPENDENCIA.objects.filter(TD_TAREA_PREDECESORA=tarea)
        if request.method == 'POST':
            form = formTAREA_INGENIERIA_DEPENDENCIA(request.POST)
            if form.is_valid():
                dependencia = form.save(commit=False)
                dependencia.TD_TAREA_PREDECESORA = tarea
                dependencia.save()
                crear_log(request.user, 'Crear Dependencia de Tarea de Ingeniería', f'Se creó la dependencia de tarea de ingeniería: {tarea.TI_CNOMBRE} para la tarea: {dependencia.TD_TAREA_SUCESORA.TI_CNOMBRE}')
                messages.success(request, 'Dependencia agregada correctamente')
                return redirect('proycli_listone', pk=proyecto_actual.id)
        else:
            form = formTAREA_INGENIERIA_DEPENDENCIA()
        
        # Filtrar las tareas de ingeniería del proyecto actual
        tareas_sucesoras = TAREA_INGENIERIA.objects.filter(TI_PROYECTO_CLIENTE=proyecto_actual).exclude(id=tarea.id)
        form.fields['TD_TAREA_SUCESORA'].queryset = tareas_sucesoras
        
        ctx = {
            'form': form,
            'tarea': tarea,
            'dependencia_existente': dependencia_existente
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_dependencia_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

# ----------TAREA FINANCIERA--------------

def TAREA_FINANCIERA_LISTALL(request):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tareas_financiera = TAREA_FINANCIERA.objects.all()
        ctx = {
            'tareas_financiera': tareas_financiera
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_ADDONE(request, page):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        form = formTAREA_FINANCIERA()
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_FINANCIERA()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_FINANCIERA()        
        if request.method == 'POST':
            form = formTAREA_FINANCIERA(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TF_CUSUARIO_CREADOR = request.user
                
                # Aplicar lógica de fechas automáticamente
                fecha_inicio = form.cleaned_data.get('TF_FFECHA_INICIO')
                fecha_fin_estimada = form.cleaned_data.get('TF_FFECHA_FIN_ESTIMADA')
                
                if fecha_inicio and not fecha_fin_estimada:
                    tarea.TF_FFECHA_FIN_ESTIMADA = fecha_inicio
                elif fecha_fin_estimada and not fecha_inicio:
                    tarea.TF_FFECHA_INICIO = fecha_fin_estimada
                
                tarea.save()
                crear_log(request.user, 'Crear Tarea Financiera', f'Se creó la tarea financiera: {tarea.TF_CNOMBRE}')
                
                # Manejar asignaciones múltiples
                empleados_ids = request.POST.getlist('empleados')
                contratistas_ids = request.POST.getlist('contratistas')                
                recursos_json = request.POST.get('recursos_json')

                # Asignar empleados
                for empleado_id in empleados_ids:
                    id_emp = EMPLEADO.objects.get(id=empleado_id)
                    asignacion = ASIGNACION_EMPLEADO_TAREA_FINANCIERA(
                        AE_TAREA=tarea,
                        AE_EMPLEADO=id_emp,
                        AE_CESTADO = 'ASIGNADO',
                        AE_CUSUARIO_CREADOR = request.user,
                        AE_FFECHA_ASIGNACION=fecha_inicio,  
                        AE_FFECHA_FINALIZACION=fecha_fin_estimada                      
                    )
                    crear_log(request.user, 'Crear Asignación de Empleado a Tarea Financiera', f'Se creó la asignación de empleado a tarea financiera: {tarea.TF_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                    asignacion.save()

                # Asignar contratistas
                for contratista_id in contratistas_ids:
                    id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                    asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA(
                        AEC_TAREA=tarea,
                        AEC_EMPLEADO=id_emp,
                        AEC_CESTADO = 'ASIGNADO',
                        AEC_FFECHA_ASIGNACION=fecha_inicio,
                        AEC_FFECHA_FINALIZACION=fecha_fin_estimada,
                        AEC_CUSUARIO_CREADOR=request.user
                    )
                    crear_log(request.user, 'Crear Asignación de Contratista a Tarea Financiera', f'Se creó la asignación de contratista a tarea financiera: {tarea.TF_CNOMBRE} para el contratista: {id_emp.EM_CNOMBRE}')
                    asignacion.save()

                # Procesar recursos                
                if recursos_json:
                    recursos = json.loads(recursos_json)
                    for recurso in recursos:
                        id_rec = PRODUCTO.objects.get(id=recurso['id'])
                        asignacion = ASIGNACION_RECURSO_TAREA_FINANCIERA(
                            ART_TAREA=tarea,
                            ART_PRODUCTO=id_rec,
                            ART_FFECHA_ASIGNACION=fecha_inicio,
                            ART_CUSUARIO_CREADOR=request.user,
                            ART_CANTIDAD=int(recurso['cantidad']),
                            ART_COSTO_UNITARIO=int(recurso['costo']),
                            ART_COSTO_TOTAL = int(recurso['costo']) * int(recurso['cantidad'])
                        )
                        crear_log(request.user, 'Crear Asignación de Recurso a Tarea Financiera', f'Se creó la asignación de recurso a tarea financiera: {tarea.TF_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
                        asignacion.save()
                
                messages.success(request, 'Tarea financiera guardada correctamente con las asignaciones seleccionadas')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TF_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_financiera_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')

        
        ctx = {
            'form': form,
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,            
            'page': page,
            
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_UPDATE(request, pk, page=1):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_FINANCIERA.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_FINANCIERA(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TF_CUSUARIO_MODIFICADOR = request.user
                
                # Aplicar lógica de fechas automáticamente
                fecha_inicio = form.cleaned_data.get('TF_FFECHA_INICIO')
                fecha_fin_estimada = form.cleaned_data.get('TF_FFECHA_FIN_ESTIMADA')
                
                if fecha_inicio and not fecha_fin_estimada:
                    tarea.TF_FFECHA_FIN_ESTIMADA = fecha_inicio
                elif fecha_fin_estimada and not fecha_inicio:
                    tarea.TF_FFECHA_INICIO = fecha_fin_estimada
                
                tarea.save()
                crear_log(request.user, 'Actualizar Tarea Financiera', f'Se actualizó la tarea financiera: {tarea.TF_CNOMBRE}')
                messages.success(request, 'Tarea financiera actualizada correctamente')
                if page == 1:
                    return redirect('/proycli_listone/'+str(tarea.TF_PROYECTO_CLIENTE.id)+'/')
                else:
                    return redirect('/tarea_financiera_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')
        else:
            # Asegúrate de que las fechas se carguen correctamente en el formulario
            initial_data = {
                'TF_FFECHA_INICIO': tarea.TF_FFECHA_INICIO.strftime('%Y-%m-%d') if tarea.TF_FFECHA_INICIO else None,
                'TF_FFECHA_FIN_ESTIMADA': tarea.TF_FFECHA_FIN_ESTIMADA.strftime('%Y-%m-%d') if tarea.TF_FFECHA_FIN_ESTIMADA else None,
                'TF_FFECHA_FIN_REAL': tarea.TF_FFECHA_FIN_REAL.strftime('%Y-%m-%d') if tarea.TF_FFECHA_FIN_REAL else None
            }
            form = formTAREA_FINANCIERA(instance=tarea, initial=initial_data)
        
        ctx = {
            'form': form,
            'tarea': tarea,
            'page': page
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_update.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_UPDATE_ASIGNACIONES(request, pk, page):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_FINANCIERA.objects.get(id=pk)
        form_asignacion_empleado = formASIGNACION_EMPLEADO_TAREA_FINANCIERA()
        form_asignacion_contratista = formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA()
        form_asignacion_recurso = formASIGNACION_RECURSO_TAREA_FINANCIERA()

        # Cargar asignaciones existentes
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_FINANCIERA.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_FINANCIERA.objects.filter(ART_TAREA=tarea)

        if request.method == 'POST':
            # Manejar asignaciones múltiples
            empleados_ids = request.POST.getlist('empleados')
            contratistas_ids = request.POST.getlist('contratistas')                
            recursos_json = request.POST.get('recursos_json')

            # Eliminar asignaciones existentes
            ASIGNACION_EMPLEADO_TAREA_FINANCIERA.objects.filter(AE_TAREA=tarea).delete()
            ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA.objects.filter(AEC_TAREA=tarea).delete()
            ASIGNACION_RECURSO_TAREA_FINANCIERA.objects.filter(ART_TAREA=tarea).delete()

            # Asignar empleados
            for empleado_id in empleados_ids:
                id_emp = EMPLEADO.objects.get(id=empleado_id)
                asignacion = ASIGNACION_EMPLEADO_TAREA_FINANCIERA(
                    AE_TAREA=tarea,
                    AE_EMPLEADO=id_emp,
                    AE_CESTADO = 'ASIGNADO',
                    AE_CUSUARIO_CREADOR = request.user,
                    AE_FFECHA_ASIGNACION=tarea.TF_FFECHA_INICIO,  
                    AE_FFECHA_FINALIZACION=tarea.TF_FFECHA_FIN_ESTIMADA                      
                )
                crear_log(request.user, 'Actualizar Asignación de Empleado a Tarea Financiera', f'Se actualizó la asignación de empleado a tarea financiera: {tarea.TF_CNOMBRE} para el empleado: {id_emp.EM_CNOMBRE}')
                asignacion.save()

            # Asignar contratistas
            for contratista_id in contratistas_ids:
                id_emp = EMPLEADO_CONTRATISTA.objects.get(id=contratista_id)
                asignacion = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA(
                    AEC_TAREA=tarea,
                    AEC_EMPLEADO=id_emp,
                    AEC_CESTADO = 'ASIGNADO',
                    AEC_FFECHA_ASIGNACION=tarea.TF_FFECHA_INICIO,
                    AEC_FFECHA_FINALIZACION=tarea.TF_FFECHA_FIN_ESTIMADA,
                    AEC_CUSUARIO_CREADOR=request.user
                )
                crear_log(request.user, 'Actualizar Asignación de Contratista a Tarea Financiera', f'Se actualizó la asignación de contratista a tarea financiera: {tarea.TF_CNOMBRE} para el contratista: {id_emp.EC_CNOMBRE}')
                asignacion.save()

            # Procesar recursos                
            if recursos_json:
                recursos = json.loads(recursos_json)
                for recurso in recursos:
                    id_rec = PRODUCTO.objects.get(id=recurso['id'])
                    asignacion = ASIGNACION_RECURSO_TAREA_FINANCIERA(
                        ART_TAREA=tarea,
                        ART_PRODUCTO=id_rec,
                        ART_FFECHA_ASIGNACION=tarea.TF_FFECHA_INICIO,
                        ART_CUSUARIO_CREADOR=request.user,
                        ART_CANTIDAD=int(float(recurso['cantidad'])),  # Convert to float first, then to int
                        ART_COSTO_UNITARIO=int(float(recurso['costo'])),  # Same here
                        ART_COSTO_TOTAL = int(float(recurso['costo'])) * int(float(recurso['cantidad']))
                    )
                    asignacion.save()
                    crear_log(request.user, 'Actualizar Asignación de Recurso a Tarea Financiera', f'Se actualizó la asignación de recurso a tarea financiera: {tarea.TF_CNOMBRE} para el recurso: {id_rec.PR_CNOMBRE}')
            messages.success(request, 'Asignaciones de la tarea financiera actualizadas correctamente')
            if page == 1:
                return redirect('/proycli_listone/'+str(tarea.TF_PROYECTO_CLIENTE.id)+'/')
            else:
                return redirect('/tarea_financiera_listall/')
        
        # Preparar datos para mostrar en el template
        empleados_asignados_ids = list(empleados_asignados.values_list('AE_EMPLEADO__id', flat=True))
        contratistas_asignados_ids = list(contratistas_asignados.values_list('AEC_EMPLEADO__id', flat=True))
        recursos_asignados_data = [
            {
                'id': str(recurso.ART_PRODUCTO.id),
                'nombre': recurso.ART_PRODUCTO.PR_CNOMBRE,
                'cantidad': str(recurso.ART_CANTIDAD),
                'costo': str(recurso.ART_COSTO_UNITARIO)
            } for recurso in recursos_asignados
        ]
        
        ctx = {
            'form_asignacion_empleado': form_asignacion_empleado,
            'form_asignacion_contratista': form_asignacion_contratista,
            'form_asignacion_recurso': form_asignacion_recurso,
            'tarea': tarea,
            'empleados_asignados_ids': empleados_asignados_ids,
            'contratistas_asignados_ids': contratistas_asignados_ids,
            'recursos_asignados_data': json.dumps(recursos_asignados_data),
            'page': page
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_update_asignaciones.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_LISTONE(request, pk, page=1):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_FINANCIERA.objects.get(id=pk)
        empleados_asignados = ASIGNACION_EMPLEADO_TAREA_FINANCIERA.objects.filter(AE_TAREA=tarea)
        contratistas_asignados = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA.objects.filter(AEC_TAREA=tarea)
        recursos_asignados = ASIGNACION_RECURSO_TAREA_FINANCIERA.objects.filter(ART_TAREA=tarea)
        tarea.TF_NPROGRESO = int(round(float(tarea.TF_NPROGRESO)))
        ctx = {
            'tarea': tarea,
            'empleados_asignados': empleados_asignados,
            'contratistas_asignados': contratistas_asignados,
            'recursos_asignados': recursos_asignados,
            'page': page
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_listone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_DEPENDENCIA_ADDONE(request, pk):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tarea = TAREA_FINANCIERA.objects.get(id=pk)
        proyecto_actual = tarea.TF_PROYECTO_CLIENTE
        dependencia_existente = TAREA_FINANCIERA_DEPENDENCIA.objects.filter(TD_TAREA_PREDECESORA=tarea)
        if request.method == 'POST':
            form = formTAREA_FINANCIERA_DEPENDENCIA(request.POST)
            if form.is_valid():
                dependencia = form.save(commit=False)
                dependencia.TD_TAREA_PREDECESORA = tarea
                dependencia.save()
                crear_log(request.user, 'Crear Dependencia de Tarea Financiera', f'Se creó la dependencia de tarea financiera: {tarea.TF_CNOMBRE} para la tarea: {dependencia.TD_TAREA_SUCESORA.TF_CNOMBRE}')                                                                               
                messages.success(request, 'Dependencia agregada correctamente')
                return redirect('proycli_listone', pk=proyecto_actual.id)
        else:
            form = formTAREA_FINANCIERA_DEPENDENCIA()
        
        # Filtrar las tareas financieras del proyecto actual
        tareas_sucesoras = TAREA_FINANCIERA.objects.filter(TF_PROYECTO_CLIENTE=proyecto_actual).exclude(id=tarea.id)
        form.fields['TD_TAREA_SUCESORA'].queryset = tareas_sucesoras
        
        ctx = {
            'form': form,
            'tarea': tarea,
            'dependencia_existente': dependencia_existente  
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_dependencia_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

# ----------TAREA UPDATE DATA--------------

def format_decimal(value):
    if value is None:
        return '0.00'
    return str(Decimal(value).quantize(Decimal('0.01')))

def tarea_update_data(request, tipo_tarea, pk):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    if tipo_tarea == 'general':
        Tarea = TAREA_GENERAL
        AsignacionEmpleado = ASIGNACION_EMPLEADO_TAREA_GENERAL
        AsignacionContratista = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL
        AsignacionRecurso = ASIGNACION_RECURSO_TAREA_GENERAL
        progreso_field = 'TG_NPROGRESO'
        duracion_real_field = 'TG_NDURACION_REAL'
        proyecto_field = 'TG_PROYECTO_CLIENTE'
    elif tipo_tarea == 'ingenieria':
        Tarea = TAREA_INGENIERIA
        AsignacionEmpleado = ASIGNACION_EMPLEADO_TAREA_INGENIERIA
        AsignacionContratista = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA
        AsignacionRecurso = ASIGNACION_RECURSO_TAREA_INGENIERIA
        progreso_field = 'TI_NPROGRESO'
        duracion_real_field = 'TI_NDURACION_REAL'
        proyecto_field = 'TI_PROYECTO_CLIENTE'
    elif tipo_tarea == 'financiera':
        Tarea = TAREA_FINANCIERA
        AsignacionEmpleado = ASIGNACION_EMPLEADO_TAREA_FINANCIERA
        AsignacionContratista = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA
        AsignacionRecurso = ASIGNACION_RECURSO_TAREA_FINANCIERA
        progreso_field = 'TF_NPROGRESO'
        duracion_real_field = 'TF_NDURACION_REAL'
        proyecto_field = 'TF_PROYECTO_CLIENTE'
    else:
        return HttpResponseBadRequest("Tipo de tarea no válido")

    tarea = get_object_or_404(Tarea, id=pk)
    proyecto = getattr(tarea, proyecto_field)
    
    empleados_asignados = AsignacionEmpleado.objects.filter(AE_TAREA=tarea)
    contratistas_asignados = AsignacionContratista.objects.filter(AEC_TAREA=tarea)
    recursos_asignados = AsignacionRecurso.objects.filter(ART_TAREA=tarea)

    empleados_formateados = []
    for empleado in empleados_asignados:
        empleados_formateados.append({
            'id': empleado.id,
            'AE_EMPLEADO': empleado.AE_EMPLEADO,
            'AE_COSTO_REAL': format_decimal(empleado.AE_COSTO_REAL),
            'AE_HORAS_REALES': format_decimal(empleado.AE_HORAS_REALES),
        })

    contratistas_formateados = []
    for contratista in contratistas_asignados:
        contratistas_formateados.append({
            'id': contratista.id,
            'AEC_EMPLEADO': contratista.AEC_EMPLEADO,
            'AEC_COSTO_REAL': format_decimal(contratista.AEC_COSTO_REAL),
            'AEC_HORAS_REALES': format_decimal(contratista.AEC_HORAS_REALES),
        })

    recursos_formateados = []
    for recurso in recursos_asignados:
        recursos_formateados.append({
            'id': recurso.id,
            'ART_PRODUCTO': recurso.ART_PRODUCTO,
            'ART_CANTIDAD': format_decimal(recurso.ART_CANTIDAD),
            'ART_COSTO_UNITARIO': format_decimal(recurso.ART_COSTO_UNITARIO),
            'ART_HORAS_REALES': format_decimal(recurso.ART_HORAS_REALES),
        })

    if request.method == 'POST':
        try:
            # Actualizar datos de la tarea
            if tipo_tarea == 'general':
                proyecto_actual = tarea.TG_PROYECTO_CLIENTE
                if request.POST.get('porcentajeAvance'):
                    tarea.TG_NPROGRESO = float(request.POST.get('porcentajeAvance'))
                if request.POST.get('horasTarea'):
                    tarea.TG_NDURACION_REAL = float(request.POST.get('horasTarea'))
            elif tipo_tarea == 'ingenieria':
                proyecto_actual = tarea.TI_PROYECTO_CLIENTE
                if request.POST.get('porcentajeAvance'):
                    tarea.TI_NPROGRESO = float(request.POST.get('porcentajeAvance'))
                if request.POST.get('horasTarea'):
                    tarea.TI_NDURACION_REAL = float(request.POST.get('horasTarea'))
            elif tipo_tarea == 'financiera':
                proyecto_actual = tarea.TF_PROYECTO_CLIENTE
                if request.POST.get('porcentajeAvance'):
                    tarea.TF_NPROGRESO = float(request.POST.get('porcentajeAvance'))
                if request.POST.get('horasTarea'):
                    tarea.TF_NDURACION_REAL = float(request.POST.get('horasTarea'))
            tarea.save()
            crear_log(request.user, f'Actualizar Tarea {tipo_tarea}', f'Se actualizó la tarea: {tarea.TG_CNOMBRE if tipo_tarea == "general" else tarea.TI_CNOMBRE if tipo_tarea == "ingenieria" else tarea.TF_CNOMBRE}')
            # Actualizar asignaciones
            for empleado in empleados_asignados:
                if request.POST.get(f'costo_empleado_{empleado.id}'):
                    empleado.AE_COSTO_REAL = float(request.POST.get(f'costo_empleado_{empleado.id}'))
                if request.POST.get(f'horas_empleado_{empleado.id}'):
                    empleado.AE_HORAS_REALES = float(request.POST.get(f'horas_empleado_{empleado.id}')  )
                if request.POST.get(f'total_empleado_{empleado.id}'):
                    empleado.AE_COSTO_TOTAL = float(request.POST.get(f'total_empleado_{empleado.id}'))
                crear_log(request.user, f'Actualizar Asignación de Empleado a Tarea {tipo_tarea}', f'Se actualizó la asignación de empleado a tarea: {tarea.TG_CNOMBRE if tipo_tarea == "general" else tarea.TI_CNOMBRE if tipo_tarea == "ingenieria" else tarea.TF_CNOMBRE} para el empleado: {empleado.AE_EMPLEADO}')
                empleado.save()

            for contratista in contratistas_asignados:
                if request.POST.get(f'costo_contratista_{contratista.id}'):
                    contratista.AEC_COSTO_REAL = float(request.POST.get(f'costo_contratista_{contratista.id}'))
                if request.POST.get(f'horas_contratista_{contratista.id}'):
                    contratista.AEC_HORAS_REALES = float(request.POST.get(f'horas_contratista_{contratista.id}'))
                if request.POST.get(f'total_contratista_{contratista.id}'):
                    contratista.AEC_COSTO_TOTAL = float(request.POST.get(f'total_contratista_{contratista.id}'))
                crear_log(request.user, f'Actualizar Asignación de Contratista a Tarea {tipo_tarea}', f'Se actualizó la asignación de contratista a tarea: {tarea.TG_CNOMBRE if tipo_tarea == "general" else tarea.TI_CNOMBRE if tipo_tarea == "ingenieria" else tarea.TF_CNOMBRE} para el contratista: {contratista.AEC_EMPLEADO}')
                contratista.save()

            for recurso in recursos_asignados:
                if request.POST.get(f'cantidad_recurso_{recurso.id}'):
                    recurso.ART_CANTIDAD = float(request.POST.get(f'cantidad_recurso_{recurso.id}'))
                if request.POST.get(f'costo_recurso_{recurso.id}'):
                    recurso.ART_COSTO_UNITARIO = float(request.POST.get(f'costo_recurso_{recurso.id}'))
                if request.POST.get(f'horas_recurso_{recurso.id}'):
                    recurso.ART_HORAS_REALES = float(request.POST.get(f'horas_recurso_{recurso.id}'))
                if request.POST.get(f'total_recurso_{recurso.id}'):   
                    total_recurso = request.POST.get(f'total_recurso_{recurso.id}')
                    total_recurso = total_recurso.replace(',', '.')
                    recurso.ART_COSTO_REAL = float(total_recurso)
                crear_log(request.user, f'Actualizar Asignación de Recurso a Tarea {tipo_tarea}', f'Se actualizó la asignación de recurso a tarea: {tarea.TG_CNOMBRE if tipo_tarea == "general" else tarea.TI_CNOMBRE if tipo_tarea == "ingenieria" else tarea.TF_CNOMBRE} para el recurso: {recurso.ART_PRODUCTO}')
                recurso.save()

            return JsonResponse({
                'success': True,
                'message': 'Datos de la tarea actualizados correctamente.',
                'redirect_url': reverse('proycli_listone', kwargs={'pk': proyecto_actual.id})
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al actualizar los datos: {str(e)}'
            }, status=400)

    ctx = {
        'tarea': tarea,
        'empleados_asignados': empleados_formateados,
        'contratistas_asignados': contratistas_formateados,
        'recursos_asignados': recursos_formateados,
        'porcentaje_avance': format_decimal(getattr(tarea, progreso_field)),
        'horas_tarea': format_decimal(getattr(tarea, duracion_real_field)),
        'tipo_tarea': tipo_tarea,
    }
    return render(request, 'home/TAREA/tarea_update_data.html', ctx)
# ----------TAREA UPDATE DATA--------------

# ----------TAREA DOCUMENTOS--------------
def get_adjunto_model(tipo_tarea):
    if tipo_tarea == 'TAREA_GENERAL':
        return ADJUNTO_TAREA_GENERAL
    elif tipo_tarea == 'TAREA_INGENIERIA':
        return ADJUNTO_TAREA_INGENIERIA
    elif tipo_tarea == 'TAREA_FINANCIERA':
        return ADJUNTO_TAREA_FINANCIERA
    raise ValueError(f"Tipo de tarea no válido: {tipo_tarea}")

def get_adjunto_model_and_prefix(tipo_tarea):
    if tipo_tarea == 'TAREA_GENERAL':
        return ADJUNTO_TAREA_GENERAL, 'AT'
    elif tipo_tarea == 'TAREA_INGENIERIA':
        return ADJUNTO_TAREA_INGENIERIA, 'ATI'
    elif tipo_tarea == 'TAREA_FINANCIERA':
        return ADJUNTO_TAREA_FINANCIERA, 'ATF'
    else:
        raise ValueError(f"Tipo de tarea no válido: {tipo_tarea}")

def tarea_adjuntos_lista(request, tarea_id, tipo_tarea):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if tipo_tarea == 'TAREA_GENERAL':
            adjuntos = ADJUNTO_TAREA_GENERAL.objects.filter(AT_TAREA_id=tarea_id)
            prefix = 'AT'
        elif tipo_tarea == 'TAREA_INGENIERIA':
            adjuntos = ADJUNTO_TAREA_INGENIERIA.objects.filter(ATI_TAREA_id=tarea_id)
            prefix = 'ATI'
        elif tipo_tarea == 'TAREA_FINANCIERA':
            adjuntos = ADJUNTO_TAREA_FINANCIERA.objects.filter(ATF_TAREA_id=tarea_id)
            prefix = 'ATF'
        else:
            return JsonResponse({
                'success': False,
                'message': f'Tipo de tarea no válido: {tipo_tarea}'
            }, status=400)
        
        adjuntos_data = []
        for adjunto in adjuntos:
            adjuntos_data.append({
                'nombre': getattr(adjunto, f'{prefix}_CNOMBRE'),
                'descripcion': getattr(adjunto, f'{prefix}_CDESCRIPCION'),
                'fecha_creacion': getattr(adjunto, f'{prefix}_FFECHA_CREACION').strftime('%d/%m/%Y'),
                'id': adjunto.id
            })
        
        return JsonResponse({'success': True, 'adjuntos': adjuntos_data})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al obtener los adjuntos: {str(e)}'
        }, status=400)

def tarea_adjunto_agregar(request, tarea_id, tipo_tarea):
    if not has_auth(request.user, 'ADD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        AdjuntoModel, prefix = get_adjunto_model_and_prefix(tipo_tarea)
        form = AdjuntoTareaForm(request.POST, request.FILES, tipo_tarea=tipo_tarea)
        if form.is_valid():
            adjunto = AdjuntoModel(**{
                f'{prefix}_TAREA_id': tarea_id,
                f'{prefix}_CARCHIVO': form.cleaned_data['CARCHIVO'],
                f'{prefix}_CNOMBRE': form.cleaned_data['CNOMBRE'],
                f'{prefix}_CDESCRIPCION': form.cleaned_data['CDESCRIPCION'],
                f'{prefix}_CUSUARIO_CREADOR': request.user,
            })
            adjunto.save()
            return JsonResponse({'success': True, 'message': 'Adjunto agregado correctamente'})
        else:
            return JsonResponse({'success': False, 'message': 'Formulario inválido', 'errors': form.errors})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al agregar el adjunto: {str(e)}'
        }, status=400)
        
@ensure_csrf_cookie        
@require_http_methods(["GET", "POST"])
def tarea_adjunto_editar(request, pk, tipo_tarea):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        AdjuntoModel, prefix = get_adjunto_model_and_prefix(tipo_tarea)
        adjunto = get_object_or_404(AdjuntoModel, pk=pk)
        
        if request.method == 'GET':
            initial_data = {
                'CNOMBRE': getattr(adjunto, f'{prefix}_CNOMBRE'),
                'CDESCRIPCION': getattr(adjunto, f'{prefix}_CDESCRIPCION'),
            }
            form = AdjuntoTareaForm(initial=initial_data, tipo_tarea=tipo_tarea, is_edit=True)
            csrf_token = get_token(request)
            form_html = render_to_string('home/TAREA/adjunto_form_partial.html', {
                'form': form, 
                'adjunto': adjunto, 
                'tipo_tarea': tipo_tarea,
                'csrf_token': csrf_token
            }, request=request)
            return HttpResponse(form_html)
        
        elif request.method == 'POST':
            form = AdjuntoTareaForm(request.POST, request.FILES, tipo_tarea=tipo_tarea, is_edit=True)
            if form.is_valid():
                setattr(adjunto, f'{prefix}_CNOMBRE', form.cleaned_data['CNOMBRE'])
                setattr(adjunto, f'{prefix}_CDESCRIPCION', form.cleaned_data['CDESCRIPCION'])
                if form.cleaned_data['CARCHIVO']:
                    setattr(adjunto, f'{prefix}_CARCHIVO', form.cleaned_data['CARCHIVO'])
                setattr(adjunto, f'{prefix}_CUSUARIO_MODIFICADOR', request.user)
                adjunto.save()
                return JsonResponse({'success': True, 'message': 'Adjunto editado correctamente'})
            else:
                return JsonResponse({'success': False, 'message': 'Formulario inválido', 'errors': form.errors})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al editar el adjunto: {str(e)}'
        }, status=400)

def tarea_adjunto_eliminar(request, pk, tipo_tarea):
    if not has_auth(request.user, 'UPD_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        AdjuntoModel = get_adjunto_model(tipo_tarea)
        adjunto = get_object_or_404(AdjuntoModel, pk=pk)
        adjunto.delete()
        return JsonResponse({'success': True, 'message': 'Adjunto eliminado correctamente'})
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al eliminar el adjunto: {str(e)}'
        }, status=400)

def tarea_adjunto_descargar(request, pk, tipo_tarea):
    if not has_auth(request.user, 'VER_TAREAS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        AdjuntoModel, prefix = get_adjunto_model_and_prefix(tipo_tarea)
        adjunto = get_object_or_404(AdjuntoModel, pk=pk)
        
        file_field = getattr(adjunto, f'{prefix}_CARCHIVO')
        if not file_field:
            return HttpResponseNotFound('El archivo no existe')

        file_path = file_field.path
        if not os.path.exists(file_path):
            return HttpResponseNotFound('El archivo no existe en el sistema de archivos')

        # Obtener el nombre original del archivo
        original_filename = os.path.basename(file_field.name)
        
        # Determinar el tipo MIME
        content_type, encoding = mimetypes.guess_type(file_path)
        content_type = content_type or 'application/octet-stream'
        
        # Abrir el archivo en modo binario
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type=content_type)
        
        # Configurar los encabezados de la respuesta
        response['Content-Disposition'] = f'attachment; filename="{original_filename}"'
        
        # Añadir el tamaño del archivo al encabezado
        response['Content-Length'] = os.path.getsize(file_path)
        
        return response
    except Exception as e:
        # Registrar el error para debugging
        import logging
        logging.error(f"Error al descargar adjunto: {str(e)}")
        
        return HttpResponseNotFound('Error al descargar el archivo')
# ----------TAREA DOCUMENTOS--------------

#--------------------------------------
#----------------TAREAS----------------
#--------------------------------------

def ACTA_REUNION_LISTALL(request):
    if not has_auth(request.user, 'VER_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = ACTA_REUNION.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/ACTA_REUNION/actareunion_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ACTA_REUNION_ADDONE(request):
    if not has_auth(request.user, 'ADD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formACTA_REUNION(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, f'Crear Acta de Reunión', f'Se creó el acta de reunión: {form.instance.AR_CTITULO}')
                messages.success(request, 'Acta de reunión guardada correctamente')
                return redirect('/actareunion_listall/')
        form = formACTA_REUNION()
        ctx = {
            'form': form
        }
        return render(request, 'home/ACTA_REUNION/actareunion_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ACTA_REUNION_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_PROYECTOS_CLIENTES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        acta_reunion = ACTA_REUNION.objects.get(id=pk)
        if request.method == 'POST':
            form = formACTA_REUNION(request.POST, instance=acta_reunion)
            if form.is_valid():
                form.save()
                crear_log(request.user, f'Actualizar Acta de Reunión', f'Se actualizó el acta de reunión: {acta_reunion.AR_CTITULO}')
                messages.success(request, 'Acta de reunión actualizada correctamente')
                return redirect('/actareunion_listall/')
        form = formACTA_REUNION(instance=acta_reunion)
        ctx = {
            'form': form
        }
        return render(request, 'home/ACTA_REUNION/actareunion_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COTIZACION_LISTALL(request):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = COTIZACION.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/COTIZACION/cotizacion_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COTIZACION_ADDONE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    
    try:
        if request.method == 'POST':
            form = formCOTIZACION(request.POST)
            
            if form.is_valid():
                cotizacion = form.save(commit=False)
                cotizacion.CO_CUSUARIO_CREADOR = request.user
                

                
                cotizacion.save()
                crear_log(request.user, f'Crear Cotización', f'Se creó la cotización: {cotizacion.CO_CNUMERO}')
                messages.success(request, 'Cotización guardada correctamente')
                return redirect('/cotizacion_listall/')
            else:
                # Si el formulario no es válido, imprimir los errores para depuración
                print(form.errors)
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo {field}: {error}')
        else:
            form = formCOTIZACION()
        
        ctx = {
            'form': form,
            'state': 'add'
        }
        return render(request, 'home/COTIZACION/cotizacion_addone.html', ctx)
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        messages.error(request, f'Error al procesar la solicitud: {str(e)}')
        return redirect('/')

def COTIZACION_ADD_LINE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            cotizacion_id = request.POST.get('cotizacion_id')
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            precio_unitario = request.POST.get('precioUnitario')
            descuento = request.POST.get('descuento')

            cotizacion = COTIZACION.objects.get(id=cotizacion_id)
            producto = PRODUCTO.objects.get(id=producto_id)

            # Ensure cantidad and precio_unitario are at least 1
            cantidad = max(1, int(cantidad or 0))
            precio_unitario = max(Decimal('1'), Decimal(precio_unitario or '0'))

            
            precio_unitario_local = precio_unitario
            descuento_local = Decimal(descuento or '0')

            # Recalculate subtotal in local currency
            subtotal_local = Decimal(cantidad) * precio_unitario_local

            # Ensure descuento is non-negative and not greater than subtotal
            descuento_local = max(Decimal('0'), min(descuento_local, subtotal_local))

            # Recalculate total in local currency
            total_local = subtotal_local - descuento_local

            # Verificar si la combinación de cotización y producto ya existe
            existing_detail = COTIZACION_DETALLE.objects.filter(CD_COTIZACION=cotizacion, CD_PRODUCTO=producto).first()
            if existing_detail:
                existing_detail.delete()

            detalle = COTIZACION_DETALLE(
                CD_COTIZACION=cotizacion,
                CD_PRODUCTO=producto,
                CD_NCANTIDAD=cantidad,
                CD_NPRECIO_UNITARIO=precio_unitario_local,
                CD_NSUBTOTAL=subtotal_local,
                CD_NDESCUENTO=descuento_local,
                CD_NTOTAL=total_local,
                CD_CUSUARIO_CREADOR=request.user
            )
            crear_log(request.user, f'Crear Línea de Cotización', f'Se creó la línea de cotización: {detalle.CD_PRODUCTO}')
            detalle.save()

            # Recalculate COTIZACION.CO_NTOTAL
            total_cotizacion_local = COTIZACION_DETALLE.objects.filter(CD_COTIZACION=cotizacion).aggregate(Sum('CD_NTOTAL'))['CD_NTOTAL__sum'] or 0
            cotizacion.CO_NTOTAL = total_cotizacion_local

           

            crear_log(request.user, f'Actualizar Cotización', f'Se actualizó la cotización: {cotizacion.CO_CNUMERO}')
            cotizacion.save()

            messages.success(request, 'Línea de cotización agregada correctamente')
            return redirect(f'/cotizacion_listone/{cotizacion_id}')
        
        return redirect('/cotizacion_listall/')
    except Exception as e:
        errMsg = f"Error al agregar línea de cotización: {str(e)}"
        print(errMsg)
        messages.error(request, errMsg)
        return JsonResponse({'error': str(errMsg)}, status=400)

def COTIZACION_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cotizacion = COTIZACION.objects.get(id=pk)
        if request.method == 'POST':
            form = formCOTIZACION(request.POST, instance=cotizacion)
            if form.is_valid():
                cotizacion = form.save(commit=False)
                cotizacion.CO_CUSUARIO_MODIFICADOR = request.user
                cotizacion.save()
                crear_log(request.user, f'Actualizar Cotización', f'Se actualizó la cotización: {cotizacion.CO_CNUMERO}')
                messages.success(request, 'Cotización actualizada correctamente')
                return redirect('/cotizacion_listall/')
        form = formCOTIZACION(instance=cotizacion)
        ctx = {
            'form': form,
            'state': 'update'
        }
        return render(request, 'home/COTIZACION/cotizacion_update.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def COTIZACION_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cotizacion = COTIZACION.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'cotizacion': cotizacion,
            'product_list': product_list,
        }
        return render(request, 'home/COTIZACION/cotizacion_listone.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/cotizacion_listall/')
    
def COTIZACION_GET_DATA(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cotizacion = COTIZACION.objects.get(id=pk)
        data = {
            'cotizacion': {
                'id': cotizacion.id,
                'CO_CCLIENTE': {
                    'id': cotizacion.CO_CLIENTE.id,
                    'nombre': str(cotizacion.CO_CLIENTE)
                },
                'CO_CNUMERO': cotizacion.CO_CNUMERO,
                'CO_FFECHA': cotizacion.CO_FFECHA.strftime('%Y-%m-%d'),
                'CO_CVALIDO_HASTA': cotizacion.CO_CVALIDO_HASTA.strftime('%Y-%m-%d'),
                'CO_CESTADO': cotizacion.CO_CESTADO,
                'CO_NTOTAL': str(cotizacion.CO_NTOTAL),
                'CO_COBSERVACIONES': cotizacion.CO_COBSERVACIONES,
                'CO_CCOMENTARIO': cotizacion.CO_CCOMENTARIO,

            }
        }
        return JsonResponse(data)
    except COTIZACION.DoesNotExist:
        return JsonResponse({'error': 'Cotización no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)
    
def COTIZACION_LISTONE_FORMAT(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        cotizacion = COTIZACION.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'cotizacion': cotizacion,
            'product_list': product_list,
        }
        return render(request, 'home/COTIZACION/cotizacion_listone_format.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/cotizacion_listall/')

def COTIZACION_GET_LINE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        print("id linea:", pk)
        detalle = COTIZACION_DETALLE.objects.get(id=pk)
        
        data = {
            'id': detalle.id,
            'producto': detalle.CD_PRODUCTO.id,
            'cantidad': detalle.CD_NCANTIDAD,
            'precioUnitario': detalle.CD_NPRECIO_UNITARIO,
            'descuento': detalle.CD_NDESCUENTO
        }
        return JsonResponse(data)
    except COTIZACION_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de cotización no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def COTIZACION_DELETE_LINE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = COTIZACION_DETALLE.objects.get(id=pk)
        cotizacion_id = detalle.CD_COTIZACION.id
        detalle.delete()
        crear_log(request.user, f'Eliminar Línea de Cotización', f'Se eliminó la línea de cotización: {detalle.CD_PRODUCTO}')
        # Recalculate COTIZACION.CO_NTOTAL
        cotizacion = detalle.CD_COTIZACION
        total_cotizacion = COTIZACION_DETALLE.objects.filter(CD_COTIZACION=cotizacion).aggregate(Sum('CD_NTOTAL'))['CD_NTOTAL__sum'] or 0
        cotizacion.CO_NTOTAL = total_cotizacion
        cotizacion.save()
        crear_log(request.user, f'Actualizar Cotización', f'Se actualizó la cotización: {cotizacion.CO_CNUMERO}')
        return JsonResponse({'success': 'Línea de cotización eliminada correctamente', 'cotizacion_id': cotizacion_id})
    except COTIZACION_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de cotización no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def CHECK_CO_NUMERO(request):
    if request.method == 'POST':
        co_numero = request.POST.get('co_numero')
        exists = COTIZACION.objects.filter(CO_CNUMERO=co_numero).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def ORDEN_VENTA_LISTALL(request):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = ORDEN_VENTA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/ORDEN_VENTA/orden_venta_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ORDEN_VENTA_ADDONE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formORDEN_VENTA(request.POST)
            if form.is_valid():
                orden_venta = form.save(commit=False)
                orden_venta.OV_CUSUARIO_CREADOR = request.user
                
                
                
                orden_venta.save()
                
                # Copiar detalles de la cotización si existe
                if orden_venta.OV_COTIZACION:
                    try:
                        cotizacion_detalles = COTIZACION_DETALLE.objects.filter(CD_COTIZACION=orden_venta.OV_COTIZACION)
                        for cotizacion_detalle in cotizacion_detalles:
                            ORDEN_VENTA_DETALLE.objects.create(
                                OVD_ORDEN_VENTA=orden_venta,
                                OVD_PRODUCTO=cotizacion_detalle.CD_PRODUCTO,
                                OVD_NCANTIDAD=cotizacion_detalle.CD_NCANTIDAD,
                                OVD_NPRECIO_UNITARIO=cotizacion_detalle.CD_NPRECIO_UNITARIO,
                                OVD_NSUBTOTAL=cotizacion_detalle.CD_NSUBTOTAL,
                                OVD_NDESCUENTO=cotizacion_detalle.CD_NDESCUENTO,
                                OVD_NTOTAL=cotizacion_detalle.CD_NTOTAL,
                                OVD_CUSUARIO_CREADOR=request.user
                            )
                    except Exception as e:
                        print(f"Error al copiar detalles de cotización: {str(e)}")

                messages.success(request, 'Orden de venta guardada correctamente')
                return redirect('/orden_venta_listall/')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo {field}: {error}')
        else:
            form = formORDEN_VENTA()        
        ctx = {
            'form': form,
            'state': 'add'
        }
        return render(request, 'home/ORDEN_VENTA/orden_venta_addone.html', ctx)
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        messages.error(request, f'Error al procesar la solicitud: {str(e)}')
        return redirect('/')

def get_tipo_cambio_options(request):
    fecha = request.GET.get('fecha')
    if fecha:
        tipos_cambio = TIPO_CAMBIO.objects.filter(TC_FFECHA=fecha)
    else:
        tipos_cambio = TIPO_CAMBIO.objects.none()
    
    options = [{'id': tc.id, 'text': f"{tc.TC_NTASA} - {tc.TC_CMONEDA}"} for tc in tipos_cambio]
    return JsonResponse(options, safe=False)

def ORDEN_VENTA_ADD_LINE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            orden_venta_id = request.POST.get('orden_venta_id')
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            precio_unitario = request.POST.get('precioUnitario')
            descuento = request.POST.get('descuento')

            orden_venta = ORDEN_VENTA.objects.get(id=orden_venta_id)
            producto = PRODUCTO.objects.get(id=producto_id)

            # Ensure cantidad and precio_unitario are at least 1
            cantidad = max(1, int(cantidad or 0))
            precio_unitario = max(Decimal('1'), Decimal(precio_unitario or '0'))

            
            precio_unitario_local = precio_unitario
            descuento_local = Decimal(descuento or '0')

            # Recalculate subtotal in local currency
            subtotal_local = Decimal(cantidad) * precio_unitario_local

            # Ensure descuento is non-negative and not greater than subtotal
            descuento_local = max(Decimal('0'), min(descuento_local, subtotal_local))

            # Recalculate total in local currency
            total_local = subtotal_local - descuento_local

            # Verificar si la combinación de orden de venta y producto ya existe
            existing_detail = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta, OVD_PRODUCTO=producto).first()
            if existing_detail:
                existing_detail.delete()
                crear_log(request.user, f'Eliminar Línea de Orden de Venta', f'Se eliminó la línea de orden de venta: {orden_venta}')

            detalle = ORDEN_VENTA_DETALLE(
                OVD_ORDEN_VENTA=orden_venta,
                OVD_PRODUCTO=producto,
                OVD_NCANTIDAD=cantidad,
                OVD_NPRECIO_UNITARIO=precio_unitario_local,
                OVD_NSUBTOTAL=subtotal_local,
                OVD_NDESCUENTO=descuento_local,
                OVD_NTOTAL=total_local,
                OVD_CUSUARIO_CREADOR=request.user
            )
            crear_log(request.user, f'Crear Línea de Orden de Venta', f'Se creó la línea de orden de venta: {detalle.OVD_PRODUCTO}')
            detalle.save()

            # Recalculate ORDEN_VENTA.OV_NTOTAL
            total_orden_venta_local = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta).aggregate(Sum('OVD_NTOTAL'))['OVD_NTOTAL__sum'] or 0
            orden_venta.OV_NTOTAL = total_orden_venta_local

            

            crear_log(request.user, f'Actualizar Orden de Venta', f'Se actualizó la orden de venta: {orden_venta.OV_CNUMERO}')
            orden_venta.save()

            messages.success(request, 'Línea de orden de venta agregada correctamente')
            return redirect(f'/orden_venta_listone/{orden_venta_id}')
        
        return redirect('/orden_venta_listall/')
    except Exception as e:
        errMsg = f"Error al agregar línea de orden de venta: {str(e)}"
        print(errMsg)
        messages.error(request, errMsg)
        return JsonResponse({'error': str(errMsg)}, status=400)
    
def ORDEN_VENTA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        orden_venta = ORDEN_VENTA.objects.get(id=pk)
        if request.method == 'POST':
            form = formORDEN_VENTA(request.POST, instance=orden_venta)
            if form.is_valid():
                orden_venta = form.save(commit=False)
                orden_venta.OV_CUSUARIO_MODIFICADOR = request.user
                orden_venta.save()
                crear_log(request.user, f'Actualizar Orden de Venta', f'Se actualizó la orden de venta: {orden_venta.OV_CNUMERO}')
                messages.success(request, 'Orden de venta actualizada correctamente')
                return redirect('/orden_venta_listall/')
        form = formORDEN_VENTA(instance=orden_venta)
        ctx = {
            'form': form,
            'state': 'update'
        }
        return render(request, 'home/ORDEN_VENTA/orden_venta_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def ORDEN_VENTA_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        orden_venta = ORDEN_VENTA.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'orden_venta': orden_venta,
            'product_list': product_list,
        }
        return render(request, 'home/ORDEN_VENTA/orden_venta_listone.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/orden_venta_listall/')

def ORDEN_VENTA_GET_DATA(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        orden_venta = ORDEN_VENTA.objects.get(id=pk)
        data = {
            'orden_venta': {
                'id': orden_venta.id,
                'OV_CCLIENTE': {
                    'id': orden_venta.OV_CCLIENTE.id,
                    'nombre': str(orden_venta.OV_CCLIENTE)
                },
                'OV_CNUMERO': orden_venta.OV_CNUMERO,
                'OV_FFECHA': orden_venta.OV_FFECHA.strftime('%Y-%m-%d'),
                'OV_FFECHA_ENTREGA': orden_venta.OV_FFECHA_ENTREGA.strftime('%Y-%m-%d'),
                'OV_CESTADO': orden_venta.OV_CESTADO,
                'OV_NTOTAL': str(orden_venta.OV_NTOTAL),
                'OV_COBSERVACIONES': orden_venta.OV_COBSERVACIONES,
                'OV_CCOMENTARIO': orden_venta.OV_CCOMENTARIO
            }
        }
        return JsonResponse(data)
    except ORDEN_VENTA.DoesNotExist:
        return JsonResponse({'error': 'Orden de venta no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def ORDEN_VENTA_LISTONE_FORMAT(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        orden_venta = ORDEN_VENTA.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'orden_venta': orden_venta,
            'product_list': product_list,
        }
        return render(request, 'home/ORDEN_VENTA/orden_venta_listone_format.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/orden_venta_listall/')

def ORDEN_VENTA_GET_LINE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        print("id linea:", pk)
        detalle = ORDEN_VENTA_DETALLE.objects.get(id=pk)
        
        data = {
            'id': detalle.id,
            'producto': detalle.OVD_PRODUCTO.id,
            'cantidad': detalle.OVD_NCANTIDAD,
            'precioUnitario': detalle.OVD_NPRECIO_UNITARIO,
            'descuento': detalle.OVD_NDESCUENTO
        }
        return JsonResponse(data)
    except ORDEN_VENTA_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de orden de venta no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def ORDEN_VENTA_DELETE_LINE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = ORDEN_VENTA_DETALLE.objects.get(id=pk)
        orden_venta_id = detalle.OVD_ORDEN_VENTA.id
        detalle.delete()
        crear_log(request.user, f'Eliminar Línea de Orden de Venta', f'Se eliminó la línea de orden de venta: {detalle.OVD_ORDEN_VENTA}')
        # Recalculate ORDEN_VENTA.OV_NTOTAL
        orden_venta = detalle.OVD_ORDEN_VENTA
        total_orden_venta = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta).aggregate(Sum('OVD_NTOTAL'))['OVD_NTOTAL__sum'] or 0
        orden_venta.OV_NTOTAL = total_orden_venta
        orden_venta.save()
        crear_log(request.user, f'Actualizar Orden de Venta', f'Se actualizó la orden de venta: {orden_venta.OV_CNUMERO}')
        return JsonResponse({'success': 'Línea de orden de venta eliminada correctamente', 'orden_venta_id': orden_venta_id})
    except ORDEN_VENTA_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de orden de venta no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def CHECK_OV_NUMERO(request):
    if request.method == 'POST':
        ov_numero = request.POST.get('ov_numero')
        exists = ORDEN_VENTA.objects.filter(OV_CNUMERO=ov_numero).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def FACTURA_LISTALL(request):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = FACTURA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/FACTURA/factura_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def FACTURA_ADDONE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formFACTURA(request.POST)
            if form.is_valid():
                factura = form.save(commit=False)
                factura.FA_CUSUARIO_CREADOR = request.user
                
                
                
                factura.save()
                
                # Copiar detalles de la orden de venta si existe
                if factura.FA_CORDEN_VENTA:
                    try:
                        orden_venta_detalles = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=factura.FA_CORDEN_VENTA)
                        for orden_venta_detalle in orden_venta_detalles:
                            FACTURA_DETALLE.objects.create(
                                FAD_FACTURA=factura,
                                FAD_PRODUCTO=orden_venta_detalle.OVD_PRODUCTO,
                                FAD_NCANTIDAD=orden_venta_detalle.OVD_NCANTIDAD,
                                FAD_NPRECIO_UNITARIO=orden_venta_detalle.OVD_NPRECIO_UNITARIO,
                                FAD_NSUBTOTAL=orden_venta_detalle.OVD_NSUBTOTAL,
                                FAD_NDESCUENTO=orden_venta_detalle.OVD_NDESCUENTO,
                                FAD_NTOTAL=orden_venta_detalle.OVD_NTOTAL,
                                FAD_CUSUARIO_CREADOR=request.user
                            )
                        crear_log(request.user, f'Crear Líneas de Factura', f'Se crearon las líneas de factura para: {factura.FA_CNUMERO}')
                    except Exception as e:
                        print(f"Error al copiar detalles de orden de venta: {str(e)}")

                messages.success(request, 'Factura guardada correctamente')
                return redirect('/factura_listall/')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Error en el campo {field}: {error}')
        else:
            form = formFACTURA()
        ctx = {
            'form': form,
            'state': 'add'
        }
        return render(request, 'home/FACTURA/factura_addone.html', ctx)
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        messages.error(request, f'Error al procesar la solicitud: {str(e)}')
        return redirect('/')
    
def FACTURA_ADD_LINE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            factura_id = request.POST.get('factura_id')
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            precio_unitario = request.POST.get('precioUnitario')
            descuento = request.POST.get('descuento')

            factura = FACTURA.objects.get(id=factura_id)
            producto = PRODUCTO.objects.get(id=producto_id)

            # Ensure cantidad and precio_unitario are at least 1
            cantidad = max(1, int(cantidad or 0))
            precio_unitario = max(Decimal('1'), Decimal(precio_unitario or '0'))

            
            precio_unitario_local = precio_unitario
            descuento_local = Decimal(descuento or '0')

            # Recalculate subtotal in local currency
            subtotal_local = Decimal(cantidad) * precio_unitario_local

            # Ensure descuento is non-negative and not greater than subtotal
            descuento_local = max(Decimal('0'), min(descuento_local, subtotal_local))

            # Recalculate total in local currency
            total_local = subtotal_local - descuento_local

            # Verificar si la combinación de factura y producto ya existe
            existing_detail = FACTURA_DETALLE.objects.filter(FAD_FACTURA=factura, FAD_PRODUCTO=producto).first()
            if existing_detail:
                existing_detail.delete()
                crear_log(request.user, f'Eliminar Línea de Factura', f'Se eliminó la línea de factura: {factura}')

            detalle = FACTURA_DETALLE(
                FAD_FACTURA=factura,
                FAD_PRODUCTO=producto,
                FAD_NCANTIDAD=cantidad,
                FAD_NPRECIO_UNITARIO=precio_unitario_local,
                FAD_NSUBTOTAL=subtotal_local,
                FAD_NDESCUENTO=descuento_local,
                FAD_NTOTAL=total_local,
                FAD_CUSUARIO_CREADOR=request.user
            )
            crear_log(request.user, f'Crear Línea de Factura', f'Se creó la línea de factura: {detalle.FAD_PRODUCTO}')
            detalle.save()

            # Recalculate FACTURA.FA_NTOTAL
            total_factura_local = FACTURA_DETALLE.objects.filter(FAD_FACTURA=factura).aggregate(Sum('FAD_NTOTAL'))['FAD_NTOTAL__sum'] or 0
            factura.FA_NTOTAL = total_factura_local

            

            crear_log(request.user, f'Actualizar Factura', f'Se actualizó la factura: {factura.FA_CNUMERO}')
            factura.save()

            messages.success(request, 'Línea de factura agregada correctamente')
            return redirect(f'/factura_listone/{factura_id}')
        
        return redirect('/factura_listall/')
    except Exception as e:
        errMsg = f"Error al agregar línea de factura: {str(e)}"
        print(errMsg)
        messages.error(request, errMsg)
        return JsonResponse({'error': str(errMsg)}, status=400)
    
def FACTURA_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        factura = FACTURA.objects.get(id=pk)
        if request.method == 'POST':
            form = formFACTURA(request.POST, instance=factura)
            if form.is_valid():
                factura = form.save(commit=False)
                factura.FA_CUSUARIO_MODIFICADOR = request.user
                factura.save()
                crear_log(request.user, f'Actualizar Factura', f'Se actualizó la factura: {factura.FA_CNUMERO}')
                messages.success(request, 'Factura actualizada correctamente')
                return redirect('/factura_listall/')
        form = formFACTURA(instance=factura)
        ctx = {
            'form': form,
            'state': 'update'
        }
        return render(request, 'home/FACTURA/factura_update.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def FACTURA_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        factura = FACTURA.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'factura': factura,
            'product_list': product_list,
        }
        return render(request, 'home/FACTURA/factura_listone.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/factura_listall/')

def FACTURA_LISTONE_FORMAT(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        factura = FACTURA.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'factura': factura,
            'product_list': product_list,
        }
        return render(request, 'home/FACTURA/factura_listone_format.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/factura_listall/')

def FACTURA_GET_LINE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        print("id linea:", pk)
        detalle = FACTURA_DETALLE.objects.get(id=pk)
        
        data = {
            'id': detalle.id,
            'producto': detalle.FAD_PRODUCTO.id,
            'cantidad': detalle.FAD_NCANTIDAD,
            'precioUnitario': detalle.FAD_NPRECIO_UNITARIO,
            'descuento': detalle.FAD_NDESCUENTO
        }
        return JsonResponse(data)
    except FACTURA_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de factura no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def FACTURA_DELETE_LINE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = FACTURA_DETALLE.objects.get(id=pk)
        factura_id = detalle.FAD_FACTURA.id
        detalle.delete()
        crear_log(request.user, f'Eliminar Línea de Factura', f'Se eliminó la línea de factura: {detalle.FAD_FACTURA}')
        # Recalculate FACTURA.FA_NTOTAL
        factura = detalle.FAD_FACTURA
        total_factura = FACTURA_DETALLE.objects.filter(FAD_FACTURA=factura).aggregate(Sum('FAD_NTOTAL'))['FAD_NTOTAL__sum'] or 0
        factura.FA_NTOTAL = total_factura
        factura.save()
        crear_log(request.user, f'Actualizar Factura', f'Se actualizó la factura: {factura.FA_CNUMERO}')
        return JsonResponse({'success': 'Línea de factura eliminada correctamente', 'factura_id': factura_id})
    except FACTURA_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de factura no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def CHECK_FA_NUMERO(request):
    if request.method == 'POST':
        fa_numero = request.POST.get('fa_numero')
        exists = FACTURA.objects.filter(FA_CNUMERO=fa_numero).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# def ORDEN_VENTA_LISTALL(request):
#     try:
#         object_list = ORDEN_VENTA.objects.all()
#         ctx = {
#             'object_list': object_list
#         }
#         return render(request, 'home/ORDEN_VENTA/orden_venta_listall.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')

# def ORDEN_VENTA_ADDONE(request):
#     try:
#         if request.method == 'POST':
#             form = formORDEN_VENTA(request.POST)
#             if form.is_valid():
#                 print("form is valid")
#                 orden_venta = form.save(commit=False)
#                 orden_venta.OV_CUSUARIO_CREADOR = request.user
#                 orden_venta.save()
#                 crear_log(request.user, f'Crear Orden de Venta', f'Se creó la orden de venta: {orden_venta.OV_CNUMERO}')
#                 print("orden_venta saved")
#                 # If there's a related cotización, copy its details
#                 if orden_venta.OV_COTIZACION:
#                     print("orden_venta.OV_COTIZACION:", orden_venta.OV_COTIZACION)
#                     try:
#                         cotizacion_detalles = COTIZACION_DETALLE.objects.filter(CD_COTIZACION=orden_venta.OV_COTIZACION)
#                         for cotizacion_detalle in cotizacion_detalles:
#                             ORDEN_VENTA_DETALLE.objects.create(
#                                 OVD_ORDEN_VENTA=orden_venta,
#                                 OVD_PRODUCTO=cotizacion_detalle.CD_PRODUCTO,
#                                 OVD_NCANTIDAD=cotizacion_detalle.CD_NCANTIDAD,
#                                 OVD_NPRECIO_UNITARIO=cotizacion_detalle.CD_NPRECIO_UNITARIO,
#                                 OVD_NSUBTOTAL=cotizacion_detalle.CD_NSUBTOTAL,
#                                 OVD_NDESCUENTO=cotizacion_detalle.CD_NDESCUENTO,
#                                 OVD_NTOTAL=cotizacion_detalle.CD_NTOTAL,
#                                 OVD_CUSUARIO_CREADOR=request.user
#                             )
#                             crear_log(request.user, f'Crear Línea de Orden de Venta', f'Se creó la línea de orden de venta: {cotizacion_detalle.CD_PRODUCTO}')
#                     except Exception as e:
#                         print(f"Error al copiar detalles de cotización: {str(e)}")

#                 messages.success(request, 'Orden de venta guardada correctamente')
#                 return redirect('/orden_venta_listall/')
#             else:
#                 print("Form is not valid. Errors:", form.errors)
#                 return HttpResponse(form.errors.as_text())
#         form = formORDEN_VENTA()
#         ctx = {
#             'form': form
#         }
#         return render(request, 'home/ORDEN_VENTA/orden_venta_addone.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')
    
# def ORDEN_VENTA_ADD_LINE(request):
#     try:
#         if request.method == 'POST':

#             orden_venta_id = request.POST.get('orden_venta_id')
#             producto_id = request.POST.get('producto')
#             cantidad = request.POST.get('cantidad')
#             precio_unitario = request.POST.get('precioUnitario')
#             descuento = request.POST.get('descuento')

#             # Ensure cantidad and precio_unitario are at least 1
#             cantidad = max(1, int(cantidad or 0))
#             precio_unitario = max(Decimal('1'), Decimal(precio_unitario or '0'))

#             # Recalculate subtotal
#             subtotal = Decimal(cantidad) * precio_unitario

#             # Ensure descuento is non-negative and not greater than subtotal
#             descuento = max(Decimal('0'), min(Decimal(descuento or '0'), subtotal))

#             orden_venta = ORDEN_VENTA.objects.get(id=orden_venta_id)
#             producto = PRODUCTO.objects.get(id=producto_id)

#             subtotal = Decimal(cantidad) * Decimal(precio_unitario)
#             total = subtotal - Decimal(descuento)

#             # Verificar si la combinación de orden de venta y producto ya existe
#             existing_detail = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta, OVD_PRODUCTO=producto).first()
#             if existing_detail:
#                 existing_detail.delete()

#             # Recalculate total
#             total = subtotal - descuento

#             detalle = ORDEN_VENTA_DETALLE(
#                 OVD_ORDEN_VENTA=orden_venta,
#                 OVD_PRODUCTO=producto,
#                 OVD_NCANTIDAD=cantidad,
#                 OVD_NPRECIO_UNITARIO=precio_unitario,
#                 OVD_NSUBTOTAL=subtotal,
#                 OVD_NDESCUENTO=descuento,
#                 OVD_NTOTAL=total,
#                 OVD_CUSUARIO_CREADOR=request.user
#             )
#             detalle.save()
#             crear_log(request.user, f'Crear Línea de Orden de Venta', f'Se creó la línea de orden de venta: {orden_venta}')
#             # Recalculate ORDEN_VENTA.OV_NTOTAL
#             total_orden_venta = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta).aggregate(Sum('OVD_NTOTAL'))['OVD_NTOTAL__sum'] or 0
#             orden_venta.OV_NTOTAL = total_orden_venta
#             orden_venta.save()

#             messages.success(request, 'Línea de orden de venta agregada correctamente')
#             return redirect(f'/orden_venta_listone/{orden_venta_id}')
        
#         return redirect('/orden_venta_listall/')
#     except Exception as e:
#         errMsg=print(f"Error al agregar línea de orden de venta: {str(e)}")
#         messages.error(request, errMsg)
#         return JsonResponse({'error': str(errMsg)}, status=400)

# def ORDEN_VENTA_UPDATE(request, pk):
#     try:
#         orden_venta = ORDEN_VENTA.objects.get(id=pk)
#         if request.method == 'POST':
#             form = formORDEN_VENTA(request.POST, instance=orden_venta)
#             if form.is_valid():
#                 orden_venta = form.save(commit=False)
#                 orden_venta.OV_CUSUARIO_MODIFICADOR = request.user
#                 orden_venta.save()
#                 crear_log(request.user, f'Actualizar Orden de Venta', f'Se actualizó la orden de venta: {orden_venta.OV_CNUMERO}')
#                 messages.success(request, 'Orden de venta actualizada correctamente')
#                 return redirect('/orden_venta_listall/')
#         form = formORDEN_VENTA(instance=orden_venta)
#         ctx = {
#             'form': form
#         }
#         return render(request, 'home/ORDEN_VENTA/orden_venta_update.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')

# def ORDEN_VENTA_LISTONE(request, pk):
#     try:
#         orden_venta = ORDEN_VENTA.objects.get(id=pk)
#         product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
#         ctx = {
#             'orden_venta': orden_venta,
#             'product_list': product_list,
#         }
#         return render(request, 'home/ORDEN_VENTA/orden_venta_listone.html', ctx)
#     except Exception as e:
#         print("ERROR:", e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/orden_venta_listall/')

# def ORDEN_VENTA_LISTONE_FORMAT(request, pk):
#     try:
#         orden_venta = ORDEN_VENTA.objects.get(id=pk)
#         product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
#         ctx = {
#             'orden_venta': orden_venta,
#             'product_list': product_list,
#         }
#         return render(request, 'home/ORDEN_VENTA/orden_venta_listone_format.html', ctx)
#     except Exception as e:
#         print("ERROR:", e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/orden_venta_listall/')

# def ORDEN_VENTA_GET_LINE(request, pk):
#     try:
#         print("id linea:", pk)
#         detalle = ORDEN_VENTA_DETALLE.objects.get(id=pk)
        
#         data = {
#             'id': detalle.id,
#             'producto': detalle.OVD_PRODUCTO.id,
#             'cantidad': detalle.OVD_NCANTIDAD,
#             'precioUnitario': detalle.OVD_NPRECIO_UNITARIO,
#             'descuento': detalle.OVD_NDESCUENTO
#         }
#         return JsonResponse(data)
#     except ORDEN_VENTA_DETALLE.DoesNotExist:
#         return JsonResponse({'error': 'Línea de orden de venta no encontrada'}, status=404)
#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({'error': str(e)}, status=500)

# def ORDEN_VENTA_DELETE_LINE(request, pk):
#     try:
#         detalle = ORDEN_VENTA_DETALLE.objects.get(id=pk)
#         orden_venta_id = detalle.OVD_ORDEN_VENTA.id
#         detalle.delete()
#         crear_log(request.user, f'Eliminar Línea de Orden de Venta', f'Se eliminó la línea de orden de venta: {detalle.OVD_PRODUCTO}')
#         # Recalculate ORDEN_VENTA.OV_NTOTAL
#         orden_venta = detalle.OVD_ORDEN_VENTA
#         total_orden_venta = ORDEN_VENTA_DETALLE.objects.filter(OVD_ORDEN_VENTA=orden_venta).aggregate(Sum('OVD_NTOTAL'))['OVD_NTOTAL__sum'] or 0
#         orden_venta.OV_NTOTAL = total_orden_venta
#         orden_venta.save()
#         crear_log(request.user, f'Actualizar Orden de Venta', f'Se actualizó la orden de venta: {orden_venta.OV_CNUMERO}')
#         return JsonResponse({'success': 'Línea de orden de venta eliminada correctamente', 'orden_venta_id': orden_venta_id})
#     except ORDEN_VENTA_DETALLE.DoesNotExist:
#         return JsonResponse({'error': 'Línea de orden de venta no encontrada'}, status=404)
#     except Exception as e:
#         print("ERROR:", e)
#         return JsonResponse({'error': str(e)}, status=500)

# def CHECK_OV_NUMERO(request):
#     if request.method == 'POST':
#         ov_numero = request.POST.get('ov_numero')
#         exists = ORDEN_VENTA.objects.filter(OV_CNUMERO=ov_numero).exists()
#         return JsonResponse({'exists': exists})
#     return JsonResponse({'error': 'Invalid request method'}, status=400)

#--------------------------------------
#------------QUERY MANAGER-------------
#--------------------------------------
def QUERY_LISTALL(request):
    if not has_auth(request.user, 'VER_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        queries = QUERY.objects.filter(QR_NHABILITADO = True)
        ctx = {
            "object_list": queries
        }
        return render(request, 'home/QUERY_MANAGER/query_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/')
    
def QUERY_ADDONE(request):
    if not has_auth(request.user, 'ADD_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formQUERY(request.POST)
            if form.is_valid():
                form.cleaned_data["USER_CREATOR_ID"] = request.user
                form.cleaned_data["USER_UPD_ID"] = request.user
                form.save()
                crear_log(request.user, f'Crear Query', f'Se creó la query: {form.cleaned_data["QR_CNOMBRE"]}')
                messages.success(request, 'Query agregada correctamente')
                return redirect('/query_listall/')
        form = formQUERY()
        ctx = {
            "form": form
        }
        return render(request, 'home/QUERY_MANAGER/query_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/query_listall/')

def QUERY_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        query = QUERY.objects.get(id = pk)
        if request.method == 'POST':
            form = formQUERY(request.POST, instance=query)
            if form.is_valid():
                form.cleaned_data["USER_UPD_ID"] = request.user
                form.save()
                crear_log(request.user, f'Actualizar Query', f'Se actualizó la query: {form.cleaned_data["QR_CNOMBRE"]}')
                messages.success(request, 'Query actualizada correctamente')
                return redirect('/query_listall/')
        form = formQUERY(instance=query)
        ctx = {
            "form": form,
            "object": query
        }
        return render(request, 'home/QUERY_MANAGER/query_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/query_listall/')

def QUERY_LISTONE(request):
    if not has_auth(request.user, 'VER_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        pass
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'valid': False, 'error': str(e)})
    
def QUERY_RUN(request, pk):
    if not has_auth(request.user, 'VER_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        query = QUERY.objects.get(id = pk)

        lstParamctx=[]
        documentos = []
        lstParam=getQueryParam(query.QR_CQUERY)
        cantidad_documentos = 0

        if lstParam!=None:
            print("Estos son los parametros de la consulta",lstParam)
            for param in lstParam:
                try:
                    print("param",param)
                    tipo=param.split(";")[0].replace('[','').replace("'","")[0]
                    nombre=param.split(";")[0].replace('[','').replace("'","")
                    etiqueta=param.split(";")[1].replace('[','').replace("'","")
                    valor=param.split(";")[2].replace(']','').replace("'","")
                    datalst=[]
                    if tipo=='L':
                        datalst,qCols,cMsgRet = run_query_sql(valor)
                        lstParamctx.append([tipo,nombre,etiqueta,json.dumps(datalst)])    
                    else:
                        lstParamctx.append([tipo,nombre,etiqueta,valor])    
                except Exception as e:
                    print(e)

            if documentos:
                cantidad_documentos = len(documentos)
            context = {
                        'lstParamctx':lstParamctx,
                        'id_query':pk,
                        'documentos':documentos,
                        'cantidad_documentos':cantidad_documentos
                    }
            return render(request,'home/QUERY_MANAGER/query_listone_param.html',context)


        else:
            documentos = []
            listado,qCols,cMsgRet = run_query_sql(query.QR_CQUERY)
            for linea in listado:
                for dato in linea:
                    try:
                        if dato.__contains__('https://labbe-files.s3.amazonaws.com'):
                            documentos.append(dato)
                    except Exception as e:
                        next
            if documentos:
                cantidad_documentos = len(documentos)
            if listado!=False:
                if query.QR_CLABEL_FIELDS != None and query.QR_CLABEL_FIELDS != '':
                    lCols = query.QR_CLABEL_FIELDS.split(",")
                    if lCols[0]=='*':
                        lCols.clear()
                else:
                    lCols = []
                if len(lCols)<qCols:
                    nCols = range(qCols-len(lCols))
                    for n in nCols:
                        lCols.append(f"Columna {str(n+1)}")
                
                context = {
                    'listado':listado,
                    'qcols':range(qCols),
                    'lcols':lCols,
                    'id_query':pk,
                    'documentos':documentos,
                    'cantidad_documentos':cantidad_documentos
                }
                return render(request,'home/QUERY_MANAGER/query_listone_param.html',context)
            else:
                listado=[]
                documentos = []
                lstmsg=[]
                lstmsg.append(cMsgRet+'\n Edite y vuelva a intentar')

                listado.append(lstmsg)
                qCols=1
                lCols=[]
                lCols.append('Descripción del error')
                context = {
                    'listado':listado,
                    'qcols':range(qCols),
                    'lcols':lCols,
                    'id_query':pk,
                    'documentos':documentos
                }
                return render(request,'home/QUERY_MANAGER/query_listone.html',context)
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/query_listall/')

def QUERY_DELETE(request, pk):
    if not has_auth(request.user, 'UPD_QUERYS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        query = QUERY.objects.get(id = pk)
        query.QR_NHABILITADO = False
        query.USER_UPD_ID = request.user
        query.save()
        crear_log(request.user, f'Eliminar Query', f'Se eliminó la query: {query.QR_CNOMBRE}')
        messages.success(request, 'Query eliminada correctamente')
        return redirect('/query_listall/')
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/query_listall/')
    
def run_query_param(request):
    try:
        id = request.POST.get('id')
        query = QUERY.objects.get(id=id)
        tableData = json.loads(request.POST.get('tableData'))

        for data in tableData:        
            if data[0]!=None and str(data[0]).strip()!="":
                query.QR_CQUERY = query.QR_CQUERY.replace(f"[%{data[0]}]",data[1])
        
        print(query.QR_CQUERY)
        listado,qCols,cMsgRet = run_query_sql(query.QR_CQUERY)

        if listado!=False:
            if query.QR_CLABEL_FIELDS != None and query.QR_CLABEL_FIELDS != '':
                lCols = query.QR_CLABEL_FIELDS.split(",")
                if lCols[0]=='*':
                    lCols.clear()
            else:
                lCols = []
            if len(lCols)<qCols:
                nCols = range(qCols-len(lCols))
                for n in nCols:
                    lCols.append(f"Columna {str(n+1)}")
            
            context = {
                'listado':listado,
                'qcols':list(range(qCols)),
                'lcols':lCols,
                'id_query':id
            }
            #return render(request,'home/query_listone.html',context)
            return JsonResponse(context,safe=False)
        else:
            listado=[]
            lstmsg=[]
            lstmsg.append(cMsgRet+'\n Edite y vuelva a intentar')

            listado.append(lstmsg)
            qCols=1
            lCols=[]
            lCols.append('Descripción del error')
            context = {
                'listado':listado,
                'qcols':list(range(qCols)),
                'lcols':lCols,
                'id_query':id
            }
            return JsonResponse(context,safe=False)
    except Exception as e:
        print(e)
        messages.error(request, 'Error: ' + str(e))
        return redirect('/query_listall/')

def getQueryParam(sql_query):

    try:       
        # Define a regular expression pattern to match the entire list inside comments
        pattern = r'\{(.*?)\}'

        # Use re.search to find the pattern in the SQL query
        match = re.search(pattern, str(sql_query), re.DOTALL)

        # Check if a match is found
        print(match)
        if match:
            # Extract the matched list
            comment_list = match.group(1)
            
            # Split the comment list into individual items
            list_items = comment_list.split(':')

            # Remove leading and trailing spaces from each item and display them
            cleaned_items = [item.strip() for item in list_items]
            
            # Display the cleaned list items
            lstParam=[]
            for item in cleaned_items:
                lstParam.append(item)
            return lstParam
        else:
            print("No hay parametros para la consulta")
            return None
    except Exception as e:
        print(e)
        return None

def run_query_sql(query):
    try:
        with connection.cursor() as cursor:

            if query.lower().find('insert') != -1:
                # NO SE PUEDE
                print('CONTIENE insert!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('update') != -1:
                # NO SE PUEDE
                print('CONTIENE update!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('delete') != -1:
                # NO SE PUEDE
                print('CONTIENE delete!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('cursor') != -1:
                # NO SE PUEDE
                print('CONTIENE CURSOR!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('execute') != -1:
                # NO SE PUEDE
                print('CONTIENE EXECUTE!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.find('drop') != -1:
                # NO SE PUEDE
                print('CONTIENE DROP!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('create') != -1:
                # NO SE PUEDE
                print('CONTIENE CREATE!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'
            if query.lower().find('alter') != -1:
                # NO SE PUEDE
                print('CONTIENE ALTER!!!!')
                return False, 0, 'La consulta contiene elementos reservados, no se ejecutará'

            cquery = f'''{query} 
                        '''
            cursor.execute(cquery)
            resultado = cursor.fetchall()
            if resultado == None:
                resultado = False, 0, ''
            qCol = len(resultado[0])
            return resultado, qCol, ''
    except Exception as e:
        return False, 0, str(e)
#--------------------------------------
#------------QUERY MANAGER-------------
#--------------------------------------

def BOLETA_GARANTIA_LISTALL(request):
    try:
        object_list = BOLETA_GARANTIA.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/BOLETA_GARANTIA/boletagarantia_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def BOLETA_GARANTIA_ADDONE(request):
    try:
        if request.method == 'POST':
            form = formBOLETA_GARANTIA(request.POST, request.FILES)
            if form.is_valid():
                boleta = form.save(commit=False)
                boleta.BG_CUSUARIO_CREADOR = request.user
                boleta.save()
                messages.success(request, 'Boleta de garantía guardada correctamente')
                return redirect('/boletagarantia_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')
        else:
            form = formBOLETA_GARANTIA()
        
        
        
        ctx = {
            'form': form,
        }
        return render(request, 'home/BOLETA_GARANTIA/boletagarantia_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def BOLETA_GARANTIA_UPDATE(request, pk):
    try:
        boleta_garantia = BOLETA_GARANTIA.objects.get(id=pk)
        if request.method == 'POST':
            form = formBOLETA_GARANTIA(request.POST, instance=boleta_garantia)
            if form.is_valid():
                form.save()
                messages.success(request, 'Boleta de garantía actualizada correctamente')
                return redirect('/boletagarantia_listall/')
        form = formBOLETA_GARANTIA(instance=boleta_garantia)
        ctx = {
            'form': form
        }
        return render(request, 'home/BOLETA_GARANTIA/boletagarantia_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EDP_LISTALL(request):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = ESTADO_DE_PAGO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/ESTADO_DE_PAGO/edp_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EDP_ADDONE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formESTADO_DE_PAGO(request.POST)
            if form.is_valid():
                edp = form.save(commit=False)
                edp.EP_CUSUARIO_CREADOR = request.user
                edp.save()
                crear_log(request.user, f'Crear Estado de Pago', f'Se creó el Estado de Pago: {edp.EP_CNUMERO}')
                messages.success(request, 'Estado de Pago guardado correctamente')
                return redirect('/edp_listall/')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario.')
        else:
            form = formESTADO_DE_PAGO()
        
       
        
        ctx = {
            'form': form,
            'state': 'add',
        }
        return render(request, 'home/ESTADO_DE_PAGO/edp_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')
def EDP_UPDATE(request, pk):
    if not has_auth(request.user, 'EDITAR_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        edp = ESTADO_DE_PAGO.objects.get(id=pk)
        if request.method == 'POST':
            form = formESTADO_DE_PAGO(request.POST, instance=edp)
            if form.is_valid():
                edp = form.save(commit=False)
                edp.EP_CUSUARIO_MODIFICADOR = request.user
                edp.save()
                crear_log(request.user, f'Editar Estado de Pago', f'Se editó el Estado de Pago: {edp.EP_CNUMERO}')
                messages.success(request, 'Estado de Pago actualizado correctamente')
                return redirect('/edp_listall/')
        form = formESTADO_DE_PAGO(instance=edp)
        ctx = {
            'form': form,
            'state': 'update'
        }
        return render(request, 'home/ESTADO_DE_PAGO/edp_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def EDP_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        edp = ESTADO_DE_PAGO.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        

        ctx = {
            'edp': edp,
            'product_list': product_list,
            
        }
        return render(request, 'home/ESTADO_DE_PAGO/edp_listone.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/edp_listall/')
    
def EDP_LISTONE_FORMAT(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        edp = ESTADO_DE_PAGO.objects.get(id=pk)
        product_list = list(PRODUCTO.objects.filter(PR_BACTIVO=True).values_list('id', 'PR_CNOMBRE'))
        
        ctx = {
            'edp': edp,
            'product_list': product_list,
        }
        return render(request, 'home/ESTADO_DE_PAGO/edp_listone_format.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/edp_listall/')
    
def EDP_GET_LINE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        print("id línea:", pk)
        detalle = ESTADO_DE_PAGO_DETALLE.objects.get(id=pk)
        
        data = {
            'id': detalle.id,
            'producto': detalle.EDD_PRODUCTO.id,
            'cantidad': detalle.EDD_NCANTIDAD,
            'precioUnitario': detalle.EDD_NPRECIO_UNITARIO,
            'descuento': detalle.EDD_NDESCUENTO
        }
        return JsonResponse(data)
    except ESTADO_DE_PAGO_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de estado de pago no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def EDP_ADD_LINE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            edp_id = request.POST.get('edp_id')
            producto_id = request.POST.get('producto')
            cantidad = request.POST.get('cantidad')
            precio_unitario = request.POST.get('precioUnitario')
            descuento = request.POST.get('descuento')

            # Ensure cantidad and precio_unitario are at least 1
            cantidad = max(1, int(cantidad or 0))
            precio_unitario = max(Decimal('1'), Decimal(precio_unitario or '0'))

            # Recalculate subtotal
            subtotal = Decimal(cantidad) * precio_unitario

            # Ensure descuento is non-negative and not greater than subtotal
            descuento = max(Decimal('0'), min(Decimal(descuento or '0'), subtotal))

            edp = ESTADO_DE_PAGO.objects.get(id=edp_id)
            producto = PRODUCTO.objects.get(id=producto_id)

            subtotal = Decimal(cantidad) * Decimal(precio_unitario)
            total = subtotal - Decimal(descuento)

            # Verificar si la combinación de estado de pago y producto ya existe
            existing_detail = ESTADO_DE_PAGO_DETALLE.objects.filter(EDD_ESTADO_DE_PAGO=edp, EDD_PRODUCTO=producto).first()
            if existing_detail:
                existing_detail.delete()

            # Recalculate total
            total = subtotal - descuento

            detalle = ESTADO_DE_PAGO_DETALLE(
                EDD_ESTADO_DE_PAGO=edp,
                EDD_PRODUCTO=producto,
                EDD_NCANTIDAD=cantidad,
                EDD_NPRECIO_UNITARIO=precio_unitario,
                EDD_NSUBTOTAL=subtotal,
                EDD_NDESCUENTO=descuento,
                EDD_NTOTAL=total,
                EDD_CUSUARIO_CREADOR=request.user
            )
            crear_log(request.user, f'Crear Línea de Estado de Pago', f'Se creó la línea de estado de pago: {detalle.EDD_PRODUCTO}')
            detalle.save()

            # Recalculate ESTADO_DE_PAGO.EP_NTOTAL
            total_edp = ESTADO_DE_PAGO_DETALLE.objects.filter(EDD_ESTADO_DE_PAGO=edp).aggregate(Sum('EDD_NTOTAL'))['EDD_NTOTAL__sum'] or 0
            edp.EP_NTOTAL = total_edp
            crear_log(request.user, f'Actualizar Estado de Pago', f'Se actualizó el estado de pago: {edp.EP_CNUMERO}')
            edp.save()

            messages.success(request, 'Línea de estado de pago agregada correctamente')
            return redirect(f'/edp_listone/{edp_id}')
        
        return redirect('/edp_listall/')
    except Exception as e:
        errMsg=print(f"Error al agregar línea de estado de pago: {str(e)}")
        messages.error(request, errMsg)
        return JsonResponse({'error': str(errMsg)}, status=400)

def EDP_DELETE_LINE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = ESTADO_DE_PAGO_DETALLE.objects.get(id=pk)
        edp_id = detalle.EDD_ESTADO_DE_PAGO.id
        detalle.delete()
        crear_log(request.user, f'Eliminar Línea de Estado de Pago', f'Se eliminó la línea de estado de pago: {detalle.EDD_PRODUCTO}')
        # Recalculate ESTADO_DE_PAGO.EP_NTOTAL
        total_edp = ESTADO_DE_PAGO_DETALLE.objects.filter(EDD_ESTADO_DE_PAGO=detalle.EDD_ESTADO_DE_PAGO).aggregate(Sum('EDD_NTOTAL'))['EDD_NTOTAL__sum'] or 0
        detalle.EDD_ESTADO_DE_PAGO.EP_NTOTAL = total_edp
        crear_log(request.user, f'Actualizar Estado de Pago', f'Se actualizó el estado de pago: {detalle.EDD_ESTADO_DE_PAGO.EP_CNUMERO}')
        detalle.EDD_ESTADO_DE_PAGO.save()
        return JsonResponse({'success': 'Línea de estado de pago eliminada correctamente', 'edp_id': edp_id})
    except ESTADO_DE_PAGO_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Línea de estado de pago no encontrada'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def CHECK_EDP_NUMERO(request):
    if request.method == 'POST':
        edp_numero = request.POST.get('edp_numero')
        exists = ESTADO_DE_PAGO.objects.filter(EP_CNUMERO=edp_numero).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def UNIDAD_NEGOCIO_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        unidades_negocio = UNIDAD_NEGOCIO.objects.all()
        ctx = {
            'unidades_negocio': unidades_negocio
        }
        return render(request, 'home/UNIDAD_NEGOCIO/un_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def UNIDAD_NEGOCIO_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formUNIDAD_NEGOCIO(request.POST)
            if form.is_valid():
                unidad_negocio = form.save(commit=False)
                unidad_negocio.UN_CUSUARIO_CREADOR = request.user
                unidad_negocio.save()
                crear_log(request.user, 'Crear Unidad de Negocio', f'Se creó la unidad de negocio: {unidad_negocio.UN_CCODIGO}')
                messages.success(request, 'Unidad de negocio guardada correctamente')
                return redirect('/un_listall/')
        form = formUNIDAD_NEGOCIO()
        ctx = {
            'form': form
        }
        return render(request, 'home/UNIDAD_NEGOCIO/un_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def UNIDAD_NEGOCIO_UPDATE(request, pk):
    if not has_auth(request.user, 'UPDATE_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        unidad_negocio = UNIDAD_NEGOCIO.objects.get(pk=pk)
        if request.method == 'POST':
            form = formUNIDAD_NEGOCIO(request.POST, instance=unidad_negocio)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Unidad de Negocio', f'Se actualizó la unidad de negocio: {unidad_negocio.UN_CCODIGO}')
                messages.success(request, 'Unidad de negocio actualizada correctamente')
                return redirect('/un_listall/')
        else:
            form = formUNIDAD_NEGOCIO(instance=unidad_negocio)
        ctx = {
            'form': form,
            'unidad_negocio': unidad_negocio
        }
        return render(request, 'home/UNIDAD_NEGOCIO/un_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def FC_LISTALL(request):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = FICHA_CIERRE.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/FICHA_CIERRE/fc_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def FC_ADDONE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            form = formFICHA_CIERRE(request.POST)
            if form.is_valid():
                fc = form.save(commit=False)
                fc.save()
                crear_log(request.user, f'Crear Ficha de Cierre', f'Se creó la Ficha de Cierre: {fc.FC_NUMERO_DE_PROYECTO}')                

                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=1,
                    FCD_CACTIVIDAD='Todos los entregables comprometidos fueron enviados a cliente.',
                    FCD_CCUMPLIMIENTO='SI',
                    FCD_COBSERVACIONES='',
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=2,
                    FCD_CACTIVIDAD='Todos los entregables comprometidos están en rev 0 o su equivalente.',
                    FCD_CCUMPLIMIENTO='SI',
                    FCD_COBSERVACIONES='',
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=3,
                    FCD_CACTIVIDAD='Se realizó la reunión de cierre con el cliente (presentación de resultados).',
                    FCD_CCUMPLIMIENTO='SI',
                    FCD_COBSERVACIONES='',
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=4,
                    FCD_CACTIVIDAD='Se emitió el último estado de pago (EDP) pactado por el cliente.',
                    FCD_CCUMPLIMIENTO='SI',
                    FCD_COBSERVACIONES='',
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=5,
                    FCD_CACTIVIDAD='Satisfacción al cliente.',
                    FCD_CCUMPLIMIENTO='SI',
                    FCD_COBSERVACIONES='',
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                
                messages.success(request, 'Ficha de Cierre guardada correctamente')
                return redirect('/fc_listall/')
        form = formFICHA_CIERRE()
        proyectos = PROYECTO_CLIENTE.objects.all()
        ctx = {
            'form': form,
            'state': 'add',
            'proyectos': proyectos,
        }
        return render(request, 'home/FICHA_CIERRE/fc_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def FC_UPDATE(request, pk):
    if not has_auth(request.user, 'EDITAR_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        fc = FICHA_CIERRE.objects.get(id=pk)
        if request.method == 'POST':
            form = formFICHA_CIERRE(request.POST, instance=fc)
            if form.is_valid():
                fc = form.save(commit=False)
                # Actualizar el número de proyecto si es necesario
                proyecto = PROYECTO_CLIENTE.objects.get(id=form.cleaned_data['FC_NOMBRE_DE_PROYECTO'].id)
                fc.FC_NUMERO_DE_PROYECTO = f"FC-{proyecto.PC_CCODIGO}-{fc.FC_FECHA_DE_CIERRE.year}"
                fc.save()
                crear_log(request.user, f'Editar Ficha de Cierre', f'Se editó la Ficha de Cierre: {fc.FC_NUMERO_DE_PROYECTO}')
                messages.success(request, 'Ficha de Cierre actualizada correctamente')
                return redirect('/fc_listall/')
        else:
            form = formFICHA_CIERRE(instance=fc)
        
        proyectos = PROYECTO_CLIENTE.objects.all()
        ctx = {
            'form': form,
            'state': 'update',
            'proyectos': proyectos,
            'ficha_cierre': fc,
        }
        return render(request, 'home/FICHA_CIERRE/fc_update.html', ctx)
    except FICHA_CIERRE.DoesNotExist:
        messages.error(request, 'No se encontró la Ficha de Cierre especificada')
        return redirect('/')
    except Exception as e:
        print(e)
        messages.error(request, f'Error: {str(e)}')
        return redirect('/')

def FC_LISTONE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        fc = FICHA_CIERRE.objects.get(id=pk)
        ctx = {
            'fc': fc,
        }
        return render(request, 'home/FICHA_CIERRE/fc_listone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/fc_listall/')

def FC_LISTONE_FORMAT(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        fc = FICHA_CIERRE.objects.get(id=pk)
        
        ctx = {
            'fc': fc,
        }
        return render(request, 'home/FICHA_CIERRE/fc_listone_format.html', ctx)
    except Exception as e:
        print("ERROR:", e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/fc_listall/')
    
def FC_GET_LINE(request, pk):
    if not has_auth(request.user, 'VER_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = FICHA_CIERRE_DETALLE.objects.get(id=pk)
        
        data = {
            'id': detalle.id,
            'nactividad': detalle.FCD_NACTIVIDAD,
            'cactividad': detalle.FCD_CACTIVIDAD,
            'ccumplimiento': detalle.FCD_CCUMPLIMIENTO,
            'cobservaciones': detalle.FCD_COBSERVACIONES
        }
        return JsonResponse(data)
    except FICHA_CIERRE_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Detalle de ficha de cierre no encontrado'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def FC_ADD_UPDATE_LINE(request):
    if not has_auth(request.user, 'ADD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method == 'POST':
            fc_id = request.POST.get('fc_id')
            line_id = request.POST.get('lineId')
            cactividad = request.POST.get('cactividad')
            ccumplimiento = request.POST.get('ccumplimiento')
            cobservaciones = request.POST.get('cobservaciones')

            fc = FICHA_CIERRE.objects.get(id=fc_id)

            if line_id:  # Actualizar línea existente
                detalle = FICHA_CIERRE_DETALLE.objects.get(id=line_id)
                detalle.FCD_CACTIVIDAD = cactividad
                detalle.FCD_CCUMPLIMIENTO = ccumplimiento
                detalle.FCD_COBSERVACIONES = cobservaciones
                detalle.save()
                crear_log(request.user, f'Actualizar Detalle de Ficha de Cierre', f'Se actualizó el detalle de ficha de cierre: Actividad {detalle.FCD_NACTIVIDAD}')
                mensaje = 'Detalle de ficha de cierre actualizado correctamente'
            else:  # Crear nueva línea
                # Obtener el último número de actividad para esta ficha de cierre
                last_detail = FICHA_CIERRE_DETALLE.objects.filter(FCD_FICHA_CIERRE=fc).order_by('-FCD_NACTIVIDAD').first()
                if last_detail:
                    nactividad = last_detail.FCD_NACTIVIDAD + 1
                else:
                    nactividad = 1

                detalle = FICHA_CIERRE_DETALLE(
                    FCD_FICHA_CIERRE=fc,
                    FCD_NACTIVIDAD=nactividad,
                    FCD_CACTIVIDAD=cactividad,
                    FCD_CCUMPLIMIENTO=ccumplimiento,
                    FCD_COBSERVACIONES=cobservaciones,
                    FCD_CUSUARIO_CREADOR=request.user
                )
                detalle.save()
                crear_log(request.user, f'Crear Detalle de Ficha de Cierre', f'Se creó el detalle de ficha de cierre: Actividad {detalle.FCD_NACTIVIDAD}')
                mensaje = 'Detalle de ficha de cierre agregado correctamente'

            messages.success(request, mensaje)
            return JsonResponse({'success': True, 'message': mensaje})
        
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    except Exception as e:
        errMsg = f"Error al procesar detalle de ficha de cierre: {str(e)}"
        print(errMsg)
        messages.error(request, errMsg)
        return JsonResponse({'error': str(errMsg)}, status=400)

def FC_DELETE_LINE(request, pk):
    if not has_auth(request.user, 'UPD_DOCUMENTOS'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        detalle = FICHA_CIERRE_DETALLE.objects.get(id=pk)
        fc_id = detalle.FCD_FICHA_CIERRE.id
        crear_log(request.user, f'Eliminar Detalle de Ficha de Cierre', f'Se eliminó el detalle de ficha de cierre: Actividad {detalle.FCD_NACTIVIDAD}')
        detalle.delete()
        return JsonResponse({'success': 'Detalle de ficha de cierre eliminado correctamente', 'fc_id': fc_id})
    except FICHA_CIERRE_DETALLE.DoesNotExist:
        return JsonResponse({'error': 'Detalle de ficha de cierre no encontrado'}, status=404)
    except Exception as e:
        print("ERROR:", e)
        return JsonResponse({'error': str(e)}, status=500)

def CHECK_FC_NUMERO(request):
    if request.method == 'POST':
        fc_numero = request.POST.get('fc_numero')
        exists = FICHA_CIERRE.objects.filter(FC_NUMERO_DE_PROYECTO=fc_numero).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def FC_GENERATE_PDF(request, pk):
    try:
        fc = FICHA_CIERRE.objects.get(id=pk)
        template = get_template('home/FICHA_CIERRE/fc_pdf_template.html')
        
        # Obtener la URL del logo
        logo_url = request.build_absolute_uri(staticfiles_storage.url('assets/images/logo_png_sin_fondo.png'))
        
        # Descargar la imagen
        response = requests.get(logo_url)
        if response.status_code == 200:
            encoded_string = base64.b64encode(response.content).decode()
        else:
            # Si no se puede obtener la imagen, usa una cadena vacía
            encoded_string = ""
        
        context = {
            'fc': fc,
            'logo_base64': encoded_string,
        }
        
        html = template.render(context)
        result = BytesIO()
        
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Ficha_de_Cierre_{fc.FC_NUMERO_DE_PROYECTO}.pdf"'
            return response
        else:
            return HttpResponse(f'Error al generar el PDF: {pdf.err}', status=400)
    
    except Exception as e:
        error_message = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        return HttpResponse(error_message, content_type="text/plain", status=500)
    
def TC_LISTALL(request):
    if not has_auth(request.user, 'VER_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        object_list = TIPO_CAMBIO.objects.all()
        ctx = {
            'object_list': object_list
        }
        return render(request, 'home/TIPO_CAMBIO/tc_listall.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TC_ADDONE(request):
    if not has_auth(request.user, 'ADD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        if request.method =='POST':
            form = formTIPO_CAMBIO(request.POST)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Crear Tipo de Cambio', f'Se creó el tipo de cambio: {form.instance.TC_CMONEDA}')
                messages.success(request, 'Tipo de cambio guardado correctamente')
                return redirect('/tc_listall/')
        form = formTIPO_CAMBIO()
        ctx = {
            'form': form
        }
        return render(request, 'home/TIPO_CAMBIO/tc_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TC_UPDATE(request, pk):
    if not has_auth(request.user, 'UPD_CONFIGURACIONES'):
        messages.error(request, 'No tienes permiso para acceder a esta vista')
        return redirect('/')
    try:
        tipo_cambio = TIPO_CAMBIO.objects.get(id=pk)
        if request.method == 'POST':
            form = formTIPO_CAMBIO(request.POST, instance=tipo_cambio)
            if form.is_valid():
                form.save()
                crear_log(request.user, 'Actualizar Tipo de Cambio', f'Se actualizó el tipo de cambio: {form.instance.TC_CMONEDA}')
                messages.success(request, 'Tipo de cambio actualizado correctamente')
                return redirect('/tc_listall/')
        form = formTIPO_CAMBIO(instance=tipo_cambio)
        ctx = {
            'form': form
        }
        return render(request, 'home/TIPO_CAMBIO/tc_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')
    


def GLOBAL_SEARCH(request, key):
    try:
        print("consultando...",key) 
        with connection.cursor() as cursor:
            # Check if the function already exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 
                    FROM pg_proc 
                    WHERE proname = 'search_all_tables'
                )
            """)
            function_exists = cursor.fetchone()[0]

            # Create the function if it does not exist
            if not function_exists:
                cursor.execute("""
                    CREATE OR REPLACE FUNCTION search_all_tables(search_term TEXT)
                    RETURNS TABLE (
                        result_table_name TEXT,
                        result_column_name TEXT,
                        result_value TEXT,
                        record_id TEXT
                    ) AS $$
                    DECLARE
                        query TEXT := '';
                        r RECORD;
                    BEGIN
                        FOR r IN (
                            SELECT table_schema, table_name, column_name
                            FROM information_schema.columns
                            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                              AND data_type IN ('character varying', 'text')
                        ) LOOP
                            -- Solo añadir la búsqueda si la tabla tiene una columna 'id'
                            IF EXISTS (
                                SELECT 1 
                                FROM information_schema.columns 
                                WHERE table_schema = r.table_schema 
                                  AND table_name = r.table_name 
                                  AND column_name = 'id'
                            ) THEN
                                IF query != '' THEN
                                    query := query || ' UNION ALL ';
                                END IF;

                                query := query || format('
                                    SELECT %L::TEXT AS result_table_name, 
                                           %L::TEXT AS result_column_name, 
                                           %I::TEXT AS result_value, 
                                           id::TEXT AS record_id
                                    FROM %I.%I
                                    WHERE LOWER(%I::TEXT) LIKE LOWER(''%%'' || $1 || ''%%'')',
                                    r.table_name, r.column_name, r.column_name, 
                                    r.table_schema, r.table_name, r.column_name
                                );
                            END IF;
                        END LOOP;

                        query := 'SELECT * FROM (' || query || ') AS results ORDER BY result_table_name, result_column_name';
                        
                        RETURN QUERY EXECUTE query USING search_term;
                    END;
                    $$ LANGUAGE plpgsql;
                """)

            # Execute the search function
            cursor.execute("SELECT * FROM search_all_tables(%s)", [key])
            print("consulta ejecutada") 
            rows = cursor.fetchall()
            # List of elements to match against the first column
            elements_to_remove = ['SYSTEM_LOG', 'ALERTA', 'COTIZACION_DETALLE','ORDEN_VENTA_DETALLE',
                                  'FACTURA_DETALLE','ESTADO_DE_PAGO_DETALLE','FICHA_CIERRE_DETALLE',
                                  'FICHA_CIERRE_DETALLE',
                                    'ETAPA_ADJUNTO',
                                    'ASIGNACION_EMPLEADO_TAREA_INGENIERIA',
                                    'ASIGNACION_EMPLEADO_TAREA_FINANCIERA',
                                    'ASIGNACION_EMPLEADO_TAREA_GENERAL',
                                    'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA',
                                    'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA',
                                    'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL',
                                    'ASIGNACION_RECURSO_TAREA_GENERAL',
                                    'ASIGNACION_RECURSO_TAREA_INGENIERIA',
                                    'ASIGNACION_RECURSO_TAREA_FINANCIERA',
                                    'PROYECTO_ADJUNTO',
                                    'TAREA_GENERAL_DEPENDENCIA',
                                    'TAREA_FINANCIERA_DEPENDENCIA',
                                    'TAREA_INGENIERIA_DEPENDENCIA']

            # Filter out rows where the first column matches any element in the list
            rows = [row for row in rows if row[0] not in elements_to_remove]
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            print("result",result) 
        return JsonResponse({'result': result})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)

def GOTO_RECORD(request, table, pk):
    print(f"Table: {table}, PK: {pk}")
    if table in model_urls:
        function_name = model_urls[table]
        if function_name in globals():
            return globals()[function_name](request, pk)
        else:
            messages.error(request, 'Function not found')
    else:
        messages.error(request, 'Invalid table name')
    return redirect('/')

