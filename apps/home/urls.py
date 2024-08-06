# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import login_required


urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('reg_listall/', login_required(views.REGION_LISTALL), name='reg_listall'),
    path('reg_addone/', login_required(views.REGION_ADDONE), name='reg_addone'),
    path('reg_update/<int:pk>/', login_required(views.REGION_UPDATE), name='reg_update'),

    # path('prov_listall/', login_required(views.PROVINCIA_LISTALL), name='prov_listall'),
    # path('prov_addone/', login_required(views.PROVINCIA_ADDONE), name='prov_addone'),
    # path('prov_update/<int:pk>/', login_required(views.PROVINCIA_UPDATE), name='prov_update'),

    # path('com_listall/', login_required(views.COMUNA_LISTALL), name='com_listall'),
    # path('com_addone/', login_required(views.COMUNA_ADDONE), name='com_addone'),
    # path('com_update/<int:pk>/', login_required(views.COMUNA_UPDATE), name='com_update'),

    # path('param_listall/', login_required(views.PARAMETRO_LISTALL), name='param_listall'),
    # path('param_addone/', login_required(views.PARAMETRO_ADDONE), name='param_addone'),
    # path('param_update/<int:pk>/', login_required(views.PARAMETRO_UPDATE), name='param_update'),

    # path('rol_listall/', login_required(views.ROL_LISTALL), name='rol_listall'),
    # path('rol_addone/', login_required(views.ROL_ADDONE), name='rol_addone'),
    # path('rol_update/<int:pk>/', login_required(views.ROL_UPDATE), name='rol_update'),

    # path('catproy_listall/', login_required(views.CATEGORIA_PROYECTO_LISTALL), name='catproy_listall'),
    # path('catproy_addone/', login_required(views.CATEGORIA_PROYECTO_ADDONE), name='catproy_addone'),
    # path('catproy_update/<int:pk>/', login_required(views.CATEGORIA_PROYECTO_UPDATE), name='catproy_update'),

    # path('catcli_listall/', login_required(views.CATEGORIA_CLIENTE_LISTALL), name='catcli_listall'),
    # path('catcli_addone/', login_required(views.CATEGORIA_CLIENTE_ADDONE), name='catcli_addone'),
    # path('catcli_update/<int:pk>/', login_required(views.CATEGORIA_CLIENTE_UPDATE), name='catcli_update'),

    # path('tipoproy_listall/', login_required(views.TIPO_PROYECTO_LISTALL), name='tipoproy_listall'),
    # path('tipoproy_addone/', login_required(views.TIPO_PROYECTO_ADDONE), name='tipoproy_addone'),
    # path('tipoproy_update/<int:pk>/', login_required(views.TIPO_PROYECTO_UPDATE), name='tipoproy_update'),

    # path('permiso_listall/', login_required(views.PERMISO_LISTALL), name='permiso_listall'),
    # path('permiso_addone/', login_required(views.PERMISO_ADDONE), name='permiso_addone'),
    # path('permiso_update/<int:pk>/', login_required(views.PERMISO_UPDATE), name='permiso_update'),

    # path('permisorol_listall/', login_required(views.PERMISO_ROL_LISTALL), name='permisorol_listall'),
    # path('permisorol_addone/', login_required(views.PERMISO_ROL_ADDONE), name='permisorol_addone'),
    # path('permisorol_update/<int:pk>/', login_required(views.PERMISO_ROL_UPDATE), name='permisorol_update'),

    # path('usuariorol_listall/', login_required(views.USUARIO_ROL_LISTALL), name='usuariorol_listall'),
    # path('usuariorol_addone/', login_required(views.USUARIO_ROL_ADDONE), name='usuariorol_addone'),
    # path('usuariorol_update/<int:pk>/', login_required(views.USUARIO_ROL_UPDATE), name='usuariorol_update'),

    # path('cliente_listall/', login_required(views.CLIENTE_LISTALL), name='cliente_listall'),
    # path('cliente_addone/', login_required(views.CLIENTE_ADDONE), name='cliente_addone'),
    # path('cliente_update/<int:pk>/', login_required(views.CLIENTE_UPDATE), name='cliente_update'),

    # path('contactocli_listall/', login_required(views.CONTACTO_CLIENTE_LISTALL), name='contactocli_listall'),
    # path('contactocli_addone/', login_required(views.CONTACTO_CLIENTE_ADDONE), name='contactocli_addone'),
    # path('contactocli_update/<int:pk>/', login_required(views.CONTACTO_CLIENTE_UPDATE), name='contactocli_update'),

    # path('direccioncli_listall/', login_required(views.DIRECCION_CLIENTE_LISTALL), name='direccioncli_listall'),
    # path('direccioncli_addone/', login_required(views.DIRECCION_CLIENTE_ADDONE), name='direccioncli_addone'),
    # path('direccioncli_update/<int:pk>/', login_required(views.DIRECCION_CLIENTE_UPDATE), name='direccioncli_update'),

    # path('producto_listall/', login_required(views.PRODUCTO_LISTALL), name='producto_listall'),
    # path('producto_addone/', login_required(views.PRODUCTO_ADDONE), name='producto_addone'),
    # path('producto_update/<int:pk>/', login_required(views.PRODUCTO_UPDATE), name='producto_update'),

    # path('empleado_listall/', login_required(views.EMPLEADO_LISTALL), name='empleado_listall'),
    # path('empleado_addone/', login_required(views.EMPLEADO_ADDONE), name='empleado_addone'),
    # path('empleado_update/<int:pk>/', login_required(views.EMPLEADO_UPDATE), name='empleado_update'),

    # path('contratista_listall/', login_required(views.CONTRATISTA_LISTALL), name='contratista_listall'),
    # path('contratista_addone/', login_required(views.CONTRATISTA_ADDONE), name='contratista_addone'),
    # path('contratista_update/<int:pk>/', login_required(views.CONTRATISTA_UPDATE), name='contratista_update'),

    # path('etapa_listall/', login_required(views.ETAPA_LISTALL), name='etapa_listall'),
    # path('etapa_addone/', login_required(views.ETAPA_ADDONE), name='etapa_addone'),
    # path('etapa_update/<int:pk>/', login_required(views.ETAPA_UPDATE), name='etapa_update'),

    # path('actareunion_listall/', login_required(views.ACTA_REUNION_LISTALL), name='actareunion_listall'),
    # path('actareunion_addone/', login_required(views.ACTA_REUNION_ADDONE), name='actareunion_addone'),
    # path('actareunion_update/<int:pk>/', login_required(views.ACTA_REUNION_UPDATE), name='actareunion_update'),

    # path('boletagarantia_listall/', login_required(views.BOLETA_GARANTIA_LISTALL), name='boletagarantia_listall'),
    # path('boletagarantia_addone/', login_required(views.BOLETA_GARANTIA_ADDONE), name='boletagarantia_addone'),
    # path('boletagarantia_update/<int:pk>/', login_required(views.BOLETA_GARANTIA_UPDATE), name='boletagarantia_update'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
