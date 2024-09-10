# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import login_required


urlpatterns = [

    # La página de inicio
    path('', login_required(views.proyecto_index), name='proyecto_index'),
    path('api/proyectos-edp/', login_required(views.api_proyectos_edp), name='api_proyectos_edp'),
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

    # URLs para la gestión de monedas
    path('mon_listall/', login_required(views.MONEDA_LISTALL), name='mon_listall'),
    path('mon_addone/', login_required(views.MONEDA_ADDONE), name='mon_addone'),
    path('mon_update/<int:pk>/', login_required(views.MONEDA_UPDATE), name='mon_update'),

    # URLs para la gestión de tipos de cambio
    path('tc_listall/', login_required(views.TC_LISTALL), name='tc_listall'),
    path('tc_addone/', login_required(views.TC_ADDONE), name='tc_addone'),
    path('tc_update/<int:pk>/', login_required(views.TC_UPDATE), name='tc_update'),

    # URLs para la gestión de categorías de proyecto
    path('catproy_listall/', login_required(views.CATEGORIA_PROYECTO_LISTALL), name='catproy_listall'),
    path('catproy_addone/', login_required(views.CATEGORIA_PROYECTO_ADDONE), name='catproy_addone'),
    path('catproy_update/<int:pk>/', login_required(views.CATEGORIA_PROYECTO_UPDATE), name='catproy_update'),

    # URLs para la gestión de estados de tarea
    path('estar_listall/', login_required(views.ESTADO_TAREA_LISTALL), name='estar_listall'),
    path('estar_addone/', login_required(views.ESTADO_TAREA_ADDONE), name='estar_addone'),
    path('estar_update/<int:pk>/', login_required(views.ESTADO_TAREA_UPDATE), name='estar_update'),

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
    path('cliente_modal/<int:pk>/', login_required(views.CLIENTE_MODAL), name='cliente_modal'),
    
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
    path('proycli_documentos_modal/<int:pk>/', login_required(views.PROYECTO_CLIENTE_DOCUMENTOS_MODAL), name='proycli_documentos_modal'),    
    path('proycli_documentos_modal_addone/<int:pk>/', login_required(views.PROYECTO_CLIENTE_DOCUMENTOS_MODAL_ADDONE), name='proycli_documentos_modal_addone'),    
    path('proycli_documento_get/<int:documento_id>/', login_required(views.get_documento), name='get_documento'),
    path('proyecto_cliente_documentos_modal_update/<int:pk>/', login_required(views.PROYECTO_CLIENTE_DOCUMENTOS_MODAL_UPDATE), name='proyecto_cliente_documentos_modal_update'),
    path('proyecto_cliente_documentos_download/<int:documento_id>/', login_required(views.PROYECTO_CLIENTE_DOCUMENTOS_DOWNLOAD), name='proyecto_cliente_documentos_download'),
    
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

    # URLs para la gestión de adjuntos de las tareas
    path('tarea_adjuntos/<int:tarea_id>/<str:tipo_tarea>/', login_required(views.tarea_adjuntos_lista), name='tarea_adjuntos_lista'),
    path('tarea_adjunto/agregar/<int:tarea_id>/<str:tipo_tarea>/', login_required(views.tarea_adjunto_agregar), name='tarea_adjunto_agregar'),
    path('tarea_adjunto/editar/<int:pk>/<str:tipo_tarea>/', login_required(views.tarea_adjunto_editar), name='tarea_adjunto_editar'),
    path('tarea_adjunto/eliminar/<int:pk>/<str:tipo_tarea>/', login_required(views.tarea_adjunto_eliminar), name='tarea_adjunto_eliminar'),
    path('tarea_adjunto/descargar/<int:pk>/<str:tipo_tarea>/', login_required(views.tarea_adjunto_descargar), name='tarea_adjunto_descargar'),

    # URLs para la gestión de etapas
    path('etapa_listall/', login_required(views.ETAPA_LISTALL), name='etapa_listall'),
    path('etapa_addone/', login_required(views.ETAPA_ADDONE), name='etapa_addone'),
    path('etapa_update/<int:pk>/', login_required(views.ETAPA_UPDATE), name='etapa_update'),

    # URLs para la gestión de actas de reunión
    path('actareunion_listall/', login_required(views.ACTA_REUNION_LISTALL), name='actareunion_listall'),
    path('actareunion_addone/', login_required(views.ACTA_REUNION_ADDONE), name='actareunion_addone'),
    path('actareunion_update/<int:pk>/', login_required(views.ACTA_REUNION_UPDATE), name='actareunion_update'),

    # URLs para la gestión de boletas de garantía (comentadas)
    path('boletagarantia_listall/', login_required(views.BOLETA_GARANTIA_LISTALL), name='boletagarantia_listall'),
    path('boletagarantia_addone/', login_required(views.BOLETA_GARANTIA_ADDONE), name='boletagarantia_addone'),
    path('boletagarantia_update/<int:pk>/', login_required(views.BOLETA_GARANTIA_UPDATE), name='boletagarantia_update'),

    path('cotizacion_listall/', login_required(views.COTIZACION_LISTALL), name='cotizacion_listall'),
    path('cotizacion_addone/', login_required(views.COTIZACION_ADDONE), name='cotizacion_addone'),
    path('cotizacion_update/<int:pk>/', login_required(views.COTIZACION_UPDATE), name='cotizacion_update'),
    path('cotizacion_listone/<int:pk>', login_required(views.COTIZACION_LISTONE), name='cotizacion_listone'),
    path('cotizacion_getdata/<int:pk>', login_required(views.COTIZACION_GET_DATA), name='cotizacion_getdata'),
    path('cotizacion_listone_format/<int:pk>', login_required(views.COTIZACION_LISTONE_FORMAT), name='cotizacion_listone_format'),
    path('cotizacion_getline/<int:pk>', login_required(views.COTIZACION_GET_LINE), name='cotizacion_getline'),
    path('cotizacion_deleteline/<int:pk>', login_required(views.COTIZACION_DELETE_LINE), name='cotizacion_deleteline'),
    path('cotizacion_addline/', login_required(views.COTIZACION_ADD_LINE), name='cotizacion_addline'),
    path('check_co_numero/', login_required(views.CHECK_CO_NUMERO), name='check_co_numero'),

    path('get_tipo_cambio_options/', login_required(views.get_tipo_cambio_options), name='get_tipo_cambio_options'),

    path('orden_venta_listall/', login_required(views.ORDEN_VENTA_LISTALL), name='orden_venta_listall'),
    path('orden_venta_addone/', login_required(views.ORDEN_VENTA_ADDONE), name='orden_venta_addone'),
    path('orden_venta_update/<int:pk>/', login_required(views.ORDEN_VENTA_UPDATE), name='orden_venta_update'),
    path('orden_venta_listone/<int:pk>', login_required(views.ORDEN_VENTA_LISTONE), name='orden_venta_listone'),
    path('orden_venta_getdata/<int:pk>', login_required(views.ORDEN_VENTA_GET_DATA), name='orden_venta_getdata'),
    path('orden_venta_listone_format/<int:pk>', login_required(views.ORDEN_VENTA_LISTONE_FORMAT), name='orden_venta_listone_format'),
    path('orden_venta_getline/<int:pk>', login_required(views.ORDEN_VENTA_GET_LINE), name='orden_venta_getline'),
    path('orden_venta_deleteline/<int:pk>', login_required(views.ORDEN_VENTA_DELETE_LINE), name='orden_venta_deleteline'),
    path('orden_venta_addline/', login_required(views.ORDEN_VENTA_ADD_LINE), name='orden_venta_addline'),
    path('check_ov_numero/', login_required(views.CHECK_OV_NUMERO), name='check_ov_numero'),

    path('factura_listall/', login_required(views.FACTURA_LISTALL), name='factura_listall'),
    path('factura_addone/', login_required(views.FACTURA_ADDONE), name='factura_addone'),
    path('factura_update/<int:pk>/', login_required(views.FACTURA_UPDATE), name='factura_update'),
    path('factura_listone/<int:pk>', login_required(views.FACTURA_LISTONE), name='factura_listone'),
    path('factura_listone_format/<int:pk>', login_required(views.FACTURA_LISTONE_FORMAT), name='factura_listone_format'),
    path('factura_getline/<int:pk>', login_required(views.FACTURA_GET_LINE), name='factura_getline'),
    path('factura_deleteline/<int:pk>', login_required(views.FACTURA_DELETE_LINE), name='factura_deleteline'),
    path('factura_addline/', login_required(views.FACTURA_ADD_LINE), name='factura_addline'),
    path('check_fa_numero/', login_required(views.CHECK_FA_NUMERO), name='check_fa_numero'),

    # URLs para query manager
    path('query_listall/', login_required(views.QUERY_LISTALL), name='query_listall'),
    path('query_listone/<int:pk>', login_required(views.QUERY_LISTONE), name='query_listone'),
    path('query_addone/', login_required(views.QUERY_ADDONE), name='query_addone'),
    path('query_update/<int:pk>/', login_required(views.QUERY_UPDATE), name='query_update'),    
    path('query_delete/<int:pk>', login_required(views.QUERY_DELETE), name='query_delete'),
    path('query_run/<int:pk>', login_required(views.QUERY_RUN), name='query_run'),
    path('run_query_param/', login_required(views.run_query_param), name='run_query_param'),

    #URLs para EDP
    path('edp_listall/', login_required(views.EDP_LISTALL), name='edp_listall'),
    path('edp_addone/', login_required(views.EDP_ADDONE), name='edp_addone'),
    path('edp_update/<int:pk>/', login_required(views.EDP_UPDATE), name='edp_update'),
    path('edp_listone/<int:pk>/', login_required(views.EDP_LISTONE), name='edp_listone'),
    path('edp_listone_format/<int:pk>/', login_required(views.EDP_LISTONE_FORMAT), name='edp_listone_format'),
    path('edp_getline/<int:pk>', login_required(views.EDP_GET_LINE), name='edp_getline'),
    path('edp_deleteline/<int:pk>', login_required(views.EDP_DELETE_LINE), name='edp_deleteline'),
    path('edp_addline/', login_required(views.EDP_ADD_LINE), name='edp_addline'),
    path('check_edp_numero/', login_required(views.CHECK_EDP_NUMERO), name='check_edp_numero'),
    
    #URLs para ficha de cierra
    path('fc_listall/', login_required(views.FC_LISTALL), name='fc_listall'),
    path('fc_addone/', login_required(views.FC_ADDONE), name='fc_addone'),
    path('fc_update/<int:pk>/', login_required(views.FC_UPDATE), name='fc_update'),
    path('fc_listone/<int:pk>/', login_required(views.FC_LISTONE), name='fc_listone'),
    path('fc_listone_format/<int:pk>/', login_required(views.FC_LISTONE_FORMAT), name='fc_listone_format'),
    path('fc_getline/<int:pk>', login_required(views.FC_GET_LINE), name='fc_getline'),
    path('fc_deleteline/<int:pk>', login_required(views.FC_DELETE_LINE), name='fc_deleteline'),
    path('fc_add_update_line/', login_required(views.FC_ADD_UPDATE_LINE), name='fc_add_update_line'),
    path('check_fc_numero/', login_required(views.CHECK_FC_NUMERO), name='check_fc_numero'),
    path('fc_generate_pdf/<int:pk>/', login_required(views.FC_GENERATE_PDF), name='fc_generate_pdf'),
    #Urls para Unidad de negocio
    path('un_listall/', login_required(views.UNIDAD_NEGOCIO_LISTALL), name='un_listall'),
    path('un_addone/', login_required(views.UNIDAD_NEGOCIO_ADDONE), name='un_addone'),
    path('un_update/<int:pk>', login_required(views.UNIDAD_NEGOCIO_UPDATE), name='un_update'),
    


    #busqueda
    path('global_search/<str:key>/', login_required(views.GLOBAL_SEARCH), name='global_search'),
    path('goto_record/<str:table>/<int:pk>/', login_required(views.GOTO_RECORD), name='goto_record'),

    # Coincide con cualquier archivo html
    re_path(r'^.*\.*', views.pages, name='pages'),

]
