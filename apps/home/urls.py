# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import login_required


urlpatterns = [

    # La página de inicio
    path('', views.index, name='home'),

    # URLs para la gestión de regiones
    path('reg_listall/', login_required(views.REGION_LISTALL), name='reg_listall'),
    path('reg_addone/', login_required(views.REGION_ADDONE), name='reg_addone'),
    path('reg_update/<int:pk>/', login_required(views.REGION_UPDATE), name='reg_update'),

    # URLs para la gestión de provincias
    path('prov_listall/', login_required(views.PROVINCIA_LISTALL), name='prov_listall'),
    path('prov_addone/', login_required(views.PROVINCIA_ADDONE), name='prov_addone'),
    path('prov_update/<int:pk>/', login_required(views.PROVINCIA_UPDATE), name='prov_update'),

    # URLs para la gestión de comunas
    path('com_listall/', login_required(views.COMUNA_LISTALL), name='com_listall'),
    path('com_addone/', login_required(views.COMUNA_ADDONE), name='com_addone'),
    path('com_update/<int:pk>/', login_required(views.COMUNA_UPDATE), name='com_update'),

    # URLs para la gestión de parámetros
    path('param_listall/', login_required(views.PARAMETRO_LISTALL), name='param_listall'),
    path('param_addone/', login_required(views.PARAMETRO_ADDONE), name='param_addone'),
    path('param_update/<int:pk>/', login_required(views.PARAMETRO_UPDATE), name='param_update'),

    # URLs para la gestión de roles
    path('rol_listall/', login_required(views.ROL_LISTALL), name='rol_listall'),
    path('rol_addone/', login_required(views.ROL_ADDONE), name='rol_addone'),
    path('rol_update/<int:pk>/', login_required(views.ROL_UPDATE), name='rol_update'),

    # URLs para la gestión de categorías de proyecto
    path('catproy_listall/', login_required(views.CATEGORIA_PROYECTO_LISTALL), name='catproy_listall'),
    path('catproy_addone/', login_required(views.CATEGORIA_PROYECTO_ADDONE), name='catproy_addone'),
    path('catproy_update/<int:pk>/', login_required(views.CATEGORIA_PROYECTO_UPDATE), name='catproy_update'),

    # URLs para la gestión de categorías de cliente
    path('catcli_listall/', login_required(views.CATEGORIA_CLIENTE_LISTALL), name='catcli_listall'),
    path('catcli_addone/', login_required(views.CATEGORIA_CLIENTE_ADDONE), name='catcli_addone'),
    path('catcli_update/<int:pk>/', login_required(views.CATEGORIA_CLIENTE_UPDATE), name='catcli_update'),

    # URLs para la gestión de tipos de proyecto
    path('tipoproy_listall/', login_required(views.TIPO_PROYECTO_LISTALL), name='tipoproy_listall'),
    path('tipoproy_addone/', login_required(views.TIPO_PROYECTO_ADDONE), name='tipoproy_addone'),
    path('tipoproy_update/<int:pk>/', login_required(views.TIPO_PROYECTO_UPDATE), name='tipoproy_update'),

    # URLs para la gestión de permisos
    path('permiso_listall/', login_required(views.PERMISO_LISTALL), name='permiso_listall'),
    path('permiso_addone/', login_required(views.PERMISO_ADDONE), name='permiso_addone'),
    path('permiso_update/<int:pk>/', login_required(views.PERMISO_UPDATE), name='permiso_update'),

    # URLs para la gestión de permisos de roles
    path('permisorol_listall/', login_required(views.PERMISO_ROL_LISTALL), name='permisorol_listall'),
    path('permisorol_addone/', login_required(views.PERMISO_ROL_ADDONE), name='permisorol_addone'),
    path('permisorol_update/<int:pk>/', login_required(views.PERMISO_ROL_UPDATE), name='permisorol_update'),

    # URLs para la gestión de usuarios de roles
    path('usuariorol_listall/', login_required(views.USUARIO_ROL_LISTALL), name='usuariorol_listall'),
    path('usuariorol_addone/', login_required(views.USUARIO_ROL_ADDONE), name='usuariorol_addone'),
    path('usuariorol_update/<int:pk>/', login_required(views.USUARIO_ROL_UPDATE), name='usuariorol_update'),

    # URLs para la gestión de clientes
    path('cliente_listall/', login_required(views.CLIENTE_LISTALL), name='cliente_listall'),
    path('cliente_addone/', login_required(views.CLIENTE_ADDONE), name='cliente_addone'),
    path('cliente_update/<int:pk>/', login_required(views.CLIENTE_UPDATE), name='cliente_update'),

    # URLs para la gestión de contactos de clientes
    path('contactocli_listall/', login_required(views.CONTACTO_CLIENTE_LISTALL), name='contactocli_listall'),
    path('contactocli_addone/', login_required(views.CONTACTO_CLIENTE_ADDONE), name='contactocli_addone'),
    path('contactocli_update/<int:pk>/', login_required(views.CONTACTO_CLIENTE_UPDATE), name='contactocli_update'),

    # URLs para la gestión de direcciones de clientes
    path('direccioncli_listall/', login_required(views.DIRECCION_CLIENTE_LISTALL), name='direccioncli_listall'),
    path('direccioncli_addone/', login_required(views.DIRECCION_CLIENTE_ADDONE), name='direccioncli_addone'),
    path('direccioncli_update/<int:pk>/', login_required(views.DIRECCION_CLIENTE_UPDATE), name='direccioncli_update'),

    # URLs para la gestión de productos
    path('producto_listall/', login_required(views.PRODUCTO_LISTALL), name='producto_listall'),
    path('producto_addone/', login_required(views.PRODUCTO_ADDONE), name='producto_addone'),
    path('producto_update/<int:pk>/', login_required(views.PRODUCTO_UPDATE), name='producto_update'),

    # URLs para la gestión de empleados
    path('empleado_listall/', login_required(views.EMPLEADO_LISTALL), name='empleado_listall'),
    path('empleado_addone/', login_required(views.EMPLEADO_ADDONE), name='empleado_addone'),
    path('empleado_update/<int:pk>/', login_required(views.EMPLEADO_UPDATE), name='empleado_update'),

    # URLs para la gestión de contratistas
    path('contratista_listall/', login_required(views.CONTRATISTA_LISTALL), name='contratista_listall'),
    path('contratista_addone/', login_required(views.CONTRATISTA_ADDONE), name='contratista_addone'),
    path('contratista_update/<int:pk>/', login_required(views.CONTRATISTA_UPDATE), name='contratista_update'),

    # URLs para la gestión de empleados externos
    path('empleado_externo_listall/', login_required(views.EMPLEADO_EXTERNO_LISTALL), name='empleado_externo_listall'),
    path('empleado_externo_addone/', login_required(views.EMPLEADO_EXTERNO_ADDONE), name='empleado_externo_addone'),
    path('empleado_externo_update/<int:pk>/', login_required(views.EMPLEADO_EXTERNO_UPDATE), name='empleado_externo_update'),

    # URLs para la gestión de proyectos de clientes
    path('proycli_listall/', login_required(views.PROYECTO_CLIENTE_LISTALL), name='proycli_listall'),
    path('proycli_addone/', login_required(views.PROYECTO_CLIENTE_ADDONE), name='proycli_addone'),
    path('proycli_update/<int:pk>/', login_required(views.PROYECTO_CLIENTE_UPDATE), name='proycli_update'),
    path('proycli_update/<int:pk>/<int:page>/', login_required(views.PROYECTO_CLIENTE_UPDATE), name='proycli_update'),
    path('proycli_listone/<int:pk>/', login_required(views.PROYECTO_CLIENTE_LISTONE), name='proycli_listone'),    

    # URLs para la gestión de tareas generales
    path('tarea_general_listall/', login_required(views.TAREA_GENERAL_LISTALL), name='tarea_general_listall'),
    path('tarea_general_addone/<int:page>/', login_required(views.TAREA_GENERAL_ADDONE), name='tarea_general_addone'),
    path('tarea_general_update/<int:pk>/', login_required(views.TAREA_GENERAL_UPDATE), name='tarea_general_update'),
    path('tarea_general_update/<int:pk>/<int:page>/', login_required(views.TAREA_GENERAL_UPDATE), name='tarea_general_update'),
    path('tarea_general_update_asignaciones/<int:pk>/<int:page>/', login_required(views.TAREA_GENERAL_UPDATE_ASIGNACIONES), name='tarea_general_update_asignaciones'),
    path('tarea_general_listone/<int:pk>/<int:page>/', login_required(views.TAREA_GENERAL_LISTONE), name='tarea_general_listone'),
    path('tarea_general_dependencia_addone/<int:pk>/', login_required(views.TAREA_GENERAL_DEPENDENCIA_ADDONE), name='tarea_general_dependencia_addone'),

    # URLs para la gestión de tareas de ingeniería
    path('tarea_ingenieria_listall/', login_required(views.TAREA_INGENIERIA_LISTALL), name='tarea_ingenieria_listall'),
    path('tarea_ingenieria_addone/<int:page>/', login_required(views.TAREA_INGENIERIA_ADDONE), name='tarea_ingenieria_addone'),
    path('tarea_ingenieria_update/<int:pk>/', login_required(views.TAREA_INGENIERIA_UPDATE), name='tarea_ingenieria_update'),
    path('tarea_ingenieria_update/<int:pk>/<int:page>/', login_required(views.TAREA_INGENIERIA_UPDATE), name='tarea_ingenieria_update'),
    path('tarea_ingenieria_update_asignaciones/<int:pk>/<int:page>/', login_required(views.TAREA_INGENIERIA_UPDATE_ASIGNACIONES), name='tarea_ingenieria_update_asignaciones'),
    path('tarea_ingenieria_listone/<int:pk>/<int:page>/', login_required(views.TAREA_INGENIERIA_LISTONE), name='tarea_ingenieria_listone'),
    path('tarea_ingenieria_dependencia_addone/<int:pk>/', login_required(views.TAREA_INGENIERIA_DEPENDENCIA_ADDONE), name='tarea_ingenieria_dependencia_addone'),    
    
    # URLs para la gestión de tareas financieras
    path('tarea_financiera_listall/', login_required(views.TAREA_FINANCIERA_LISTALL), name='tarea_financiera_listall'),
    path('tarea_financiera_addone/<int:page>/', login_required(views.TAREA_FINANCIERA_ADDONE), name='tarea_financiera_addone'),
    path('tarea_financiera_update/<int:pk>/', login_required(views.TAREA_FINANCIERA_UPDATE), name='tarea_financiera_update'),
    path('tarea_financiera_update/<int:pk>/<int:page>/', login_required(views.TAREA_FINANCIERA_UPDATE), name='tarea_financiera_update'),
    path('tarea_financiera_update_asignaciones/<int:pk>/<int:page>/', login_required(views.TAREA_FINANCIERA_UPDATE_ASIGNACIONES), name='tarea_financiera_update_asignaciones'),
    path('tarea_financiera_listone/<int:pk>/<int:page>/', login_required(views.TAREA_FINANCIERA_LISTONE), name='tarea_financiera_listone'),
    path('tarea_financiera_dependencia_addone/<int:pk>/', login_required(views.TAREA_FINANCIERA_DEPENDENCIA_ADDONE), name='tarea_financiera_dependencia_addone'),    
    
    # URL para la gestión de actualización de datos de tareas
    path('tarea/<str:tipo_tarea>/<int:pk>/update_data/', login_required(views.tarea_update_data), name='tarea_update_data'),

    # URLs para la gestión de etapas
    path('etapa_listall/', login_required(views.ETAPA_LISTALL), name='etapa_listall'),
    path('etapa_addone/', login_required(views.ETAPA_ADDONE), name='etapa_addone'),
    path('etapa_update/<int:pk>/', login_required(views.ETAPA_UPDATE), name='etapa_update'),

    # URLs para la gestión de actas de reunión
    path('actareunion_listall/', login_required(views.ACTA_REUNION_LISTALL), name='actareunion_listall'),
    path('actareunion_addone/', login_required(views.ACTA_REUNION_ADDONE), name='actareunion_addone'),
    path('actareunion_update/<int:pk>/', login_required(views.ACTA_REUNION_UPDATE), name='actareunion_update'),

    # URLs para la gestión de boletas de garantía (comentadas)
    # path('boletagarantia_listall/', login_required(views.BOLETA_GARANTIA_LISTALL), name='boletagarantia_listall'),
    # path('boletagarantia_addone/', login_required(views.BOLETA_GARANTIA_ADDONE), name='boletagarantia_addone'),
    # path('boletagarantia_update/<int:pk>/', login_required(views.BOLETA_GARANTIA_UPDATE), name='boletagarantia_update'),

    path('cotizacion_listall/', login_required(views.COTIZACION_LISTALL), name='cotizacion_listall'),
    path('cotizacion_addone/', login_required(views.COTIZACION_ADDONE), name='cotizacion_addone'),
    path('cotizacion_update/<int:pk>/', login_required(views.COTIZACION_UPDATE), name='cotizacion_update'),
    path('cotizacion_listone/<int:pk>', login_required(views.COTIZACION_LISTONE), name='cotizacion_listone'),
    path('cotizacion_listone_format/<int:pk>', login_required(views.COTIZACION_LISTONE_FORMAT), name='cotizacion_listone_format'),
    path('cotizacion_getline/<int:pk>', login_required(views.COTIZACION_GET_LINE), name='cotizacion_getline'),
    path('cotizacion_deleteline/<int:pk>', login_required(views.COTIZACION_DELETE_LINE), name='cotizacion_deleteline'),
    path('cotizacion_addline/', login_required(views.COTIZACION_ADD_LINE), name='cotizacion_addline'),


    # Coincide con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),

]
