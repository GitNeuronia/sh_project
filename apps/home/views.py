# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import * 
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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


def REGION_LISTALL(request):
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
    try:
        if request.method =='POST':
            form = formREGION(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        region = REGION.objects.get(id=pk)
        if request.method == 'POST':
            form = formREGION(request.POST, instance=region)
            if form.is_valid():
                form.save()
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
    try:
        if request.method =='POST':
            form = formPROVINCIA(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        provincia = PROVINCIA.objects.get(id=pk)
        if request.method == 'POST':
            form = formPROVINCIA(request.POST, instance=provincia)
            if form.is_valid():
                form.save()
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
    try:
        if request.method =='POST':
            form = formCOMUNA(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        comuna = COMUNA.objects.get(id=pk)
        if request.method == 'POST':
            form = formCOMUNA(request.POST, instance=comuna)
            if form.is_valid():
                form.save()
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
    try:
        if request.method =='POST':
            form = formPARAMETRO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        parametro = PARAMETRO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPARAMETRO(request.POST, instance=parametro)
            if form.is_valid():
                form.save()
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
    try:
        if request.method =='POST':
            form = formROL(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        rol = ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formROL(request.POST, instance=rol)
            if form.is_valid():
                form.save()
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
    try:
        if request.method =='POST':
            form = formCATEGORIA_PROYECTO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        categoria_proyecto = CATEGORIA_PROYECTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formCATEGORIA_PROYECTO(request.POST, instance=categoria_proyecto)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formCATEGORIA_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        categoria_cliente = CATEGORIA_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCATEGORIA_CLIENTE(request.POST, instance=categoria_cliente)
            if form.is_valid():
                form.save()
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

def TIPO_PROYECTO_LISTALL(request):
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
    try:
        if request.method == 'POST':
            form = formTIPO_PROYECTO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        tipo_proyecto = TIPO_PROYECTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formTIPO_PROYECTO(request.POST, instance=tipo_proyecto)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formPERMISO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        permiso = PERMISO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPERMISO(request.POST, instance=permiso)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formPERMISO_ROL(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        permiso_rol = PERMISO_ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formPERMISO_ROL(request.POST, instance=permiso_rol)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formUSUARIO_ROL(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        usuario_rol = USUARIO_ROL.objects.get(id=pk)
        if request.method == 'POST':
            form = formUSUARIO_ROL(request.POST, instance=usuario_rol)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formCLIENTE(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        cliente = CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCLIENTE(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formCONTACTO_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        contacto_cliente = CONTACTO_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formCONTACTO_CLIENTE(request.POST, instance=contacto_cliente)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formDIRECCION_CLIENTE(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        direccion_cliente = DIRECCION_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formDIRECCION_CLIENTE(request.POST, instance=direccion_cliente)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formPRODUCTO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        producto = PRODUCTO.objects.get(id=pk)
        if request.method == 'POST':
            form = formPRODUCTO(request.POST, instance=producto)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formEMPLEADO(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        empleado = EMPLEADO.objects.get(id=pk)
        if request.method == 'POST':
            form = formEMPLEADO(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
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
    try:
        if request.method == 'POST':
            form = formCONTRATISTA(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        contratista = CONTRATISTA.objects.get(id=pk)
        if request.method == 'POST':
            form = formCONTRATISTA(request.POST, instance=contratista)
            if form.is_valid():
                form.save()
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

def ETAPA_LISTALL(request):
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
    try:
        if request.method == 'POST':
            form = formETAPA(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        etapa = ETAPA.objects.get(id=pk)
        if request.method == 'POST':
            form = formETAPA(request.POST, instance=etapa)
            if form.is_valid():
                form.save()
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

def PROYECTO_CLIENTE_LISTALL(request):
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
    try:
        if request.method == 'POST':
            form = formPROYECTO_CLIENTE(request.POST)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.PC_CUSUARIO_CREADOR = request.user
                proyecto.save()
                messages.success(request, 'Proyecto de cliente guardado correctamente')
                return redirect('/proycli_listall/')
        form = formPROYECTO_CLIENTE()
        ctx = {
            'form': form
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def PROYECTO_CLIENTE_UPDATE(request, pk):
    try:
        proyecto = PROYECTO_CLIENTE.objects.get(id=pk)
        if request.method == 'POST':
            form = formPROYECTO_CLIENTE(request.POST, instance=proyecto)
            if form.is_valid():
                proyecto = form.save(commit=False)
                proyecto.PC_CUSUARIO_MODIFICADOR = request.user
                proyecto.save()
                messages.success(request, 'Proyecto de cliente actualizado correctamente')
                return redirect('/proycli_listall/')
        form = formPROYECTO_CLIENTE(instance=proyecto)
        ctx = {
            'form': form
        }
        return render(request, 'home/PROYECTO_CLIENTE/proycli_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

#--------------------------------------
#----------------TAREAS----------------
#--------------------------------------

# ----------TAREA GENERAL--------------

def TAREA_GENERAL_LISTALL(request):
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

def TAREA_GENERAL_ADDONE(request):
    try:
        if request.method == 'POST':
            form = formTAREA_GENERAL(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TG_CUSUARIO_CREADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea general guardada correctamente')
                return redirect('/tarea_general_listall/')
        form = formTAREA_GENERAL()
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_GENERAL_UPDATE(request, pk):
    try:
        tarea = TAREA_GENERAL.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_GENERAL(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TG_CUSUARIO_MODIFICADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea general actualizada correctamente')
                return redirect('/tarea_general_listall/')
        form = formTAREA_GENERAL(instance=tarea)
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/GENERAL/tarea_general_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

# ----------TAREA INGENIERIA--------------

def TAREA_INGENIERIA_LISTALL(request):
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

def TAREA_INGENIERIA_ADDONE(request):
    try:
        if request.method == 'POST':
            form = formTAREA_INGENIERIA(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TI_CUSUARIO_CREADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea de ingeniería guardada correctamente')
                return redirect('/tarea_ingenieria_listall/')
        form = formTAREA_INGENIERIA()
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_INGENIERIA_UPDATE(request, pk):
    try:
        tarea = TAREA_INGENIERIA.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_INGENIERIA(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TI_CUSUARIO_MODIFICADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea de ingeniería actualizada correctamente')
                return redirect('/tarea_ingenieria_listall/')
        form = formTAREA_INGENIERIA(instance=tarea)
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/INGENIERIA/tarea_ingenieria_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

# ----------TAREA FINANCIERA--------------

def TAREA_FINANCIERA_LISTALL(request):
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

def TAREA_FINANCIERA_ADDONE(request):
    try:
        if request.method == 'POST':
            form = formTAREA_FINANCIERA(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TF_CUSUARIO_CREADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea financiera guardada correctamente')
                return redirect('/tarea_financiera_listall/')
        form = formTAREA_FINANCIERA()
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

def TAREA_FINANCIERA_UPDATE(request, pk):
    try:
        tarea = TAREA_FINANCIERA.objects.get(id=pk)
        if request.method == 'POST':
            form = formTAREA_FINANCIERA(request.POST, instance=tarea)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.TF_CUSUARIO_MODIFICADOR = request.user
                tarea.save()
                messages.success(request, 'Tarea financiera actualizada correctamente')
                return redirect('/tarea_financiera_listall/')
        form = formTAREA_FINANCIERA(instance=tarea)
        ctx = {
            'form': form
        }
        return render(request, 'home/TAREA/FINANCIERA/tarea_financiera_addone.html', ctx)
    except Exception as e:
        print(e)
        messages.error(request, f'Error, {str(e)}')
        return redirect('/')

#--------------------------------------
#----------------TAREAS----------------
#--------------------------------------

def ACTA_REUNION_LISTALL(request):
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
    try:
        if request.method == 'POST':
            form = formACTA_REUNION(request.POST)
            if form.is_valid():
                form.save()
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
    try:
        acta_reunion = ACTA_REUNION.objects.get(id=pk)
        if request.method == 'POST':
            form = formACTA_REUNION(request.POST, instance=acta_reunion)
            if form.is_valid():
                form.save()
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



# def BOLETA_GARANTIA_LISTALL(request):
#     try:
#         object_list = BOLETA_GARANTIA.objects.all()
#         ctx = {
#             'object_list': object_list
#         }
#         return render(request, 'home/BOLETA_GARANTIA/boletagarantia_listall.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')

# def BOLETA_GARANTIA_ADDONE(request):
#     try:
#         if request.method =='POST':
#             form = formBOLETA_GARANTIA(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Boleta de garantía guardada correctamente')
#                 return redirect('/boletagarantia_listall/')
#         form = formBOLETA_GARANTIA()
#         ctx = {
#             'form': form
#         }
#         return render(request, 'home/BOLETA_GARANTIA/boletagarantia_addone.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')

# def BOLETA_GARANTIA_UPDATE(request, pk):
#     try:
#         boleta_garantia = BOLETA_GARANTIA.objects.get(id=pk)
#         if request.method == 'POST':
#             form = formBOLETA_GARANTIA(request.POST, instance=boleta_garantia)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Boleta de garantía actualizada correctamente')
#                 return redirect('/boletagarantia_listall/')
#         form = formBOLETA_GARANTIA(instance=boleta_garantia)
#         ctx = {
#             'form': form
#         }
#         return render(request, 'home/BOLETA_GARANTIA/boletagarantia_addone.html', ctx)
#     except Exception as e:
#         print(e)
#         messages.error(request, f'Error, {str(e)}')
#         return redirect('/')
