import datetime
from django import forms
from django.contrib.auth.models import *
from apps.home.models import *
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from collections import OrderedDict
from decimal import Decimal, InvalidOperation
def validate_file_size(value):
    filesize = value.file.size
    if filesize > 5242880:  # 5MB limit
        raise ValidationError("El tamaño máximo de archivo que se puede subir es de 5MB")
    else:
        return value
    
class formREGION(forms.ModelForm):
    class Meta:
        model = REGION
        fields = ['RG_CNOMBRE', 'RG_CCODIGO']  # Adjust fields to match model attributes
        labels = {
            'RG_CNOMBRE': 'Nombre',
            'RG_CCODIGO': 'Código'
        }
        widgets = {
            'RG_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'RG_CCODIGO': forms.TextInput(attrs={'class': 'form-control'})
        }

class formPROVINCIA(forms.ModelForm):
    class Meta:
        model = PROVINCIA
        fields = ['PV_CNOMBRE', 'PV_CCODIGO', 'RG_NID']  # Adjust fields to match model attributes
        labels = {
            'PV_CNOMBRE': 'Nombre',
            'PV_CCODIGO': 'Código',
            'REGION': 'Región'
        }
        widgets = {
            'PV_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'PV_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'RG_NID': forms.Select(attrs={'class': 'form-control js-example-placeholder-multiple', 'id': 'id_region'}),
            
        }

class formCOMUNA(forms.ModelForm):
    class Meta:
        model = COMUNA
        fields = ['COM_CNOMBRE', 'COM_CCODIGO', 'PV_NID']  # Adjust fields to match model attributes
        labels = {
            'COM_CNOMBRE': 'Nombre',
            'COM_CCODIGO': 'Código',
            'PV_NID': 'Provincia'
        }
        widgets = {
            'COM_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'COM_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'PV_NID': forms.Select(attrs={'class': 'form-control js-example-placeholder-multiple', 'id': 'id_provincia'}),
        }

class formSYSTEM_LOG(forms.ModelForm):
    class Meta:
        model = SYSTEM_LOG
        fields = ['USER_CREATOR_ID', 'LG_ACTION', 'LG_DESCRIPTION']
        labels = {
            'USER_CREATOR_ID': 'Usuario Creador',
            'LG_ACTION': 'Acción',
            'LG_DESCRIPTION': 'Descripción'
        }
        widgets = {
            'USER_CREATOR_ID': forms.Select(attrs={'class': 'form-control'}),
            'LG_ACTION': forms.TextInput(attrs={'class': 'form-control'}),
            'LG_DESCRIPTION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super(formSYSTEM_LOG, self).__init__(*args, **kwargs)
        self.fields['LG_TIMESTAMP'].widget = forms.HiddenInput()

class formPARAMETRO(forms.ModelForm):
    class Meta:
        model = PARAMETRO
        fields = ['PM_CGRUPO', 'PM_CCODIGO', 'PM_CDESCRIPCION', 'PM_CVALOR']
        labels = {
            'PM_CGRUPO': 'Grupo',
            'PM_CCODIGO': 'Código',
            'PM_CDESCRIPCION': 'Descripción',
            'PM_CVALOR': 'Valor'
        }
        widgets = {
            'PM_CGRUPO': forms.TextInput(attrs={'class': 'form-control'}),
            'PM_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'PM_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'PM_CVALOR': forms.TextInput(attrs={'class': 'form-control'})
        }

class formALERTA(forms.ModelForm):
    class Meta:
        model = ALERTA
        fields = ['AL_USUARIO_ORIGEN', 'AL_USUARIO_DESTINO', 'AL_CCLASE', 'AL_CASUNTO', 'AL_CCUERPO']
        labels = {
            'AL_USUARIO_ORIGEN': 'Usuario Origen',
            'AL_USUARIO_DESTINO': 'Usuario Destino',
            'AL_CCLASE': 'Clase',
            'AL_CASUNTO': 'Asunto',
            'AL_CCUERPO': 'Cuerpo'
        }
        widgets = {
            'AL_USUARIO_ORIGEN': forms.Select(attrs={'class': 'form-control'}),
            'AL_USUARIO_DESTINO': forms.Select(attrs={'class': 'form-control'}),
            'AL_CCLASE': forms.TextInput(attrs={'class': 'form-control'}),
            'AL_CASUNTO': forms.TextInput(attrs={'class': 'form-control'}),
            'AL_CCUERPO': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(formALERTA, self).__init__(*args, **kwargs)
        self.fields['AL_FFECHA_CREACION'].widget = forms.HiddenInput()
        self.fields['AL_FFECHA_ENVIO'].widget = forms.HiddenInput()
        self.fields['AL_FFECHA_LECTURA'].widget = forms.HiddenInput()
        self.fields['AL_BLEIDA'].widget = forms.HiddenInput()

class formROL(forms.ModelForm):
    class Meta:
        model = ROL
        fields = ['RO_CNOMBRE', 'RO_CDESCRIPCION', 'RO_BACTIVO']
        labels = {
            'RO_CNOMBRE': 'Nombre del rol',
            'RO_CDESCRIPCION': 'Descripción del rol',
            'RO_BACTIVO': 'Activo'
        }
        widgets = {
            'RO_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'RO_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'RO_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formROL, self).__init__(*args, **kwargs)
        if 'RO_FFECHA_CREACION' in self.fields:
            self.fields['RO_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'RO_FFECHA_MODIFICACION' in self.fields:
            self.fields['RO_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formCATEGORIA_PROYECTO(forms.ModelForm):
    class Meta:
        model = CATEGORIA_PROYECTO
        fields = ['CA_CNOMBRE', 'CA_CDESCRIPCION', 'CA_BACTIVA']
        labels = {
            'CA_CNOMBRE': 'Nombre de la categoría',
            'CA_CDESCRIPCION': 'Descripción de la categoría',
            'CA_BACTIVA': 'Activa'
        }
        widgets = {
            'CA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'CA_BACTIVA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formCATEGORIA_PROYECTO, self).__init__(*args, **kwargs)
        if 'CA_FFECHA_CREACION' in self.fields:
            self.fields['CA_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'CA_FFECHA_MODIFICACION' in self.fields:
            self.fields['CA_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formESTADO_TAREA(forms.ModelForm):
    class Meta:
        model = ESTADO_TAREA
        fields = ['ET_CNOMBRE', 'ET_CDESCRIPCION', 'ET_BACTIVA']
        labels = {
            'ET_CNOMBRE': 'Nombre del estado de tarea',
            'ET_CDESCRIPCION': 'Descripción del estado de tarea',
            'ET_BACTIVA': 'Activo'
        }
        widgets = {
            'ET_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'ET_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ET_BACTIVA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formESTADO_TAREA, self).__init__(*args, **kwargs)
        if 'ET_FFECHA_CREACION' in self.fields:
            self.fields['ET_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'ET_FFECHA_MODIFICACION' in self.fields:
            self.fields['ET_FFECHA_MODIFICACION'].widget = forms.HiddenInput()


class formCATEGORIA_CLIENTE(forms.ModelForm):
    class Meta:
        model = CATEGORIA_CLIENTE
        fields = ['CA_CNOMBRE', 'CA_CDESCRIPCION', 'CA_BACTIVA']
        labels = {
            'CA_CNOMBRE': 'Nombre de la categoría',
            'CA_CDESCRIPCION': 'Descripción de la categoría',
            'CA_BACTIVA': 'Activa'
        }
        widgets = {
            'CA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'CA_BACTIVA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formCATEGORIA_CLIENTE, self).__init__(*args, **kwargs)
        if 'CA_FFECHA_CREACION' in self.fields:
            self.fields['CA_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'CA_FFECHA_MODIFICACION' in self.fields:
            self.fields['CA_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formTIPO_PROYECTO(forms.ModelForm):
    class Meta:
        model = TIPO_PROYECTO
        fields = ['TP_CNOMBRE', 'TP_CDESCRIPCION', 'TP_BACTIVO']
        labels = {
            'TP_CNOMBRE': 'Nombre del tipo de proyecto',
            'TP_CDESCRIPCION': 'Descripción del tipo de proyecto',
            'TP_BACTIVO': 'Activo'
        }
        widgets = {
            'TP_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'TP_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'TP_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formTIPO_PROYECTO, self).__init__(*args, **kwargs)
        if 'TP_FFECHA_CREACION' in self.fields:
            self.fields['TP_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'TP_FFECHA_MODIFICACION' in self.fields:
            self.fields['TP_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formPERMISO(forms.ModelForm):
    class Meta:
        model = PERMISO
        fields = ['PE_CNOMBRE', 'PE_CDESCRIPCION', 'PE_BACTIVO']
        labels = {
            'PE_CNOMBRE': 'Nombre del permiso',
            'PE_CDESCRIPCION': 'Descripción del permiso',
            'PE_BACTIVO': 'Activo'
        }
        widgets = {
            'PE_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'PE_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'PE_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formPERMISO, self).__init__(*args, **kwargs)
        if 'PE_FFECHA_CREACION' in self.fields:
            self.fields['PE_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'PE_FFECHA_MODIFICACION' in self.fields:
            self.fields['PE_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formPERMISO_ROL(forms.ModelForm):
    class Meta:
        model = PERMISO_ROL
        fields = ['PR_CPERMISO', 'PR_CROL', 'PR_BACTIVO']
        labels = {
            'PR_CPERMISO': 'Permiso',
            'PR_CROL': 'Rol',
            'PR_BACTIVO': 'Activo'
        }
        widgets = {
            'PR_CPERMISO': forms.Select(attrs={'class': 'form-control'}),
            'PR_CROL': forms.Select(attrs={'class': 'form-control'}),
            'PR_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formPERMISO_ROL, self).__init__(*args, **kwargs)
        if 'PR_FFECHA_CREACION' in self.fields:
            self.fields['PR_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'PR_FFECHA_MODIFICACION' in self.fields:
            self.fields['PR_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formUSUARIO_ROL(forms.ModelForm):
    class Meta:
        model = USUARIO_ROL
        fields = ['UR_CUSUARIO', 'UR_CROL', 'UR_BACTIVO']
        labels = {
            'UR_CUSUARIO': 'Usuario',
            'UR_CROL': 'Rol',
            'UR_BACTIVO': 'Activo'
        }
        widgets = {
            'UR_CUSUARIO': forms.Select(attrs={'class': 'form-control'}),
            'UR_CROL': forms.Select(attrs={'class': 'form-control'}),
            'UR_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formUSUARIO_ROL, self).__init__(*args, **kwargs)
        if 'UR_FFECHA_CREACION' in self.fields:
            self.fields['UR_FFECHA_CREACION'].widget = forms.HiddenInput()
        if 'UR_FFECHA_MODIFICACION' in self.fields:
            self.fields['UR_FFECHA_MODIFICACION'].widget = forms.HiddenInput()

class formCLIENTE(forms.ModelForm):
    class Meta:
        model = CLIENTE
        fields = [
            'CL_CNOMBRE', 'CL_CRUT', 'CL_CDIRECCION', 'CL_CREGION', 'CL_CPROVINCIA', 
            'CL_CCOMUNA', 'CL_CTELEFONO', 'CL_CEMAIL', 'CL_CPERSONA_CONTACTO', 
            'CL_CSITIO_WEB', 'CL_CRUBRO', 'CL_BACTIVO', 'CL_BPROSPECTO', 'CL_CCATEGORIA',
            'CL_CUSUARIO_GESTOR'
        ]
        labels = {
            'CL_CNOMBRE': 'Nombre de la empresa',
            'CL_CRUT': 'RUT',
            'CL_CDIRECCION': 'Dirección',
            'CL_CREGION': 'Región',
            'CL_CPROVINCIA': 'Provincia',
            'CL_CCOMUNA': 'Comuna',
            'CL_CTELEFONO': 'Teléfono',
            'CL_CEMAIL': 'Correo electrónico',
            'CL_CPERSONA_CONTACTO': 'Persona de contacto',
            'CL_CSITIO_WEB': 'Sitio web',
            'CL_CRUBRO': 'Rubro',
            'CL_BACTIVO': 'Activo',
            'CL_BPROSPECTO': 'Prospecto',
            'CL_CCATEGORIA': 'Categoría del cliente',
            'CL_CUSUARIO_GESTOR': 'Usuario gestor'
        }
        widgets = {
            'CL_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CL_CRUT': forms.TextInput(attrs={'class': 'form-control'}),
            'CL_CDIRECCION': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'CL_CREGION': forms.Select(attrs={'class': 'form-control'}),
            'CL_CPROVINCIA': forms.Select(attrs={'class': 'form-control'}),
            'CL_CCOMUNA': forms.Select(attrs={'class': 'form-control'}),
            'CL_CTELEFONO': forms.TextInput(attrs={'class': 'form-control'}),
            'CL_CEMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'CL_CPERSONA_CONTACTO': forms.TextInput(attrs={'class': 'form-control'}),
            'CL_CSITIO_WEB': forms.URLInput(attrs={'class': 'form-control'}),
            'CL_CRUBRO': forms.TextInput(attrs={'class': 'form-control'}),
            'CL_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'CL_BPROSPECTO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'CL_CCATEGORIA': forms.Select(attrs={'class': 'form-control'}),
            'CL_CUSUARIO_GESTOR': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formCLIENTE, self).__init__(*args, **kwargs)
        for field in ['CL_FFECHA_CREACION', 'CL_FFECHA_MODIFICACION', 'CL_CUSUARIO_CREADOR', 'CL_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for CONTACTO_CLIENTE model
class formCONTACTO_CLIENTE(forms.ModelForm):
    class Meta:
        model = CONTACTO_CLIENTE
        fields = [
            'CC_CLIENTE', 'CC_CNOMBRE', 'CC_CAPELLIDO', 'CC_CCARGO',
            'CC_CTELEFONO', 'CC_CEMAIL', 'CC_BACTIVO'
        ]
        labels = {
            'CC_CLIENTE': 'Cliente',
            'CC_CNOMBRE': 'Nombre del contacto',
            'CC_CAPELLIDO': 'Apellido del contacto',
            'CC_CCARGO': 'Cargo',
            'CC_CTELEFONO': 'Teléfono',
            'CC_CEMAIL': 'Correo electrónico',
            'CC_BACTIVO': 'Activo'
        }
        widgets = {
            'CC_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'CC_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CC_CAPELLIDO': forms.TextInput(attrs={'class': 'form-control'}),
            'CC_CCARGO': forms.TextInput(attrs={'class': 'form-control'}),
            'CC_CTELEFONO': forms.TextInput(attrs={'class': 'form-control'}),
            'CC_CEMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'CC_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formCONTACTO_CLIENTE, self).__init__(*args, **kwargs)
        for field in ['CC_FFECHA_CREACION', 'CC_FFECHA_MODIFICACION', 'CC_CUSUARIO_CREADOR', 'CC_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()


# Form for DIRECCION_CLIENTE model
class formDIRECCION_CLIENTE(forms.ModelForm):
    class Meta:
        model = DIRECCION_CLIENTE
        fields = [
            'DR_CLIENTE', 'DR_CDIRECCION', 'DR_CREGION', 'DR_CPROVINCIA',
            'DR_CCOMUNA', 'DR_CTIPO', 'DR_BACTIVA'
        ]
        labels = {
            'DR_CLIENTE': 'Cliente',
            'DR_CDIRECCION': 'Dirección',
            'DR_CREGION': 'Región',
            'DR_CPROVINCIA': 'Provincia',
            'DR_CCOMUNA': 'Comuna',
            'DR_CTIPO': 'Tipo de dirección',
            'DR_BACTIVA': 'Activa'
        }
        widgets = {
            'DR_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'DR_CDIRECCION': forms.Textarea(attrs={'class': 'form-control'}),
            'DR_CREGION': forms.Select(attrs={'class': 'form-control'}),
            'DR_CPROVINCIA': forms.Select(attrs={'class': 'form-control'}),
            'DR_CCOMUNA': forms.Select(attrs={'class': 'form-control'}),
            'DR_CTIPO': forms.TextInput(attrs={'class': 'form-control'}),
            'DR_BACTIVA': forms.CheckboxInput(attrs={'class': 'form-check-input','style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formDIRECCION_CLIENTE, self).__init__(*args, **kwargs)
        for field in ['DR_FFECHA_CREACION', 'DR_FFECHA_MODIFICACION', 'DR_CUSUARIO_CREADOR', 'DR_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for PRODUCTO model
class formPRODUCTO(forms.ModelForm):
    class Meta:
        model = PRODUCTO
        fields = [
            'PR_CNOMBRE', 'PR_CDESCRIPCION', 'PR_BACTIVO', 'PR_BSERVICIO'
        ]
        labels = {
            'PR_CNOMBRE': 'Nombre del producto',
            'PR_CDESCRIPCION': 'Descripción',
            'PR_BACTIVO': 'Activo',
            'PR_BSERVICIO': 'Es servicio'
        }
        widgets = {
            'PR_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'PR_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'PR_BACTIVO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'PR_BSERVICIO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formPRODUCTO, self).__init__(*args, **kwargs)
        for field in ['PR_FFECHA_CREACION', 'PR_FFECHA_MODIFICACION', 'PR_CUSUARIO_CREADOR', 'PR_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

class formTIPO_CAMBIO(forms.ModelForm):
    class Meta:
        model = TIPO_CAMBIO
        fields = [
            'TC_CMONEDA', 'TC_FFECHA', 'TC_NTASA'
        ]
        labels = {
            'TC_CMONEDA': 'Moneda',
            'TC_FFECHA': 'Fecha de Tipo de Cambio',
            'TC_NTASA': 'Tasa de Cambio'
        }
        widgets = {
            'TC_CMONEDA': forms.Select(attrs={'class': 'form-control'}),
            'TC_FFECHA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TC_NTASA': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formTIPO_CAMBIO, self).__init__(*args, **kwargs)
        for field in ['FECHA_CREACION']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for MONEDA model
class formMONEDA(forms.ModelForm):
    class Meta:
        model = MONEDA
        fields = [
            'MO_CMONEDA', 'MO_CDESCRIPCION', 'MO_BACTIVA'
        ]
        labels = {
            'MO_CMONEDA': 'Moneda',
            'MO_CDESCRIPCION': 'Descripción',
            'MO_BACTIVA': 'Activo'
        }
        widgets = {
            'MO_CMONEDA': forms.TextInput(attrs={'class': 'form-control'}),
            'MO_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control'}),
            'MO_BACTIVA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formMONEDA, self).__init__(*args, **kwargs)
        for field in ['MO_FFECHA_CREACION', 'MO_FFECHA_MODIFICACION']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()


# Form for COTIZACION model
class formCOTIZACION(forms.ModelForm):
    class Meta:
        model = COTIZACION
        fields = [
            'CO_CLIENTE', 'CO_CNUMERO', 'CO_FFECHA', 'CO_CVALIDO_HASTA',
            'CO_CESTADO', 'CO_MONEDA','CO_NTOTAL', 'CO_COBSERVACIONES', 'CO_CCOMENTARIO'
            
        ]
        labels = {
            'CO_CLIENTE': 'Cliente',
            'CO_CNUMERO': 'Número de cotización',
            'CO_FFECHA': 'Fecha de cotización',
            'CO_CVALIDO_HASTA': 'Válido hasta',
            'CO_CESTADO': 'Estado',
            'CO_MONEDA': 'Moneda',
            'CO_NTOTAL': 'Total (Moneda Local)',
            'CO_COBSERVACIONES': 'Observaciones',
            'CO_CCOMENTARIO': 'Comentarios generales',
            
        }
        widgets = {
            'CO_CLIENTE': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_CNUMERO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_FFECHA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'CO_CVALIDO_HASTA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'CO_CESTADO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_NTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'CO_CCOMENTARIO': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(formCOTIZACION, self).__init__(*args, **kwargs)
        
      
        
        for field in ['CO_FFECHA_CREACION', 'CO_FFECHA_MODIFICACION', 'CO_CUSUARIO_CREADOR', 'CO_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

        

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

# Form for COTIZACION_DETALLE model
class formCOTIZACION_DETALLE(forms.ModelForm):
    class Meta:
        model = COTIZACION_DETALLE
        fields = [
            'CD_COTIZACION', 'CD_PRODUCTO', 'CD_NCANTIDAD', 'CD_NPRECIO_UNITARIO',
            'CD_NSUBTOTAL', 'CD_NDESCUENTO', 'CD_NTOTAL'
        ]
        labels = {
            'CD_COTIZACION': 'Cotización',
            'CD_PRODUCTO': 'Producto',
            'CD_NCANTIDAD': 'Cantidad',
            'CD_NPRECIO_UNITARIO': 'Precio unitario',
            'CD_NSUBTOTAL': 'Subtotal',
            'CD_NDESCUENTO': 'Descuento',
            'CD_NTOTAL': 'Total'
        }
        widgets = {
            'CD_COTIZACION': forms.Select(attrs={'class': 'form-control'}),
            'CD_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'CD_NCANTIDAD': forms.NumberInput(attrs={'class': 'form-control'}),
            'CD_NPRECIO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control'}),
            'CD_NSUBTOTAL': forms.NumberInput(attrs={'class': 'form-control'}),
            'CD_NDESCUENTO': forms.NumberInput(attrs={'class': 'form-control'}),
            'CD_NTOTAL': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formCOTIZACION_DETALLE, self).__init__(*args, **kwargs)
        for field in ['CD_FFECHA_CREACION', 'CD_FFECHA_MODIFICACION', 'CD_CUSUARIO_CREADOR', 'CD_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ORDEN_VENTA model
class formORDEN_VENTA(forms.ModelForm):
    class Meta:
        model = ORDEN_VENTA
        fields = [
            'OV_COTIZACION', 'OV_CCLIENTE', 'OV_CNUMERO', 'OV_FFECHA', 'OV_FFECHA_ENTREGA',
            'OV_CESTADO', 'OV_MONEDA','OV_NTOTAL', 'OV_COBSERVACIONES', 'OV_CCOMENTARIO',
            
        ]
        labels = {
            'OV_COTIZACION': 'Cotización',
            'OV_CCLIENTE': 'Cliente',
            'OV_CNUMERO': 'Número de orden de venta',
            'OV_FFECHA': 'Fecha de orden',
            'OV_FFECHA_ENTREGA': 'Fecha de entrega',
            'OV_CESTADO': 'Estado',
            'OV_NTOTAL': 'Total (Moneda Local)',
            'OV_COBSERVACIONES': 'Observaciones',
            'OV_CCOMENTARIO': 'Comentarios generales',
            'OV_MONEDA': 'Moneda',
        }
        widgets = {
            'OV_COTIZACION': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_CCLIENTE': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_CNUMERO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_FFECHA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'OV_FFECHA_ENTREGA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'OV_CESTADO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            
            'OV_NTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'OV_CCOMENTARIO': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formORDEN_VENTA, self).__init__(*args, **kwargs)
        
       

        # Manejar la carga inicial de datos desde la cotización
        if self.instance.pk is None and 'OV_COTIZACION' in self.data:
            try:
                cotizacion_id = int(self.data.get('OV_COTIZACION'))
                cotizacion = COTIZACION.objects.get(id=cotizacion_id)
                self.fields['OV_CCLIENTE'].initial = cotizacion.CO_CLIENTE
                self.fields['OV_NTOTAL'].initial = cotizacion.CO_NTOTAL
                self.fields['OV_MONEDA'].initial = cotizacion.CO_MONEDA
                self.fields['OV_FFECHA'].initial = cotizacion.CO_FFECHA
                self.fields['OV_COBSERVACIONES'].initial = cotizacion.CO_COBSERVACIONES
            except (ValueError, COTIZACION.DoesNotExist):
                pass

    def clean(self):
        cleaned_data = super().clean()
        cotizacion = cleaned_data.get('OV_COTIZACION')
        
        if cotizacion:
            # Verificar que el cliente coincida con el de la cotización
            if cleaned_data.get('OV_CCLIENTE') != cotizacion.CO_CLIENTE:
                raise ValidationError("El cliente debe coincidir con el de la cotización seleccionada.")
            
            # Verificar que el total coincida con el de la cotización
            if cleaned_data.get('OV_NTOTAL') != cotizacion.CO_NTOTAL:
                raise ValidationError("El total debe coincidir con el de la cotización seleccionada.")
            

        return cleaned_data

# Form for ORDEN_VENTA_DETALLE model
class formORDEN_VENTA_DETALLE(forms.ModelForm):
    class Meta:
        model = ORDEN_VENTA_DETALLE
        fields = [
            'OVD_ORDEN_VENTA', 'OVD_PRODUCTO', 'OVD_NCANTIDAD',
            'OVD_NPRECIO_UNITARIO', 'OVD_NSUBTOTAL', 'OVD_NDESCUENTO', 'OVD_NTOTAL'
        ]
        labels = {
            'OVD_ORDEN_VENTA': 'Orden de Venta',
            'OVD_PRODUCTO': 'Producto',
            'OVD_NCANTIDAD': 'Cantidad',
            'OVD_NPRECIO_UNITARIO': 'Precio unitario',
            'OVD_NSUBTOTAL': 'Subtotal',
            'OVD_NDESCUENTO': 'Descuento',
            'OVD_NTOTAL': 'Total'
        }
        widgets = {
            'OVD_ORDEN_VENTA': forms.Select(attrs={'class': 'form-control'}),
            'OVD_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'OVD_NCANTIDAD': forms.NumberInput(attrs={'class': 'form-control'}),
            'OVD_NPRECIO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control'}),
            'OVD_NSUBTOTAL': forms.NumberInput(attrs={'class': 'form-control'}),
            'OVD_NDESCUENTO': forms.NumberInput(attrs={'class': 'form-control'}),
            'OVD_NTOTAL': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formORDEN_VENTA_DETALLE, self).__init__(*args, **kwargs)
        for field in ['OVD_FFECHA_CREACION', 'OVD_FFECHA_MODIFICACION', 'OVD_CUSUARIO_CREADOR', 'OVD_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for FACTURA model
class formFACTURA(forms.ModelForm):
    class Meta:
        model = FACTURA
        fields = [
            'FA_CORDEN_VENTA', 'FA_CNUMERO', 'FA_FFECHA', 'FA_FFECHA_VENCIMIENTO',
            'FA_CESTADO', 'FA_MONEDA', 'FA_NTOTAL', 'FA_COBSERVACIONES', 'FA_CESTADO_PAGO',
            'FA_NMONTO_PAGADO', 'FA_FFECHA_ULTIMO_PAGO'
        ]
        labels = {
            'FA_CORDEN_VENTA': 'Orden de Venta',
            'FA_CNUMERO': 'Número de factura',
            'FA_FFECHA': 'Fecha de factura',
            'FA_FFECHA_VENCIMIENTO': 'Fecha de vencimiento',
            'FA_CESTADO': 'Estado',
            'FA_MONEDA': 'Moneda',
            
            'FA_NTOTAL': 'Total',
            'FA_COBSERVACIONES': 'Observaciones',
            'FA_CESTADO_PAGO': 'Estado de pago',
            'FA_NMONTO_PAGADO': 'Monto pagado',
            'FA_FFECHA_ULTIMO_PAGO': 'Fecha del último pago',
        }
        widgets = {
            'FA_CORDEN_VENTA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_CNUMERO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_FFECHA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'FA_FFECHA_VENCIMIENTO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'FA_CESTADO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_NTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_CESTADO_PAGO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_NMONTO_PAGADO': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FA_FFECHA_ULTIMO_PAGO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formFACTURA, self).__init__(*args, **kwargs)
        
       
        # Manejar la carga inicial de datos desde la orden de venta
        if self.instance.pk is None and 'FA_CORDEN_VENTA' in self.data:
            try:
                orden_venta_id = int(self.data.get('FA_CORDEN_VENTA'))
                orden_venta = ORDEN_VENTA.objects.get(id=orden_venta_id)
                self.fields['FA_NTOTAL'].initial = orden_venta.OV_NTOTAL
                self.fields['FA_MONEDA'].initial = orden_venta.OV_MONEDA
                self.fields['FA_FFECHA'].initial = orden_venta.OV_FFECHA
                self.fields['FA_COBSERVACIONES'].initial = orden_venta.OV_COBSERVACIONES
            except (ValueError, ORDEN_VENTA.DoesNotExist):
                pass

    def clean(self):
        cleaned_data = super().clean()
        orden_venta = cleaned_data.get('FA_CORDEN_VENTA')
        
        if orden_venta:
            # Verificar que el total coincida con el de la orden de venta
            if cleaned_data.get('FA_NTOTAL') != orden_venta.OV_NTOTAL:
                raise ValidationError("El total debe coincidir con el de la orden de venta seleccionada.")
            
        return cleaned_data
    
# Form for FACTURA_DETALLE model
class formFACTURA_DETALLE(forms.ModelForm):
    class Meta:
        model = FACTURA_DETALLE
        fields = [
            'FAD_FACTURA', 'FAD_PRODUCTO', 'FAD_NCANTIDAD', 'FAD_NPRECIO_UNITARIO',
            'FAD_NSUBTOTAL', 'FAD_NDESCUENTO', 'FAD_NTOTAL'
        ]
        labels = {
            'FAD_FACTURA': 'Factura',
            'FAD_PRODUCTO': 'Producto',
            'FAD_NCANTIDAD': 'Cantidad',
            'FAD_NPRECIO_UNITARIO': 'Precio unitario',
            'FAD_NSUBTOTAL': 'Subtotal',
            'FAD_NDESCUENTO': 'Descuento',
            'FAD_NTOTAL': 'Total'
        }
        widgets = {
            'FAD_FACTURA': forms.Select(attrs={'class': 'form-control'}),
            'FAD_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'FAD_NCANTIDAD': forms.NumberInput(attrs={'class': 'form-control'}),
            'FAD_NPRECIO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control'}),
            'FAD_NSUBTOTAL': forms.NumberInput(attrs={'class': 'form-control'}),
            'FAD_NDESCUENTO': forms.NumberInput(attrs={'class': 'form-control'}),
            'FAD_NTOTAL': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formFACTURA_DETALLE, self).__init__(*args, **kwargs)
        for field in ['FAD_FFECHA_CREACION', 'FAD_FFECHA_MODIFICACION', 'FAD_CUSUARIO_CREADOR', 'FAD_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for EMPLEADO model
class formEMPLEADO(forms.ModelForm):
    class Meta:
        model = EMPLEADO
        fields = [
            'EM_CCODIGO', 'EM_CNOMBRE', 'EM_CAPELLIDO', 'EM_CRUT', 'EM_CFECHA_NACIMIENTO',
            'EM_CDIRECCION', 'EM_CTELEFONO', 'EM_CEMAIL', 'EM_FFECHA_CONTRATACION',
            'EM_CCARGO', 'EM_CDEPARTAMENTO', 'EM_CESTADO'
        ]
        widgets = {
            'EM_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CAPELLIDO': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CRUT': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CFECHA_NACIMIENTO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'EM_CDIRECCION': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CTELEFONO': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CEMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'EM_FFECHA_CONTRATACION': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'EM_CCARGO': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CDEPARTAMENTO': forms.TextInput(attrs={'class': 'form-control'}),
            'EM_CESTADO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formEMPLEADO, self).__init__(*args, **kwargs)
        for field in ['EM_FFECHA_CREACION', 'EM_FFECHA_MODIFICACION', 'EM_CUSUARIO_CREADOR', 'EM_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for EMPLEADO_ADJUNTO model
class formEMPLEADO_ADJUNTO(forms.ModelForm):
    class Meta:
        model = EMPLEADO_ADJUNTO
        fields = [
            'EA_EMPLEADO', 'EA_CNOMBRE', 'EA_CDESCRIPCION', 'EA_CARCHIVO', 'EA_CTIPO'
        ]
        widgets = {
            'EA_EMPLEADO': forms.Select(attrs={'class': 'form-control'}),
            'EA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'EA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'EA_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'EA_CTIPO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formEMPLEADO_ADJUNTO, self).__init__(*args, **kwargs)
        for field in ['EA_FFECHA_SUBIDA', 'EA_FFECHA_MODIFICACION', 'EA_CUSUARIO_CREADOR', 'EA_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for CONTRATISTA model
class formCONTRATISTA(forms.ModelForm):
    class Meta:
        model = CONTRATISTA
        fields = [
            'CO_CCODIGO', 'CO_CNOMBRE', 'CO_CRUT', 'CO_CDIRECCION', 'CO_CTELEFONO',
            'CO_CEMAIL', 'CO_FFECHA_CONTRATACION', 'CO_CESTADO'
        ]
        widgets = {
            'CO_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'CO_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CO_CRUT': forms.TextInput(attrs={'class': 'form-control'}),
            'CO_CDIRECCION': forms.TextInput(attrs={'class': 'form-control'}),
            'CO_CTELEFONO': forms.TextInput(attrs={'class': 'form-control'}),
            'CO_CEMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'CO_FFECHA_CONTRATACION': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'CO_CESTADO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formCONTRATISTA, self).__init__(*args, **kwargs)
        for field in ['CO_FFECHA_CREACION', 'CO_FFECHA_MODIFICACION', 'CO_CUSUARIO_CREADOR', 'CO_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for CONTRATISTA_ADJUNTO model
class formCONTRATISTA_ADJUNTO(forms.ModelForm):
    class Meta:
        model = CONTRATISTA_ADJUNTO
        fields = [
            'CA_CONTRATISTA', 'CA_CNOMBRE', 'CA_CDESCRIPCION', 'CA_CARCHIVO', 'CA_CTIPO'
        ]
        widgets = {
            'CA_CONTRATISTA': forms.Select(attrs={'class': 'form-control'}),
            'CA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'CA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'CA_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'CA_CTIPO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formCONTRATISTA_ADJUNTO, self).__init__(*args, **kwargs)
        for field in ['CA_FFECHA_SUBIDA', 'CA_FFECHA_MODIFICACION', 'CA_CUSUARIO_CREADOR', 'CA_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for EMPLEADO_CONTRATISTA model
class formEMPLEADO_CONTRATISTA(forms.ModelForm):
    class Meta:
        model = EMPLEADO_CONTRATISTA
        fields = [
            'EC_CONTRATISTA', 'EC_CCODIGO', 'EC_CNOMBRE', 'EC_CAPELLIDO', 'EC_CRUT',
            'EC_CFECHA_NACIMIENTO', 'EC_CDIRECCION', 'EC_CTELEFONO', 'EC_CEMAIL',
            'EC_FFECHA_CONTRATACION', 'EC_CCARGO', 'EC_CESTADO'
        ]
        widgets = {
            'EC_CONTRATISTA': forms.Select(attrs={'class': 'form-control'}),
            'EC_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CAPELLIDO': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CRUT': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CFECHA_NACIMIENTO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'EC_CDIRECCION': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CTELEFONO': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CEMAIL': forms.EmailInput(attrs={'class': 'form-control'}),
            'EC_FFECHA_CONTRATACION': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'EC_CCARGO': forms.TextInput(attrs={'class': 'form-control'}),
            'EC_CESTADO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formEMPLEADO_CONTRATISTA, self).__init__(*args, **kwargs)
        for field in ['EC_FFECHA_CREACION', 'EC_FFECHA_MODIFICACION', 'EC_CUSUARIO_CREADOR', 'EC_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for EMPLEADO_CONTRATISTA_ADJUNTO model
class formEMPLEADO_CONTRATISTA_ADJUNTO(forms.ModelForm):
    class Meta:
        model = EMPLEADO_CONTRATISTA_ADJUNTO
        fields = [
            'ECA_EMPLEADO', 'ECA_CNOMBRE', 'ECA_CDESCRIPCION', 'ECA_CARCHIVO', 'ECA_CTIPO'
        ]
        widgets = {
            'ECA_EMPLEADO': forms.Select(attrs={'class': 'form-control'}),
            'ECA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'ECA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'ECA_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'ECA_CTIPO': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(formEMPLEADO_CONTRATISTA_ADJUNTO, self).__init__(*args, **kwargs)
        for field in ['ECA_FFECHA_SUBIDA', 'ECA_FFECHA_MODIFICACION', 'ECA_CUSUARIO_CREADOR', 'ECA_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for CONTRATO_CLIENTE model
class formCONTRATO_CLIENTE(forms.ModelForm):
    class Meta:
        model = CONTRATO_CLIENTE
        fields = [
            'CC_CCODIGO', 'CC_CLIENTE', 'CC_FFECHA_INICIO', 'CC_FFECHA_FIN', 'CC_NESTADO',
            'CC_NVALOR_TOTAL', 'CC_CTERMS_CONDICIONES', 'CC_COBSERVACIONES'
        ]
        widgets = {
            'CC_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'CC_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'CC_FFECHA_INICIO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'CC_FFECHA_FIN': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'CC_NESTADO': forms.Select(attrs={'class': 'form-control'}),
            'CC_NVALOR_TOTAL': forms.NumberInput(attrs={'class': 'form-control'}),
            'CC_CTERMS_CONDICIONES': forms.Textarea(attrs={'class': 'form-control'}),
            'CC_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formCONTRATO_CLIENTE, self).__init__(*args, **kwargs)
        for field in ['CC_FFECHA_CREACION', 'CC_FFECHA_MODIFICACION', 'CC_CUSUARIO_CREADOR', 'CC_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ANEXO model
class formANEXO(forms.ModelForm):
    class Meta:
        model = ANEXO
        fields = [
            'AN_CCODIGO', 'AN_CONTRATO', 'AN_CNOMBRE', 'AN_CDESCRIPCION', 'AN_CARCHIVO', 'AN_CTIPO'
        ]
        widgets = {
            'AN_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'AN_CONTRATO': forms.Select(attrs={'class': 'form-control'}),
            'AN_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'AN_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'AN_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'AN_CTIPO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formANEXO, self).__init__(*args, **kwargs)
        self.fields['AN_FFECHA_SUBIDA'].widget = forms.HiddenInput()
        self.fields['AN_FFECHA_MODIFICACION'].widget = forms.HiddenInput()
        self.fields['AN_CUSUARIO_CREADOR'].widget = forms.HiddenInput()
        self.fields['AN_CUSUARIO_MODIFICADOR'].widget = forms.HiddenInput()

# Form for PROYECTO_CLIENTE model

class formPROYECTO_CLIENTE(forms.ModelForm):
    class Meta:
        model = PROYECTO_CLIENTE
        fields = [
            # Basic Project Information
            'PC_CCODIGO', 'PC_CNOMBRE', 'PC_CDESCRIPCION','PC_CLIDER_TECNICO',
            'PC_CCATEGORIA', 'PC_CTIPO', 'PC_CUNIDAD_NEGOCIO',
            
            # Client Information
            'PC_CLIENTE', 'PC_CONTACTO_CLIENTE', 'PC_DIRECCION_CLIENTE',
            
            # Project Dates
            'PC_FFECHA_INICIO', 'PC_FFECHA_FIN_ESTIMADA', 'PC_FFECHA_FIN_REAL',
            
            # Project Status and Observations
            'PC_CESTADO', 'PC_COBSERVACIONES',
            
            # Financial Information
            'PC_NPRESUPUESTO', 'PC_MONEDA',
            
            # Time and Cost Estimates
            'PC_NVALOR_HORA', 'PC_NHORAS_ESTIMADAS', 'PC_NCOSTO_ESTIMADO',
            
            # Actual Time and Cost (can be filled later)
            'PC_NHORAS_REALES', 'PC_NCOSTO_REAL',
            
            # Profit Margin
            'PC_NMARGEN'
        ]
        labels = {
            'PC_CCODIGO': 'Código de proyecto',
            'PC_CNOMBRE': 'Nombre del proyecto',
            'PC_CDESCRIPCION': 'Descripción del proyecto',
            'PC_CLIDER_TECNICO': 'Líder Técnico',
            'PC_CCATEGORIA': 'Categoría del proyecto',
            'PC_CTIPO': 'Tipo de proyecto',
            'PC_CUNIDAD_NEGOCIO': 'Unidad de Negocio',
            'PC_CLIENTE': 'Cliente',
            'PC_CONTACTO_CLIENTE': 'Contacto del cliente',
            'PC_DIRECCION_CLIENTE': 'Dirección del cliente',
            'PC_FFECHA_INICIO': 'Fecha de inicio',
            'PC_FFECHA_FIN_ESTIMADA': 'Fecha de fin estimada',
            'PC_FFECHA_FIN_REAL': 'Fecha de fin real',
            'PC_CESTADO': 'Estado del proyecto',
            'PC_COBSERVACIONES': 'Observaciones',
            'PC_NPRESUPUESTO': 'Presupuesto',
            'PC_MONEDA': 'Moneda',
            'PC_NVALOR_HORA': 'Valor por hora',
            'PC_NHORAS_ESTIMADAS': 'Horas estimadas',
            'PC_NCOSTO_ESTIMADO': 'Costo estimado',
            'PC_NHORAS_REALES': 'Horas reales',
            'PC_NCOSTO_REAL': 'Costo real',
            'PC_NMARGEN': 'Margen (%)'
        }
        widgets = {
            'PC_CCODIGO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CNOMBRE': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CLIDER_TECNICO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CCATEGORIA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CTIPO': forms.Select(attrs={'class': 'js-example-basic-single form-control', 'style': 'width: 480px;'}),
            'PC_CUNIDAD_NEGOCIO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CLIENTE': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_CONTACTO_CLIENTE': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_DIRECCION_CLIENTE': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_FFECHA_INICIO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'PC_FFECHA_FIN_ESTIMADA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'PC_FFECHA_FIN_REAL': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'PC_CESTADO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NPRESUPUESTO': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NVALOR_HORA': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NHORAS_ESTIMADAS': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NCOSTO_ESTIMADO': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NHORAS_REALES': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NCOSTO_REAL': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'PC_NMARGEN': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 480px;'})
        }

    def __init__(self, *args, **kwargs):
        super(formPROYECTO_CLIENTE, self).__init__(*args, **kwargs)
        
        self.fields['PC_FFECHA_FIN_REAL'].required = False
        
        for field in ['PC_FFECHA_CREACION', 'PC_FFECHA_MODIFICACION', 'PC_CUSUARIO_CREADOR', 'PC_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('PC_FFECHA_INICIO')
        fecha_fin_estimada = cleaned_data.get('PC_FFECHA_FIN_ESTIMADA')
        fecha_fin_real = cleaned_data.get('PC_FFECHA_FIN_REAL')

        if fecha_inicio and fecha_fin_estimada and fecha_fin_estimada < fecha_inicio:
            self.add_error('PC_FFECHA_FIN_ESTIMADA', 'La fecha de fin estimada no puede ser menor a la fecha de inicio.')

        if fecha_inicio and fecha_fin_real and fecha_fin_real < fecha_inicio:
            self.add_error('PC_FFECHA_FIN_REAL', 'La fecha de fin real no puede ser menor a la fecha de inicio.')

        return cleaned_data

# Form for ETAPA model
class formETAPA(forms.ModelForm):
    class Meta:
        model = ETAPA
        fields = [
            'ET_CCODIGO', 'ET_CNOMBRE', 'ET_CDESCRIPCION'
        ]
        widgets = {
            'ET_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'ET_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'ET_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(formETAPA, self).__init__(*args, **kwargs)
        for field in ['ET_FFECHA_CREACION', 'ET_FFECHA_MODIFICACION',  
                      'ET_CUSUARIO_CREADOR', 'ET_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for TAREA_GENERAL model
class formTAREA_GENERAL(forms.ModelForm):
    TG_CCODIGO = forms.CharField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = TAREA_GENERAL
        fields = [
            'TG_CCODIGO', 'TG_PROYECTO_CLIENTE', 'TG_CNOMBRE', 'TG_CDESCRIPCION', 'TG_FFECHA_INICIO',
            'TG_FFECHA_FIN_ESTIMADA', 'TG_FFECHA_FIN_REAL', 'TG_CESTADO', 'TG_NPRESUPUESTO','TG_MONEDA',
            'TG_COBSERVACIONES', 'TG_BMILESTONE', 'TG_NPROGRESO', 'TG_NDURACION_PLANIFICADA',
            'TG_NDURACION_REAL', 'TG_BCRITICA'
        ]
        widgets = {
            'TG_PROYECTO_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'TG_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'TG_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'TG_FFECHA_INICIO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TG_FFECHA_FIN_ESTIMADA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TG_FFECHA_FIN_REAL': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TG_CESTADO': forms.Select(attrs={'class': 'form-control'}),
            'TG_NPRESUPUESTO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TG_MONEDA': forms.Select(attrs={'class': 'form-control'}),
            'TG_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control'}),
            'TG_BMILESTONE': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'TG_NPROGRESO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'TG_NDURACION_PLANIFICADA': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TG_NDURACION_REAL': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TG_BCRITICA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formTAREA_GENERAL, self).__init__(*args, **kwargs)
        for field in ['TG_FFECHA_CREACION', 'TG_FFECHA_MODIFICACION', 
                      'TG_CUSUARIO_CREADOR', 'TG_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
        
        # Generamos el código automáticamente si es una nueva instancia
        if not self.instance.pk:
            self.generate_code()

    def generate_code(self):
        if self.data.get('TG_PROYECTO_CLIENTE') :
            proyecto = PROYECTO_CLIENTE.objects.get(id=self.data['TG_PROYECTO_CLIENTE'])
            
            tarea_count = TAREA_GENERAL.objects.filter(TG_PROYECTO_CLIENTE=proyecto, ).count() + 1
            self.initial['TG_CCODIGO'] = f"{proyecto.PC_CCODIGO}-TG{tarea_count:03d}"

    def clean(self):
        cleaned_data = super().clean()
        for field in ['TG_NPRESUPUESTO', 'TG_NPROGRESO', 'TG_NDURACION_PLANIFICADA', 'TG_NDURACION_REAL']:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, "Este campo no puede ser negativo.")
        
        progreso = cleaned_data.get('TG_NPROGRESO')
        if progreso is not None and progreso > 100:
            self.add_error('TG_NPROGRESO', "El progreso no puede ser mayor a 100.")
        
        fecha_inicio = cleaned_data.get('TG_FFECHA_INICIO')
        fecha_fin_estimada = cleaned_data.get('TG_FFECHA_FIN_ESTIMADA')
        fecha_fin_real = cleaned_data.get('TG_FFECHA_FIN_REAL')
        
        if fecha_inicio and fecha_fin_estimada and fecha_fin_estimada < fecha_inicio:
            self.add_error('TG_FFECHA_FIN_ESTIMADA', "La fecha fin estimada no puede ser menor a la fecha de inicio.")
        
        if fecha_inicio and fecha_fin_real and fecha_fin_real < fecha_inicio:
            self.add_error('TG_FFECHA_FIN_REAL', "La fecha fin real no puede ser menor a la fecha de inicio.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super(formTAREA_GENERAL, self).save(commit=False)
        
        if not instance.TG_CCODIGO:
            self.generate_code()
            instance.TG_CCODIGO = self.initial['TG_CCODIGO']
        
        if commit:
            instance.save()
        return instance

# Form for TAREA_INGENIERIA model
class formTAREA_INGENIERIA(forms.ModelForm):
    TI_CCODIGO = forms.CharField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = TAREA_INGENIERIA
        fields = [
            'TI_CCODIGO', 'TI_PROYECTO_CLIENTE', 'TI_CNOMBRE', 'TI_CDESCRIPCION',  'TI_FFECHA_INICIO',
            'TI_FFECHA_FIN_ESTIMADA', 'TI_FFECHA_FIN_REAL', 'TI_CESTADO', 'TI_NPRESUPUESTO','TI_MONEDA',
            'TI_COBSERVACIONES', 'TI_BMILESTONE', 'TI_NPROGRESO', 'TI_NDURACION_PLANIFICADA',
            'TI_NDURACION_REAL', 'TG_BCRITICA'
        ]
        widgets = {
            'TI_PROYECTO_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'TI_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'TI_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'TI_FFECHA_INICIO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TI_FFECHA_FIN_ESTIMADA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TI_FFECHA_FIN_REAL': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TI_CESTADO': forms.Select(attrs={'class': 'form-control'}),
            'TI_NPRESUPUESTO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TI_MONEDA': forms.Select(attrs={'class': 'form-control'}),
            'TI_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control'}),
            'TI_BMILESTONE': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'TI_NPROGRESO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'TI_NDURACION_PLANIFICADA': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TI_NDURACION_REAL': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TG_BCRITICA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formTAREA_INGENIERIA, self).__init__(*args, **kwargs)
        for field in ['TI_FFECHA_CREACION', 'TI_FFECHA_MODIFICACION', 
                      'TI_CUSUARIO_CREADOR', 'TI_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
        
        # Generamos el código automáticamente si es una nueva instancia
        if not self.instance.pk:
            self.generate_code()

    def generate_code(self):
        if self.data.get('TI_PROYECTO_CLIENTE') :
            proyecto = PROYECTO_CLIENTE.objects.get(id=self.data['TI_PROYECTO_CLIENTE'])
            
            tarea_count = TAREA_INGENIERIA.objects.filter(TI_PROYECTO_CLIENTE=proyecto).count() + 1
            self.initial['TI_CCODIGO'] = f"{proyecto.PC_CCODIGO}-TI{tarea_count:03d}"

    def clean(self):
        cleaned_data = super().clean()
        for field in ['TI_NPRESUPUESTO', 'TI_NPROGRESO', 'TI_NDURACION_PLANIFICADA', 'TI_NDURACION_REAL']:
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, "Este campo no puede ser negativo.")
        
        progreso = cleaned_data.get('TI_NPROGRESO')
        if progreso is not None and progreso > 100:
            self.add_error('TI_NPROGRESO', "El progreso no puede ser mayor a 100.")
        
        fecha_inicio = cleaned_data.get('TI_FFECHA_INICIO')
        fecha_fin_estimada = cleaned_data.get('TI_FFECHA_FIN_ESTIMADA')
        fecha_fin_real = cleaned_data.get('TI_FFECHA_FIN_REAL')
        
        if fecha_inicio and fecha_fin_estimada and fecha_fin_estimada < fecha_inicio:
            self.add_error('TI_FFECHA_FIN_ESTIMADA', "La fecha fin estimada no puede ser menor a la fecha de inicio.")
        
        if fecha_inicio and fecha_fin_real and fecha_fin_real < fecha_inicio:
            self.add_error('TI_FFECHA_FIN_REAL', "La fecha fin real no puede ser menor a la fecha de inicio.")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super(formTAREA_INGENIERIA, self).save(commit=False)
        
        if not instance.TI_CCODIGO:
            self.generate_code()
            instance.TI_CCODIGO = self.initial['TI_CCODIGO']
        
        if commit:
            instance.save()
        return instance

# Formulario para TAREA_FINANCIERA
class formTAREA_FINANCIERA(forms.ModelForm):
    TF_CCODIGO = forms.CharField(widget=forms.HiddenInput(), required=False, label='')

    class Meta:
        model = TAREA_FINANCIERA
        fields = [
            'TF_CCODIGO', 'TF_PROYECTO_CLIENTE', 'TF_CNOMBRE', 'TF_CDESCRIPCION',  'TF_FFECHA_INICIO',
            'TF_FFECHA_FIN_ESTIMADA', 'TF_FFECHA_FIN_REAL', 'TF_CESTADO', 'TF_NMONTO','TF_MONEDA',
            'TF_CTIPO_TRANSACCION', 'TF_COBSERVACIONES', 'TF_BMILESTONE', 'TF_NPROGRESO', 
            'TF_NDURACION_PLANIFICADA', 'TF_NDURACION_REAL', 'TG_BCRITICA'
        ]
        widgets = {
            'TF_PROYECTO_CLIENTE': forms.Select(attrs={'class': 'form-control'}),
            'TF_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'TF_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'TF_FFECHA_INICIO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TF_FFECHA_FIN_ESTIMADA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TF_FFECHA_FIN_REAL': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'TF_CESTADO': forms.Select(attrs={'class': 'form-control'}),
            'TF_NMONTO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TF_MONEDA': forms.Select(attrs={'class': 'form-control'}),
            'TF_CTIPO_TRANSACCION': forms.TextInput(attrs={'class': 'form-control'}),
            'TF_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control'}),
            'TF_BMILESTONE': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
            'TF_NPROGRESO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'TF_NDURACION_PLANIFICADA': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TF_NDURACION_REAL': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'TG_BCRITICA': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-left: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formTAREA_FINANCIERA, self).__init__(*args, **kwargs)
        for field in ['TF_FFECHA_CREACION', 'TF_FFECHA_MODIFICACION', 
                      'TF_CUSUARIO_CREADOR', 'TF_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
        
        # Generamos el código automáticamente si es una nueva instancia
        if not self.instance.pk:
            self.generate_code()

    def generate_code(self):
        if self.data.get('TF_PROYECTO_CLIENTE'):
            proyecto = PROYECTO_CLIENTE.objects.get(id=self.data['TF_PROYECTO_CLIENTE'])
            
            tarea_count = TAREA_FINANCIERA.objects.filter(TF_PROYECTO_CLIENTE=proyecto).count() + 1
            self.initial['TF_CCODIGO'] = f"{proyecto.PC_CCODIGO}-TF{tarea_count:03d}"

    def clean(self):
        cleaned_data = super().clean()
    def save(self, commit=True):
        instance = super(formTAREA_FINANCIERA, self).save(commit=False)
        
        if not instance.TF_CCODIGO:
            self.generate_code()
            instance.TF_CCODIGO = self.initial['TF_CCODIGO']
        
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('TF_FFECHA_INICIO')
        fecha_fin_estimada = cleaned_data.get('TF_FFECHA_FIN_ESTIMADA')

        if fecha_inicio and not fecha_fin_estimada:
            cleaned_data['TF_FFECHA_FIN_ESTIMADA'] = fecha_inicio
        elif fecha_fin_estimada and not fecha_inicio:
            cleaned_data['TF_FFECHA_INICIO'] = fecha_fin_estimada

        return cleaned_data

# Form for ADJUNTO_TAREA_GENERAL model
class formADJUNTO_TAREA_GENERAL(forms.ModelForm):
    class Meta:
        model = ADJUNTO_TAREA_GENERAL
        fields = ['AT_TAREA', 'AT_CARCHIVO', 'AT_CNOMBRE', 'AT_CDESCRIPCION']
        widgets = {
            'AT_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'AT_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'AT_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'AT_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formADJUNTO_TAREA_GENERAL, self).__init__(*args, **kwargs)
        hidden_fields = ['AT_FFECHA_CREACION', 'AT_FFECHA_MODIFICACION', 'AT_CUSUARIO_CREADOR', 'AT_CUSUARIO_MODIFICADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ADJUNTO_TAREA_INGENIERIA model
class formADJUNTO_TAREA_INGENIERIA(forms.ModelForm):
    class Meta:
        model = ADJUNTO_TAREA_INGENIERIA
        fields = ['ATI_TAREA', 'ATI_CARCHIVO', 'ATI_CNOMBRE', 'ATI_CDESCRIPCION']
        widgets = {
            'ATI_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'ATI_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'ATI_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'ATI_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['ATI_FFECHA_CREACION', 'ATI_FFECHA_MODIFICACION', 'ATI_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ADJUNTO_TAREA_FINANCIERA model
class formADJUNTO_TAREA_FINANCIERA(forms.ModelForm):
    class Meta:
        model = ADJUNTO_TAREA_FINANCIERA
        fields = ['ATF_TAREA', 'ATF_CARCHIVO', 'ATF_CNOMBRE', 'ATF_CDESCRIPCION']
        widgets = {
            'ATF_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'ATF_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'ATF_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'ATF_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['ATF_FFECHA_CREACION', 'ATF_FFECHA_MODIFICACION', 'ATF_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

class AdjuntoTareaForm(forms.Form):
    CARCHIVO = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    CNOMBRE = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    CDESCRIPCION = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        self.tipo_tarea = kwargs.pop('tipo_tarea', None)
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        if self.tipo_tarea:
            prefix = self.get_prefix()
            self.fields['CARCHIVO'].label = f'{prefix}_CARCHIVO'
            self.fields['CNOMBRE'].label = f'{prefix}_CNOMBRE'
            self.fields['CDESCRIPCION'].label = f'{prefix}_CDESCRIPCION'
        
        if self.is_edit:
            self.fields['CARCHIVO'].required = False

    def get_prefix(self):
        if self.tipo_tarea == 'TAREA_GENERAL':
            return 'AT'
        elif self.tipo_tarea == 'TAREA_INGENIERIA':
            return 'ATI'
        elif self.tipo_tarea == 'TAREA_FINANCIERA':
            return 'ATF'
        return ''

    def save(self, commit=True):
        if self.tipo_tarea == 'TAREA_GENERAL':
            instance = ADJUNTO_TAREA_GENERAL()
        elif self.tipo_tarea == 'TAREA_INGENIERIA':
            instance = ADJUNTO_TAREA_INGENIERIA()
        elif self.tipo_tarea == 'TAREA_FINANCIERA':
            instance = ADJUNTO_TAREA_FINANCIERA()
        else:
            raise ValueError("Tipo de tarea no válido")

        prefix = self.get_prefix()
        setattr(instance, f'{prefix}_CARCHIVO', self.cleaned_data['CARCHIVO'])
        setattr(instance, f'{prefix}_CNOMBRE', self.cleaned_data['CNOMBRE'])
        setattr(instance, f'{prefix}_CDESCRIPCION', self.cleaned_data['CDESCRIPCION'])

        if commit:
            instance.save()
        return instance

# Form for ADJUNTO_ETAPA model
class formADJUNTO_ETAPA(forms.ModelForm):
    class Meta:
        model = ADJUNTO_ETAPA
        fields = ['AE_ETAPA', 'AE_CARCHIVO', 'AE_CNOMBRE', 'AE_CDESCRIPCION']
        widgets = {
            'AE_ETAPA': forms.Select(attrs={'class': 'form-control'}),
            'AE_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'AE_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'AE_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AE_FFECHA_CREACION', 'AE_FFECHA_MODIFICACION', 'AE_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_TAREA_INGENIERIA model
class formASIGNACION_EMPLEADO_TAREA_INGENIERIA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_TAREA_INGENIERIA
        fields = ['AE_EMPLEADO', 'AE_TAREA', 'AE_CESTADO']
        widgets = {
            'AE_EMPLEADO': forms.Select(attrs={'class': 'form-control'}),
            'AE_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'AE_CESTADO': forms.Select(attrs={'class': 'form-control'}),            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AE_FFECHA_ASIGNACION', 'AE_FFECHA_FINALIZACION', 'AE_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_TAREA_FINANCIERA model
class formASIGNACION_EMPLEADO_TAREA_FINANCIERA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_TAREA_FINANCIERA
        fields = ['AE_EMPLEADO', 'AE_CESTADO']
        widgets = {
            'AE_EMPLEADO': forms.Select(attrs={'class': 'js-example-basic-multiple form-control'}),            
            'AE_CESTADO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AE_FFECHA_ASIGNACION', 'AE_FFECHA_FINALIZACION', 'AE_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_TAREA_GENERAL model
class formASIGNACION_EMPLEADO_TAREA_GENERAL(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_TAREA_GENERAL
        fields = ['AE_EMPLEADO', 'AE_CESTADO']
        widgets = {
            'AE_EMPLEADO': forms.Select(attrs={'class': 'js-example-basic-multiple form-control'}),            
            'AE_CESTADO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AE_FFECHA_ASIGNACION', 'AE_FFECHA_FINALIZACION', 'AE_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA model
class formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA
        fields = ['AEC_EMPLEADO', 'AEC_TAREA', 'AEC_CESTADO']
        widgets = {
            'AEC_EMPLEADO': forms.Select(attrs={'class': 'form-control'}),
            'AEC_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'AEC_CESTADO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AEC_FFECHA_ASIGNACION', 'AEC_FFECHA_FINALIZACION', 'AEC_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA model
class formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA
        fields = ['AEC_EMPLEADO', 'AEC_CESTADO']
        widgets = {
            'AEC_EMPLEADO': forms.Select(attrs={'class': 'js-example-basic-multiple form-control'}),
            'AEC_CESTADO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AEC_FFECHA_ASIGNACION', 'AEC_FFECHA_FINALIZACION', 'AEC_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL model
class formASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL(forms.ModelForm):
    class Meta:
        model = ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL
        fields = ['AEC_EMPLEADO', 'AEC_TAREA', 'AEC_CESTADO']
        widgets = {
            'AEC_EMPLEADO': forms.Select(attrs={'class': 'form-control'}),
            'AEC_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'AEC_CESTADO': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['AEC_FFECHA_ASIGNACION', 'AEC_FFECHA_FINALIZACION', 'AEC_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for ASIGNACION_RECURSO_TAREA_GENERAL model
class formASIGNACION_RECURSO_TAREA_GENERAL(forms.ModelForm):
    class Meta:
        model = ASIGNACION_RECURSO_TAREA_GENERAL
        fields = ['ART_TAREA', 'ART_PRODUCTO', 'ART_CANTIDAD', 'ART_COSTO_UNITARIO','ART_MONEDA']
        widgets = {
            'ART_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'ART_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'ART_CANTIDAD': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_COSTO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['ART_COSTO_TOTAL', 'ART_FFECHA_ASIGNACION', 'ART_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('ART_CANTIDAD')
        costo_unitario = cleaned_data.get('ART_COSTO_UNITARIO')

        if cantidad is not None and cantidad < 0:
            self.add_error('ART_CANTIDAD', 'La cantidad no puede ser negativa.')
        if costo_unitario is not None and costo_unitario < 0:
            self.add_error('ART_COSTO_UNITARIO', 'El costo unitario no puede ser negativo.')

        return cleaned_data

# Form for ASIGNACION_RECURSO_TAREA_INGENIERIA model
class formASIGNACION_RECURSO_TAREA_INGENIERIA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_RECURSO_TAREA_INGENIERIA
        fields = ['ART_TAREA', 'ART_PRODUCTO', 'ART_CANTIDAD', 'ART_COSTO_UNITARIO','ART_MONEDA']
        widgets = {
            'ART_TAREA': forms.Select(attrs={'class': 'form-control'}),
            'ART_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'ART_CANTIDAD': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_COSTO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['ART_COSTO_TOTAL', 'ART_FFECHA_ASIGNACION', 'ART_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('ART_CANTIDAD')
        costo_unitario = cleaned_data.get('ART_COSTO_UNITARIO')

        if cantidad is not None and cantidad < 0:
            self.add_error('ART_CANTIDAD', 'La cantidad no puede ser negativa.')
        if costo_unitario is not None and costo_unitario < 0:
            self.add_error('ART_COSTO_UNITARIO', 'El costo unitario no puede ser negativo.')

        return cleaned_data

# Form for ASIGNACION_RECURSO_TAREA_FINANCIERA model
class formASIGNACION_RECURSO_TAREA_FINANCIERA(forms.ModelForm):
    class Meta:
        model = ASIGNACION_RECURSO_TAREA_FINANCIERA
        fields = ['ART_PRODUCTO', 'ART_CANTIDAD', 'ART_COSTO_UNITARIO','ART_MONEDA']
        widgets = {            
            'ART_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'ART_CANTIDAD': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_COSTO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'ART_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hidden_fields = ['ART_COSTO_TOTAL', 'ART_FFECHA_ASIGNACION', 'ART_CUSUARIO_CREADOR']
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('ART_CANTIDAD')
        costo_unitario = cleaned_data.get('ART_COSTO_UNITARIO')

        if cantidad is not None and cantidad < 0:
            self.add_error('ART_CANTIDAD', 'La cantidad no puede ser negativa.')
        if costo_unitario is not None and costo_unitario < 0:
            self.add_error('ART_COSTO_UNITARIO', 'El costo unitario no puede ser negativo.')

        return cleaned_data

# Form for ACTA_REUNION model
class formACTA_REUNION(forms.ModelForm):
    class Meta:
        model = ACTA_REUNION
        fields = ['AR_ETAPA', 'AR_CTITULO', 'AR_CFECHA', 'AR_CLUGAR', 'AR_CPARTICIPANTES', 'AR_CAGENDA', 'AR_CCONTENIDO', 'AR_CACUERDOS', 'AR_CARCHIVO']
        widgets = {
            'AR_ETAPA': forms.Select(attrs={'class': 'form-control'}),
            'AR_CTITULO': forms.TextInput(attrs={'class': 'form-control'}),
            'AR_CFECHA': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'AR_CLUGAR': forms.TextInput(attrs={'class': 'form-control'}),
            'AR_CPARTICIPANTES': forms.Textarea(attrs={'class': 'form-control'}),
            'AR_CAGENDA': forms.Textarea(attrs={'class': 'form-control'}),
            'AR_CCONTENIDO': forms.Textarea(attrs={'class': 'form-control'}),
            'AR_CACUERDOS': forms.Textarea(attrs={'class': 'form-control'}),
            'AR_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formACTA_REUNION, self).__init__(*args, **kwargs)
        hidden_fields = [
            'AR_FFECHA_CREACION',
            'AR_FFECHA_MODIFICACION', 
            'AR_CUSUARIO_CREADOR',
            'AR_CUSUARIO_MODIFICADOR'
        ]
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for PROYECTO_ADJUNTO model
class formPROYECTO_ADJUNTO(forms.ModelForm):
    class Meta:
        model = PROYECTO_ADJUNTO
        fields = ['PA_CNOMBRE', 'PA_CDESCRIPCION', 'PA_CARCHIVO', 'PA_CTIPO']
        widgets = {            
            'PA_CNOMBRE': forms.TextInput(attrs={'class': 'form-control'}),
            'PA_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'PA_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'PA_CTIPO': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formPROYECTO_ADJUNTO, self).__init__(*args, **kwargs)
        self.fields['PA_CDESCRIPCION'].required = False

# Form for BOLETA_GARANTIA model
class formBOLETA_GARANTIA(forms.ModelForm):
    class Meta:
        model = BOLETA_GARANTIA
        fields = ['BG_PROYECTO', 'BG_CNUMERO','BG_MONEDA', 'BG_CMONTO', 'BG_CENTIDAD_EMISORA', 'BG_FFECHA_EMISION', 'BG_FFECHA_VENCIMIENTO', 'BG_CESTADO', 'BG_CARCHIVO', 'BG_COBSERVACIONES']
        widgets = {
            'BG_PROYECTO': forms.Select(attrs={'class': 'form-control'}),
            'BG_CNUMERO': forms.TextInput(attrs={'class': 'form-control'}),
            'BG_MONEDA': forms.Select(attrs={'class': 'form-control'}),
            'BG_CMONTO': forms.NumberInput(attrs={'class': 'form-control'}),
            'BG_CENTIDAD_EMISORA': forms.TextInput(attrs={'class': 'form-control'}),
            'BG_FFECHA_EMISION': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'BG_FFECHA_VENCIMIENTO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'BG_CESTADO': forms.Select(attrs={'class': 'form-control'}),
            'BG_CARCHIVO': forms.FileInput(attrs={'class': 'form-control'}),
            'BG_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(formBOLETA_GARANTIA, self).__init__(*args, **kwargs)
        hidden_fields = [
            'BG_FFECHA_CREACION',
            'BG_FFECHA_MODIFICACION', 
            'BG_CUSUARIO_CREADOR',
            'BG_CUSUARIO_MODIFICADOR'
        ]
        for field in hidden_fields:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

# Form for TAREA_GENERAL_DEPENDENCIA model
class formTAREA_GENERAL_DEPENDENCIA(forms.ModelForm):
    class Meta:
        model = TAREA_GENERAL_DEPENDENCIA
        fields = ['TD_TAREA_SUCESORA', 'TD_TIPO_DEPENDENCIA']
        widgets = {            
            'TD_TAREA_SUCESORA': forms.Select(attrs={'class': 'form-control'}),
            'TD_TIPO_DEPENDENCIA': forms.Select(attrs={'class': 'form-control'}),
        }

# Form for TAREA_FINANCIERA_DEPENDENCIA model
class formTAREA_FINANCIERA_DEPENDENCIA(forms.ModelForm):
    class Meta:
        model = TAREA_FINANCIERA_DEPENDENCIA
        fields = ['TD_TAREA_SUCESORA', 'TD_TIPO_DEPENDENCIA']
        widgets = {            
            'TD_TAREA_SUCESORA': forms.Select(attrs={'class': 'form-control'}),
            'TD_TIPO_DEPENDENCIA': forms.Select(attrs={'class': 'form-control'}),
        }

# Form for TAREA_INGENIERIA_DEPENDENCIA model
class formTAREA_INGENIERIA_DEPENDENCIA(forms.ModelForm):
    class Meta:
        model = TAREA_INGENIERIA_DEPENDENCIA
        fields = ['TD_TAREA_SUCESORA', 'TD_TIPO_DEPENDENCIA']
        widgets = {            
            'TD_TAREA_SUCESORA': forms.Select(attrs={'class': 'form-control'}),
            'TD_TIPO_DEPENDENCIA': forms.Select(attrs={'class': 'form-control'}),
        }

class formQUERY(forms.ModelForm):
    class Meta:
        model = QUERY
        fields = ['QR_CNOMBRE', 'QR_CLABEL_FIELDS' , 'QR_CDESCRIPCION', 'QR_CQUERY', 'QR_NHABILITADO']
        labels = {
            'QR_CNOMBRE': 'Ingrese nombre',
            'QR_CLABEL_FIELDS': 'Ingrese etiquetas',
            'QR_CDESCRIPCION': 'Ingrese descripción',
            'QR_CQUERY': 'Ingrese consulta',
            'QR_NHABILITADO': 'Habilitado',
        }
        widgets = {
            'QR_CNOMBRE': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Ingrese nombre'}),
            'QR_CLABEL_FIELDS': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese etiquetas'}),
            'QR_CDESCRIPCION': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese descripción'}),
            'QR_CQUERY': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese consulta'}),
            'QR_NHABILITADO': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'switch-s-2'}),
        }

class formESTADO_DE_PAGO(forms.ModelForm):
    class Meta:
        model = ESTADO_DE_PAGO
        fields = [
            'EP_PROYECTO', 'EP_CNUMERO', 'EP_FFECHA', 'EP_CESTADO',
            'EP_NTOTAL','EP_MONEDA', 'EP_COBSERVACIONES', 'EP_CESTADO_PAGO',
            'EP_NMONTO_PAGADO', 'EP_FFECHA_ULTIMO_PAGO'
        ]
        labels = {
            'EP_PROYECTO': 'Proyecto cliente',
            'EP_CNUMERO': 'Número de estado de pago',
            'EP_FFECHA': 'Fecha de estado de pago',
            'EP_CESTADO': 'Estado',
            'EP_NTOTAL': 'Total',
            'EP_MONEDA': 'Moneda',
            'EP_COBSERVACIONES': 'Observaciones',
            'EP_CESTADO_PAGO': 'Estado de pago',
            'EP_NMONTO_PAGADO': 'Monto pagado',
            'EP_FFECHA_ULTIMO_PAGO': 'Fecha del último pago'
        }
        widgets = {
            'EP_PROYECTO': forms.Select(attrs={'class': 'form-control'}),
            'EP_CNUMERO': forms.TextInput(attrs={'class': 'form-control'}),
            'EP_FFECHA': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'EP_CESTADO': forms.Select(attrs={'class': 'form-control'}),
            'EP_NTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EP_MONEDA': forms.Select(attrs={'class': 'form-control'}),
            'EP_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'EP_CESTADO_PAGO': forms.Select(attrs={'class': 'form-control'}),
            'EP_NMONTO_PAGADO': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EP_FFECHA_ULTIMO_PAGO': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(formESTADO_DE_PAGO, self).__init__(*args, **kwargs)
        for field in ['EP_FFECHA_CREACION', 'EP_FFECHA_MODIFICACION', 'EP_CUSUARIO_CREADOR', 'EP_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        ep_ntotal = cleaned_data.get('EP_NTOTAL')
        ep_nmonto_pagado = cleaned_data.get('EP_NMONTO_PAGADO')

        if ep_ntotal and ep_nmonto_pagado:
            if ep_nmonto_pagado > ep_ntotal:
                raise forms.ValidationError("El monto pagado no puede ser mayor que el total.")

        return cleaned_data
    
class formEDP_DETALLE(forms.ModelForm):
    class Meta:
        model = ESTADO_DE_PAGO_DETALLE
        fields = [
            'EDD_ESTADO_DE_PAGO', 'EDD_PRODUCTO', 'EDD_NCANTIDAD',
            'EDD_NPRECIO_UNITARIO', 'EDD_NSUBTOTAL', 'EDD_NDESCUENTO', 'EDD_NTOTAL'
        ]
        labels = {
            'EDD_ESTADO_DE_PAGO': 'Estado de Pago',
            'EDD_PRODUCTO': 'Producto',
            'EDD_NCANTIDAD': 'Cantidad',
            'EDD_NPRECIO_UNITARIO': 'Precio unitario',
            'EDD_NSUBTOTAL': 'Subtotal',
            'EDD_NDESCUENTO': 'Descuento',
            'EDD_NTOTAL': 'Total'
        }
        widgets = {
            'EDD_ESTADO_DE_PAGO': forms.Select(attrs={'class': 'form-control'}),
            'EDD_PRODUCTO': forms.Select(attrs={'class': 'form-control'}),
            'EDD_NCANTIDAD': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EDD_NPRECIO_UNITARIO': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EDD_NSUBTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EDD_NDESCUENTO': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'EDD_NTOTAL': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        super(formEDP_DETALLE, self).__init__(*args, **kwargs)
        for field in ['EDD_FFECHA_CREACION', 'EDD_FFECHA_MODIFICACION', 'EDD_CUSUARIO_CREADOR', 'EDD_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('EDD_NCANTIDAD')
        precio_unitario = cleaned_data.get('EDD_NPRECIO_UNITARIO')
        subtotal = cleaned_data.get('EDD_NSUBTOTAL')
        descuento = cleaned_data.get('EDD_NDESCUENTO')
        total = cleaned_data.get('EDD_NTOTAL')

        if cantidad and precio_unitario and subtotal:
            calculated_subtotal = cantidad * precio_unitario
            if abs(calculated_subtotal - subtotal) > 0.01:
                raise forms.ValidationError("El subtotal no coincide con la cantidad y el precio unitario.")

        if subtotal and descuento and total:
            calculated_total = subtotal - descuento
            if abs(calculated_total - total) > 0.01:
                raise forms.ValidationError("El total no coincide con el subtotal menos el descuento.")

        return cleaned_data
    
# Form for UNIDAD_NEGOCIO model
class formUNIDAD_NEGOCIO(forms.ModelForm):
    class Meta:
        model = UNIDAD_NEGOCIO
        fields = [
            'UN_CCODIGO', 'UN_CDESCRIPCION', 'UN_BHABILITADO',
        ]
        labels = {
            'UN_CCODIGO': 'Código',
            'UN_CDESCRIPCION': 'Descripción',
            'UN_BHABILITADO': 'Habilitado',
        }
        widgets = {
            'UN_CCODIGO': forms.TextInput(attrs={'class': 'form-control'}),
            'UN_CDESCRIPCION': forms.Textarea(attrs={'class': 'form-control'}),
            'UN_BHABILITADO': forms.CheckboxInput(attrs={'class': 'form-check-input','style': 'margin-left: 5px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(formUNIDAD_NEGOCIO, self).__init__(*args, **kwargs)
        for field in ['UN_FFECHA_CREACION']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()
                
class formFICHA_CIERRE(forms.ModelForm):
    class Meta:
        model = FICHA_CIERRE
        fields = [
            'FC_JEFE_DE_PROYECTO', 'FC_NOMBRE_DE_PROYECTO', 'FC_NUMERO_DE_PROYECTO',
            'FC_FECHA_DE_CIERRE', 'FC_HH_GASTADAS', 'FC_HH_COBRADAS',
            'FC_MONEDA', 'FC_EXCEDENTES', 'FC_PROYECCION_CON_EL_CLIENTE', 'FC_OBSERVACIONES'
        ]
        labels = {
            'FC_JEFE_DE_PROYECTO': 'Jefe de Proyecto',
            'FC_NOMBRE_DE_PROYECTO': 'Nombre de Proyecto',
            'FC_NUMERO_DE_PROYECTO': 'Número de Proyecto',
            'FC_FECHA_DE_CIERRE': 'Fecha de Cierre',
            'FC_HH_GASTADAS': 'Horas Hombre Gastadas',
            'FC_HH_COBRADAS': 'Horas Hombre Cobradas',
            'FC_MONEDA': 'Moneda',
            'FC_EXCEDENTES': 'Excedentes',
            'FC_PROYECCION_CON_EL_CLIENTE': 'Proyección con el Cliente',
            'FC_OBSERVACIONES': 'Observaciones'
        }
        widgets = {
            'FC_JEFE_DE_PROYECTO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FC_NOMBRE_DE_PROYECTO': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FC_NUMERO_DE_PROYECTO': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FC_FECHA_DE_CIERRE': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 480px;'}),
            'FC_HH_GASTADAS': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'style': 'width: 480px;'}),
            'FC_HH_COBRADAS': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'style': 'width: 480px;'}),
            'FC_MONEDA': forms.Select(attrs={'class': 'form-control', 'style': 'width: 480px;'}),
            'FC_EXCEDENTES': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'style': 'width: 480px;'}),
            'FC_PROYECCION_CON_EL_CLIENTE': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'style': 'width: 480px;'}),
            'FC_OBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'width: 480px;'})
        }

    def clean(self):
        cleaned_data = super().clean()
        hh_gastadas = cleaned_data.get('FC_HH_GASTADAS')
        hh_cobradas = cleaned_data.get('FC_HH_COBRADAS')

        if hh_gastadas and hh_cobradas:
            if hh_cobradas > hh_gastadas:
                raise forms.ValidationError("Las horas hombre cobradas no pueden ser mayores que las gastadas.")

        return cleaned_data

class formFICHA_CIERRE_DETALLE(forms.ModelForm):
    class Meta:
        model = FICHA_CIERRE_DETALLE
        fields = [
            'FCD_FICHA_CIERRE', 'FCD_CACTIVIDAD',
            'FCD_CCUMPLIMIENTO', 'FCD_COBSERVACIONES'
        ]
        labels = {
            'FCD_FICHA_CIERRE': 'Ficha de Cierre',
            'FCD_CACTIVIDAD': 'Actividad Técnica o Administrativa',
            'FCD_CCUMPLIMIENTO': '¿Cumple?',
            'FCD_COBSERVACIONES': 'Observaciones'
        }
        widgets = {
            'FCD_FICHA_CIERRE': forms.Select(attrs={'class': 'form-control'}),
            'FCD_CACTIVIDAD': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'FCD_CCUMPLIMIENTO': forms.Select(attrs={'class': 'form-control'}),
            'FCD_COBSERVACIONES': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(formFICHA_CIERRE_DETALLE, self).__init__(*args, **kwargs)
        for field in ['FCD_FFECHA_CREACION', 'FCD_FFECHA_MODIFICACION', 'FCD_CUSUARIO_CREADOR', 'FCD_CUSUARIO_MODIFICADOR']:
            if field in self.fields:
                self.fields[field].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        ficha_cierre = cleaned_data.get('FCD_FICHA_CIERRE')
        nactividad = cleaned_data.get('FCD_NACTIVIDAD')

        if ficha_cierre and nactividad:
            existing_detail = FICHA_CIERRE_DETALLE.objects.filter(
                FCD_FICHA_CIERRE=ficha_cierre, 
                FCD_NACTIVIDAD=nactividad
            ).exclude(pk=self.instance.pk if self.instance else None).first()

            if existing_detail:
                raise forms.ValidationError("Ya existe un detalle con este número de actividad para esta ficha de cierre.")

        return cleaned_data            