# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class REGION(models.Model):
    RG_CNOMBRE = models.CharField(("nombre region"), max_length=128, null=False)
    RG_CCODIGO = models.CharField(("codigo region"), max_length=128, null=False)

    def __str__(self):
        return self.RG_CNOMBRE

    class Meta:
        db_table = "REGION"

class PROVINCIA(models.Model):
    RG_NID = models.ForeignKey(REGION, verbose_name='region_id', on_delete=models.PROTECT)
    PV_CNOMBRE = models.CharField(("nombre provincia"), max_length=128, null=False)
    PV_CCODIGO = models.CharField(("codigo provincia"), max_length=128, null=False)

    def __str__(self):
        return self.PV_CNOMBRE

    class Meta:
        db_table = 'PROVINCIA'

class COMUNA(models.Model):
    PV_NID = models.ForeignKey(PROVINCIA, verbose_name="provincia_id", on_delete=models.PROTECT)
    COM_CNOMBRE = models.CharField(("nombre comuna"), max_length=128, null=False)
    COM_CCODIGO = models.CharField(("codigo comuna"), max_length=128, null=False)

    def __str__(self):
        return self.COM_CNOMBRE

    class Meta:
        db_table = "COMUNA"

class SYSTEM_LOG(models.Model):
    USER_CREATOR_ID	= models.ForeignKey(User, verbose_name='id usuario creador', on_delete=models.PROTECT, related_name='log_user_creator')
    LG_ACTION = models.CharField(max_length=255)
    LG_DESCRIPTION = models.TextField()
    LG_TIMESTAMP = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.USER_CREATOR_ID.username} - {self.LG_ACTION} - {self.LG_TIMESTAMP}"

    class Meta:
        db_table = 'SYSTEM_LOG'
        verbose_name = 'Log de sistema'
        verbose_name_plural = 'Logs de sistema'

class PARAMETRO(models.Model):

    PM_CGRUPO = models.CharField(max_length=255)	
    PM_CCODIGO = models.CharField(max_length=255)
    PM_CDESCRIPCION = models.TextField()
    PM_CVALOR = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.PM_CGRUPO} - {self.PM_CCODIGO} - {self.PM_CDESCRIPCION} - {self.PM_CVALOR}"

    class Meta:
        db_table = 'PARAMETRO'
        verbose_name = 'Parametro'
        verbose_name_plural = 'Parametros'

class ALERTA(models.Model):
    AL_USUARIO_ORIGEN = models.ForeignKey(User, verbose_name='Usuario origen', on_delete=models.PROTECT, related_name='alertas_enviadas')
    AL_USUARIO_DESTINO = models.ForeignKey(User, verbose_name='Usuario destino', on_delete=models.PROTECT, related_name='alertas_recibidas')
    AL_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    AL_FFECHA_ENVIO = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de envío')
    AL_FFECHA_LECTURA = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de lectura')
    AL_CCLASE = models.CharField(max_length=255, verbose_name='Clase')
    AL_CASUNTO = models.CharField(max_length=255, verbose_name='Asunto')
    AL_CCUERPO = models.TextField(verbose_name='Cuerpo')
    AL_BLEIDA = models.BooleanField(default=False, verbose_name='Leída')

    def __str__(self):
        return f"{self.USUARIO_ORIGEN.username} - {self.USUARIO_DESTINO.username} - {self.ASUNTO}"

    class Meta:
        db_table = 'ALERTA'
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'

class ROL(models.Model):
    RO_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del rol')
    RO_CDESCRIPCION = models.TextField(verbose_name='Descripción del rol')
    RO_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    RO_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    RO_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.RO_CNOMBRE

    class Meta:
        db_table = 'ROL'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

class CATEGORIA_PROYECTO(models.Model):
    CA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la categoría')
    CA_CDESCRIPCION = models.TextField(verbose_name='Descripción de la categoría')
    CA_BACTIVA = models.BooleanField(default=True, verbose_name='Activa')
    CA_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.CA_CNOMBRE

    class Meta:
        db_table = 'CATEGORIA'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class CATEGORIA_CLIENTE(models.Model):
    CA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la categoría')
    CA_CDESCRIPCION = models.TextField(verbose_name='Descripción de la categoría')
    CA_BACTIVA = models.BooleanField(default=True, verbose_name='Activa')
    CA_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.CA_CNOMBRE

    class Meta:
        db_table = 'CATEGORIA_CLIENTE'
        verbose_name = 'Categoría de Cliente'
        verbose_name_plural = 'Categorías de Clientes'

class TIPO_PROYECTO(models.Model):
    TP_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del tipo de documento')
    TP_CDESCRIPCION = models.TextField(verbose_name='Descripción del tipo de documento')
    TP_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    TP_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    TP_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.TP_CNOMBRE

    class Meta:
        db_table = 'TIPO_PROYECTO'
        verbose_name = 'Tipo de Proyecto'
        verbose_name_plural = 'Tipos de Proyectos'

class PERMISO(models.Model):
    PE_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del permiso')
    PE_CDESCRIPCION = models.TextField(verbose_name='Descripción del permiso')
    PE_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    PE_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    PE_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.PE_CNOMBRE

    class Meta:
        db_table = 'PERMISO'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

class PERMISO_ROL(models.Model):
    PR_CPERMISO = models.ForeignKey(PERMISO, on_delete=models.CASCADE, verbose_name='Permiso')
    PR_CROL = models.ForeignKey(ROL, on_delete=models.CASCADE, verbose_name='Rol')
    PR_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    PR_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    PR_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return f"{self.PR_CPERMISO} - {self.PR_CROL}"

    class Meta:
        db_table = 'PERMISO_ROL'
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Roles'
        unique_together = ('PR_CPERMISO', 'PR_CROL')

class USUARIO_ROL(models.Model):
    UR_CUSUARIO = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Usuario')
    UR_CROL = models.ForeignKey(ROL, on_delete=models.CASCADE, verbose_name='Rol')
    UR_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    UR_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    UR_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return f"{self.UR_CUSUARIO.username} - {self.UR_CROL}"

    class Meta:
        db_table = 'USUARIO_ROL'
        verbose_name = 'Usuario-Rol'
        verbose_name_plural = 'Usuarios-Roles'
        unique_together = ('UR_CUSUARIO', 'UR_CROL')

class CLIENTE(models.Model):
    CL_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la empresa')
    CL_CRUT = models.CharField(max_length=20, unique=True, verbose_name='RUT')
    CL_CDIRECCION = models.TextField(verbose_name='Dirección')
    CL_CREGION = models.ForeignKey('REGION', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Región')
    CL_CPROVINCIA = models.ForeignKey('PROVINCIA', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Provincia')
    CL_CCOMUNA = models.ForeignKey('COMUNA', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Comuna')
    CL_CTELEFONO = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    CL_CEMAIL = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Correo electrónico')
    CL_CPERSONA_CONTACTO = models.CharField(max_length=255, blank=True, null=True, verbose_name='Persona de contacto')
    CL_CSITIO_WEB = models.URLField(max_length=255, blank=True, null=True, verbose_name='Sitio web')
    CL_CRUBRO = models.CharField(max_length=255, blank=True, null=True, verbose_name='Rubro')
    CL_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    CL_BPROSPECTO = models.BooleanField(default=True, verbose_name='Prospecto')
    CL_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CL_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CL_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='clientes_creados', verbose_name='Usuario creador')
    CL_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='clientes_modificados', verbose_name='Usuario modificador')
    CL_CUSUARIO_GESTOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='clientes_gestionados', verbose_name='Usuario gestor')
    CL_CCATEGORIA = models.ForeignKey('CATEGORIA_CLIENTE', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría del cliente')
    def __str__(self):
        return self.CL_CNOMBRE

    class Meta:
        db_table = 'CLIENTE'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class CONTACTO_CLIENTE(models.Model):
    CC_CLIENTE = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, related_name='contactos', verbose_name='Cliente')
    CC_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del contacto')
    CC_CAPELLIDO = models.CharField(max_length=255, verbose_name='Apellido del contacto')
    CC_CCARGO = models.CharField(max_length=255, verbose_name='Cargo')
    CC_CTELEFONO = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    CC_CEMAIL = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Correo electrónico')
    CC_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    CC_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CC_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contactos_creados', verbose_name='Usuario creador')
    CC_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contactos_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.CC_CNOMBRE} {self.CC_CAPELLIDO} - {self.CC_CLIENTE}"

    class Meta:
        db_table = 'CONTACTO_CLIENTE'
        verbose_name = 'Contacto de Cliente'
        verbose_name_plural = 'Contactos de Clientes'
        unique_together = ('CC_CLIENTE', 'CC_CEMAIL')

class DIRECCION_CLIENTE(models.Model):
    DR_CLIENTE = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, related_name='direcciones', verbose_name='Cliente')
    DR_CDIRECCION = models.TextField(verbose_name='Dirección')
    DR_CREGION = models.ForeignKey('REGION', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Región')
    DR_CPROVINCIA = models.ForeignKey('PROVINCIA', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Provincia')
    DR_CCOMUNA = models.ForeignKey('COMUNA', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Comuna')
    DR_CTIPO = models.CharField(max_length=50, verbose_name='Tipo de dirección', help_text='Ej: Oficina principal, Sucursal, Bodega')
    DR_BACTIVA = models.BooleanField(default=True, verbose_name='Activa')
    DR_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    DR_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    DR_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='direcciones_creadas', verbose_name='Usuario creador')
    DR_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='direcciones_modificadas', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.DR_CTIPO}: {self.DR_CDIRECCION} - {self.DR_CLIENTE}"

    class Meta:
        db_table = 'DIRECCION_CLIENTE'
        verbose_name = 'Dirección de Cliente'
        verbose_name_plural = 'Direcciones de Clientes'
        unique_together = ('DR_CLIENTE', 'DR_CDIRECCION', 'DR_CTIPO')

class PRODUCTO(models.Model):
    PR_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del producto')
    PR_CDESCRIPCION = models.TextField(verbose_name='Descripción')
    PR_BACTIVO = models.BooleanField(default=True, verbose_name='Activo')
    PR_BSERVICIO = models.BooleanField(verbose_name='Tipo de producto', help_text='False para producto físico, True para servicio')
    PR_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    PR_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    PR_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='productos_creados', verbose_name='Usuario creador')
    PR_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='productos_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return self.PR_CNOMBRE

    class Meta:
        db_table = 'PRODUCTO'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class COTIZACION(models.Model):
    CO_CLIENTE = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, related_name='cotizaciones', verbose_name='Cliente')
    CO_CNUMERO = models.CharField(max_length=20, unique=True, verbose_name='Número de cotización')
    CO_FFECHA = models.DateField(verbose_name='Fecha de cotización')
    CO_CVALIDO_HASTA = models.DateField(verbose_name='Válido hasta')
    CO_CESTADO = models.CharField(max_length=20, verbose_name='Estado', choices=[
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ])
    CO_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    CO_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    CO_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CO_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CO_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='cotizaciones_creadas', verbose_name='Usuario creador')
    CO_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='cotizaciones_modificadas', verbose_name='Usuario modificador')
    CO_CCOMENTARIO = models.TextField(blank=True, null=True, verbose_name='Comentarios generales')
    def __str__(self):
        return f"Cotización {self.CO_CNUMERO} - {self.CO_CLIENTE}"

    class Meta:
        db_table = 'COTIZACION'
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'

class COTIZACION_DETALLE(models.Model):
    CD_COTIZACION = models.ForeignKey(COTIZACION, on_delete=models.CASCADE, related_name='detalles', verbose_name='Cotización')
    CD_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='detalles_cotizacion', verbose_name='Producto')
    CD_NCANTIDAD = models.PositiveIntegerField(verbose_name='Cantidad')
    CD_NPRECIO_UNITARIO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Precio unitario')
    CD_NSUBTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Subtotal')
    CD_NDESCUENTO = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Descuento')
    CD_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    CD_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CD_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CD_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_cotizacion_creados', verbose_name='Usuario creador')
    CD_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_cotizacion_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Detalle de Cotización {self.CD_COTIZACION.CO_CNUMERO} - {self.CD_PRODUCTO}"

    class Meta:
        db_table = 'COTIZACION_DETALLE'
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotizaciones'
        unique_together = ('CD_COTIZACION', 'CD_PRODUCTO')

class ORDEN_VENTA(models.Model):
    OV_CCLIENTE = models.ForeignKey(CLIENTE, on_delete=models.CASCADE, related_name='ordenes_venta', verbose_name='Cliente')
    OV_CNUMERO = models.CharField(max_length=20, unique=True, verbose_name='Número de orden de venta')
    OV_FFECHA = models.DateField(verbose_name='Fecha de orden')
    OV_FFECHA_ENTREGA = models.DateField(verbose_name='Fecha de entrega')
    OV_CESTADO = models.CharField(max_length=20, verbose_name='Estado', choices=[
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ])
    OV_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    OV_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    OV_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    OV_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    OV_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='ordenes_venta_creadas', verbose_name='Usuario creador')
    OV_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='ordenes_venta_modificadas', verbose_name='Usuario modificador')
    OV_CCOMENTARIO = models.TextField(blank=True, null=True, verbose_name='Comentarios generales')
    OV_COTIZACION = models.ForeignKey(COTIZACION, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_venta', verbose_name='Cotización')

    def __str__(self):
        return f"Orden de Venta {self.OV_CNUMERO} - {self.OV_CCLIENTE}"

    class Meta:
        db_table = 'ORDEN_VENTA'
        verbose_name = 'Orden de Venta'
        verbose_name_plural = 'Órdenes de Venta'

class ORDEN_VENTA_DETALLE(models.Model):
    OVD_ORDEN_VENTA = models.ForeignKey(ORDEN_VENTA, on_delete=models.CASCADE, related_name='detalles', verbose_name='Orden de Venta')
    OVD_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='detalles_orden_venta', verbose_name='Producto')
    OVD_NCANTIDAD = models.PositiveIntegerField(verbose_name='Cantidad')
    OVD_NPRECIO_UNITARIO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Precio unitario')
    OVD_NSUBTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Subtotal')
    OVD_NDESCUENTO = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Descuento')
    OVD_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    OVD_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    OVD_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    OVD_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_orden_venta_creados', verbose_name='Usuario creador')
    OVD_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_orden_venta_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Detalle de Orden de Venta {self.OVD_ORDEN_VENTA.OV_CNUMERO} - {self.OVD_PRODUCTO}"

    class Meta:
        db_table = 'ORDEN_VENTA_DETALLE'
        verbose_name = 'Detalle de Orden de Venta'
        verbose_name_plural = 'Detalles de Órdenes de Venta'
        unique_together = ('OVD_ORDEN_VENTA', 'OVD_PRODUCTO')

class FACTURA(models.Model):
    FA_CORDEN_VENTA = models.ForeignKey(ORDEN_VENTA, on_delete=models.CASCADE, related_name='facturas', verbose_name='Orden de Venta')
    FA_CNUMERO = models.CharField(max_length=20, unique=True, verbose_name='Número de factura')
    FA_FFECHA = models.DateField(verbose_name='Fecha de factura')
    FA_FFECHA_VENCIMIENTO = models.DateField(verbose_name='Fecha de vencimiento')
    FA_CESTADO = models.CharField(max_length=20, verbose_name='Estado', choices=[
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ])
    FA_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    FA_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    FA_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    FA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    FA_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='facturas_creadas', verbose_name='Usuario creador')
    FA_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='facturas_modificadas', verbose_name='Usuario modificador')
    FA_CESTADO_PAGO = models.CharField(max_length=20, verbose_name='Estado de pago', choices=[
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('COMPLETO', 'Completo'),
    ], default='PENDIENTE')
    FA_NMONTO_PAGADO = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Monto pagado')
    FA_FFECHA_ULTIMO_PAGO = models.DateField(null=True, blank=True, verbose_name='Fecha del último pago')

    def __str__(self):
        return f"Factura {self.FA_CNUMERO} - {self.FA_CORDEN_VENTA.OV_CNUMERO}"

    class Meta:
        db_table = 'FACTURA'
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'

class FACTURA_DETALLE(models.Model):
    FAD_FACTURA = models.ForeignKey(FACTURA, on_delete=models.CASCADE, related_name='detalles', verbose_name='Factura')
    FAD_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='detalles_factura', verbose_name='Producto')
    FAD_NCANTIDAD = models.PositiveIntegerField(verbose_name='Cantidad')
    FAD_NPRECIO_UNITARIO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Precio unitario')
    FAD_NSUBTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Subtotal')
    FAD_NDESCUENTO = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Descuento')
    FAD_NTOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    FAD_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    FAD_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    FAD_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_factura_creados', verbose_name='Usuario creador')
    FAD_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='detalles_factura_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Detalle de Factura {self.FAD_FACTURA.FA_CNUMERO} - {self.FAD_PRODUCTO}"

    class Meta:
        db_table = 'FACTURA_DETALLE'
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Facturas'
        unique_together = ('FAD_FACTURA', 'FAD_PRODUCTO')

class EMPLEADO(models.Model):
    EM_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de empleado')
    EM_CNOMBRE = models.CharField(max_length=100, verbose_name='Nombre')
    EM_CAPELLIDO = models.CharField(max_length=100, verbose_name='Apellido')
    EM_CRUT = models.CharField(max_length=20, unique=True, verbose_name='RUT')
    EM_CFECHA_NACIMIENTO = models.DateField(verbose_name='Fecha de nacimiento')
    EM_CDIRECCION = models.CharField(max_length=200, verbose_name='Dirección')
    EM_CTELEFONO = models.CharField(max_length=20, verbose_name='Teléfono')
    EM_CEMAIL = models.EmailField(unique=True, verbose_name='Correo electrónico')
    EM_FFECHA_CONTRATACION = models.DateField(verbose_name='Fecha de contratación')
    EM_CCARGO = models.CharField(max_length=100, verbose_name='Cargo')
    EM_CDEPARTAMENTO = models.CharField(max_length=100, verbose_name='Departamento')
    EM_CESTADO = models.CharField(max_length=20, choices=[
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('VACACIONES', 'Vacaciones'),
        ('LICENCIA', 'Licencia'),
    ], default='ACTIVO', verbose_name='Estado')
    EM_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    EM_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    EM_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='empleados_creados', verbose_name='Usuario creador')
    EM_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='empleados_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.EM_CNOMBRE} {self.EM_CAPELLIDO} - {self.EM_CCODIGO}"

    class Meta:
        db_table = 'EMPLEADO'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

class EMPLEADO_ADJUNTO(models.Model):
    EA_EMPLEADO = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Empleado')
    EA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del documento')
    EA_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción')
    EA_CARCHIVO = models.FileField(
        upload_to='empleados_adjuntos/',
        verbose_name='Archivo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])
        ]
    )
    EA_CTIPO = models.CharField(
        max_length=20,
        choices=[
            ('CONTRATO', 'Contrato'),
            ('CV', 'Curriculum Vitae'),
            ('CERTIFICADO', 'Certificado'),
            ('EVALUACION', 'Evaluación'),
            ('OTRO', 'Otro'),
        ],
        verbose_name='Tipo de documento'
    )
    EA_FFECHA_SUBIDA = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    EA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    EA_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_empleado_creados', verbose_name='Usuario creador')
    EA_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_empleado_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.EA_CNOMBRE} - {self.EA_CEMPLEADO}"

    class Meta:
        db_table = 'EMPLEADO_ADJUNTO'
        verbose_name = 'Adjunto de Empleado'
        verbose_name_plural = 'Adjuntos de Empleados'
        ordering = ['-EA_FFECHA_SUBIDA']

class CONTRATISTA(models.Model):
    CO_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de contratista')
    CO_CNOMBRE = models.CharField(max_length=100, verbose_name='Nombre')
    CO_CRUT = models.CharField(max_length=20, unique=True, verbose_name='RUT')
    CO_CDIRECCION = models.CharField(max_length=200, verbose_name='Dirección')
    CO_CTELEFONO = models.CharField(max_length=20, verbose_name='Teléfono')
    CO_CEMAIL = models.EmailField(unique=True, verbose_name='Correo electrónico')
    CO_FFECHA_CONTRATACION = models.DateField(verbose_name='Fecha de contratación')
    CO_CESTADO = models.CharField(max_length=20, choices=[
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
    ], default='ACTIVO', verbose_name='Estado')
    CO_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CO_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CO_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contratistas_creados', verbose_name='Usuario creador')
    CO_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contratistas_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.CO_CNOMBRE} - {self.CO_CCODIGO}"

    class Meta:
        db_table = 'CONTRATISTA'
        verbose_name = 'Contratista'
        verbose_name_plural = 'Contratistas'

class CONTRATISTA_ADJUNTO(models.Model):
    CA_CONTRATISTA = models.ForeignKey(CONTRATISTA, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Contratista')
    CA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del documento')
    CA_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción')
    CA_CARCHIVO = models.FileField(
        upload_to='contratistas_adjuntos/',
        verbose_name='Archivo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])
        ]
    )
    CA_CTIPO = models.CharField(
        max_length=20,
        choices=[
            ('CONTRATO', 'Contrato'),
            ('CERTIFICADO', 'Certificado'),
            ('EVALUACION', 'Evaluación'),
            ('OTRO', 'Otro'),
        ],
        verbose_name='Tipo de documento'
    )
    CA_FFECHA_SUBIDA = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    CA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CA_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_contratista_creados', verbose_name='Usuario creador')
    CA_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_contratista_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.CA_CNOMBRE} - {self.CA_CONTRATISTA}"

    class Meta:
        db_table = 'CONTRATISTA_ADJUNTO'
        verbose_name = 'Adjunto de Contratista'
        verbose_name_plural = 'Adjuntos de Contratistas'
        ordering = ['-CA_FFECHA_SUBIDA']

class EMPLEADO_CONTRATISTA(models.Model):
    EC_CONTRATISTA = models.ForeignKey(CONTRATISTA, on_delete=models.CASCADE, related_name='empleados', verbose_name='Contratista')
    EC_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de empleado')
    EC_CNOMBRE = models.CharField(max_length=100, verbose_name='Nombre')
    EC_CAPELLIDO = models.CharField(max_length=100, verbose_name='Apellido')
    EC_CRUT = models.CharField(max_length=20, unique=True, verbose_name='RUT')
    EC_CFECHA_NACIMIENTO = models.DateField(verbose_name='Fecha de nacimiento')
    EC_CDIRECCION = models.CharField(max_length=200, verbose_name='Dirección')
    EC_CTELEFONO = models.CharField(max_length=20, verbose_name='Teléfono')
    EC_CEMAIL = models.EmailField(unique=True, verbose_name='Correo electrónico')
    EC_FFECHA_CONTRATACION = models.DateField(verbose_name='Fecha de contratación')
    EC_CCARGO = models.CharField(max_length=100, verbose_name='Cargo')
    EC_CESTADO = models.CharField(max_length=20, choices=[
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('VACACIONES', 'Vacaciones'),
        ('LICENCIA', 'Licencia'),
    ], default='ACTIVO', verbose_name='Estado')
    EC_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    EC_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    EC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='empleados_contratista_creados', verbose_name='Usuario creador')
    EC_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='empleados_contratista_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.EC_CNOMBRE} {self.EC_CAPELLIDO} - {self.EC_CCODIGO}"

    class Meta:
        db_table = 'EMPLEADO_CONTRATISTA'
        verbose_name = 'Empleado de Contratista'
        verbose_name_plural = 'Empleados de Contratistas'

class EMPLEADO_CONTRATISTA_ADJUNTO(models.Model):
    ECA_EMPLEADO = models.ForeignKey(EMPLEADO_CONTRATISTA, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Empleado de Contratista')
    ECA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del documento')
    ECA_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción')
    ECA_CARCHIVO = models.FileField(
        upload_to='empleados_contratista_adjuntos/',
        verbose_name='Archivo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])
        ]
    )
    ECA_CTIPO = models.CharField(
        max_length=20,
        choices=[
            ('CONTRATO', 'Contrato'),
            ('CV', 'Curriculum Vitae'),
            ('CERTIFICADO', 'Certificado'),
            ('EVALUACION', 'Evaluación'),
            ('OTRO', 'Otro'),
        ],
        verbose_name='Tipo de documento'
    )
    ECA_FFECHA_SUBIDA = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    ECA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    ECA_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_empleado_contratista_creados', verbose_name='Usuario creador')
    ECA_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_empleado_contratista_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.ECA_CNOMBRE} - {self.ECA_EMPLEADO}"

    class Meta:
        db_table = 'EMPLEADO_CONTRATISTA_ADJUNTO'
        verbose_name = 'Adjunto de Empleado de Contratista'
        verbose_name_plural = 'Adjuntos de Empleados de Contratistas'
        ordering = ['-ECA_FFECHA_SUBIDA']

class CONTRATO_CLIENTE(models.Model):
    CC_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de contrato')
    CC_CLIENTE = models.ForeignKey('CLIENTE', on_delete=models.CASCADE, related_name='contratos', verbose_name='Cliente')
    CC_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    CC_FFECHA_FIN = models.DateField(verbose_name='Fecha de fin')
    CC_NESTADO = models.CharField(max_length=20, choices=[
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('PENDIENTE', 'Pendiente'),
        ('TERMINADO', 'Terminado'),
    ], default='ACTIVO', verbose_name='Estado')
    CC_NVALOR_TOTAL = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor total')
    CC_CTERMS_CONDICIONES = models.TextField(verbose_name='Términos y condiciones')
    CC_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    CC_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    CC_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    CC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contratos_creados', verbose_name='Usuario creador')
    CC_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='contratos_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Contrato {self.CC_CCODIGO} - {self.CC_CLIENTE}"

    class Meta:
        db_table = 'CONTRATO_CLIENTE'
        verbose_name = 'Contrato de Cliente'
        verbose_name_plural = 'Contratos de Clientes'

class ANEXO(models.Model):
    AN_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de anexo')
    AN_CONTRATO = models.ForeignKey('CONTRATO_CLIENTE', on_delete=models.CASCADE, related_name='anexos', verbose_name='Contrato')
    AN_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del anexo')
    AN_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción')
    AN_CARCHIVO = models.FileField(
        upload_to='anexos/',
        verbose_name='Archivo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx'])
        ]
    )
    AN_CTIPO = models.CharField(
        max_length=4,
        choices=[
            ('PDF', 'PDF'),
            ('DOCX', 'DOCX'),
            ('XLSX', 'XLSX'),
        ],
        verbose_name='Tipo de archivo'
    )
    AN_FFECHA_SUBIDA = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    AN_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    AN_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='anexos_creados', verbose_name='Usuario creador')
    AN_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='anexos_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Anexo {self.AN_CCODIGO} - {self.AN_CNOMBRE}"

    class Meta:
        db_table = 'ANEXO'
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'

class PROYECTO_CLIENTE(models.Model):
    PC_CCODIGO = models.CharField(max_length=100, unique=True, verbose_name='Código de proyecto')
    PC_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del proyecto')
    PC_CDESCRIPCION = models.TextField(verbose_name='Descripción del proyecto')
    PC_CLIENTE = models.ForeignKey('CLIENTE', on_delete=models.CASCADE, related_name='proyectos', verbose_name='Cliente')
    PC_CCATEGORIA = models.ForeignKey('CATEGORIA_PROYECTO', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Categoría del proyecto')
    PC_CTIPO = models.ForeignKey('TIPO_PROYECTO', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tipo de proyecto')
    PC_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    PC_FFECHA_FIN_ESTIMADA = models.DateField(verbose_name='Fecha de fin estimada')
    PC_FFECHA_FIN_REAL = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    PC_CESTADO = models.CharField(max_length=50, verbose_name='Estado del proyecto')
    PC_NPRESUPUESTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Presupuesto')
    PC_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    PC_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    PC_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    PC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='proyectos_creados', verbose_name='Usuario creador')
    PC_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='proyectos_modificados', verbose_name='Usuario modificador')
    PC_CONTACTO_CLIENTE = models.ForeignKey('CONTACTO_CLIENTE', on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos', verbose_name='Contacto del cliente')
    PC_DIRECCION_CLIENTE = models.ForeignKey('DIRECCION_CLIENTE', on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos', verbose_name='Dirección del cliente')
    PC_NVALOR_HORA = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor por hora')
    PC_NHORAS_ESTIMADAS = models.PositiveIntegerField(verbose_name='Horas estimadas')
    PC_NCOSTO_ESTIMADO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Costo estimado')
    PC_NHORAS_REALES = models.PositiveIntegerField(default=0, verbose_name='Horas reales')
    PC_NCOSTO_REAL = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Costo real')
    PC_NMARGEN = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Margen (%)')

    def __str__(self):
        return f"Proyecto {self.PC_CCODIGO} - {self.PC_CNOMBRE}"

    class Meta:
        db_table = 'PROYECTO_CLIENTE'
        verbose_name = 'Proyecto de Cliente'
        verbose_name_plural = 'Proyectos de Clientes'

class ETAPA(models.Model):
    ET_CCODIGO = models.CharField(max_length=20, unique=True, verbose_name='Código de etapa')
    ET_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la etapa')
    ET_CDESCRIPCION = models.TextField(verbose_name='Descripción de la etapa')
    ET_PROYECTO = models.ForeignKey('PROYECTO_CLIENTE', on_delete=models.CASCADE, related_name='etapas', verbose_name='Proyecto')
    ET_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    ET_FFECHA_FIN_ESTIMADA = models.DateField(verbose_name='Fecha de fin estimada')
    ET_FFECHA_FIN_REAL = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    ET_CESTADO = models.CharField(max_length=50, verbose_name='Estado de la etapa')
    ET_NPRESUPUESTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Presupuesto')
    ET_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    ET_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    ET_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    ET_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='etapas_creadas', verbose_name='Usuario creador')
    ET_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='etapas_modificadas', verbose_name='Usuario modificador')

    def __str__(self):
        return f"Etapa {self.ET_CCODIGO} - {self.ET_CNOMBRE} ({self.ET_PROYECTO.PC_CNOMBRE})"

    class Meta:
        db_table = 'ETAPA'
        verbose_name = 'Etapa de Proyecto'
        verbose_name_plural = 'Etapas de Proyectos'

class TAREA_GENERAL(models.Model):
    TG_CCODIGO = models.CharField(max_length=100, unique=True, verbose_name='Código de tarea general')
    TG_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la tarea general')
    TG_CDESCRIPCION = models.TextField(verbose_name='Descripción de la tarea general')
    TG_ETAPA = models.ForeignKey(ETAPA, on_delete=models.CASCADE, related_name='tareas_generales', verbose_name='Etapa')
    TG_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    TG_FFECHA_FIN_ESTIMADA = models.DateField(verbose_name='Fecha de fin estimada')
    TG_FFECHA_FIN_REAL = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    TG_CESTADO = models.CharField(max_length=50, verbose_name='Estado de la tarea general')
    TG_NPRESUPUESTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Presupuesto')
    TG_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    TG_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    TG_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    TG_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_generales_creadas', verbose_name='Usuario creador')
    TG_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_generales_modificadas', verbose_name='Usuario modificador')
    TG_BMILESTONE = models.BooleanField(default=False, verbose_name='Es un hito')
    TG_NPROGRESO = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Progreso (%)')
    TG_NDURACION_PLANIFICADA = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Duración planificada (horas)')
    TG_NDURACION_REAL = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Duración real (horas)')
    TG_BCRITICA = models.BooleanField(default=False, verbose_name='En la ruta crítica')
    TG_PROYECTO_CLIENTE = models.ForeignKey(PROYECTO_CLIENTE, on_delete=models.CASCADE, null=True, blank=True, related_name='tareas_generales_proyecto', verbose_name='Proyecto de Cliente')
    def __str__(self):
        return f"Tarea General {self.TG_CCODIGO} - {self.TG_CNOMBRE} ({self.TG_ETAPA.ET_CNOMBRE})"

    def get_progreso(self):
        return self.TG_NPROGRESO
    
    def get_horas(self):
        return self.TG_NDURACION_REAL

    class Meta:
        db_table = 'TAREA_GENERAL'
        verbose_name = 'Tarea General'
        verbose_name_plural = 'Tareas Generales'

class TAREA_INGENIERIA(models.Model):
    TI_CCODIGO = models.CharField(max_length=100, unique=True, verbose_name='Código de tarea de ingeniería')
    TI_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la tarea de ingeniería')
    TI_CDESCRIPCION = models.TextField(verbose_name='Descripción de la tarea de ingeniería')
    TI_ETAPA = models.ForeignKey(ETAPA, on_delete=models.CASCADE, related_name='tareas_ingenieria', verbose_name='Etapa')
    TI_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    TI_FFECHA_FIN_ESTIMADA = models.DateField(verbose_name='Fecha de fin estimada')
    TI_FFECHA_FIN_REAL = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    TI_CESTADO = models.CharField(max_length=50, verbose_name='Estado de la tarea de ingeniería')
    TI_NPRESUPUESTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Presupuesto')
    TI_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    TI_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    TI_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    TI_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_ingenieria_creadas', verbose_name='Usuario creador')
    TI_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_ingenieria_modificadas', verbose_name='Usuario modificador')
    TI_BMILESTONE = models.BooleanField(default=False, verbose_name='Es un hito')
    TI_NPROGRESO = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Progreso (%)')
    TI_NDURACION_PLANIFICADA = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Duración planificada (horas)')
    TI_NDURACION_REAL = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Duración real (horas)')
    TG_BCRITICA = models.BooleanField(default=False, verbose_name='En la ruta crítica')
    TI_PROYECTO_CLIENTE = models.ForeignKey(PROYECTO_CLIENTE, on_delete=models.CASCADE, null=True, blank=True, related_name='tareas_ingenieria_proyecto', verbose_name='Proyecto de Cliente')
    def __str__(self):
        return f"Tarea de Ingeniería {self.TI_CCODIGO} - {self.TI_CNOMBRE} ({self.TI_ETAPA.ET_CNOMBRE})"

    def get_progreso(self):
        return self.TI_NPROGRESO
    
    def get_horas(self):
        return self.TI_NDURACION_REAL

    class Meta:
        db_table = 'TAREA_INGENIERIA'
        verbose_name = 'Tarea de Ingeniería'
        verbose_name_plural = 'Tareas de Ingeniería'

class TAREA_FINANCIERA(models.Model):
    TF_CCODIGO = models.CharField(max_length=100, unique=True, verbose_name='Código de tarea financiera')
    TF_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre de la tarea financiera')
    TF_CDESCRIPCION = models.TextField(verbose_name='Descripción de la tarea financiera')
    TF_ETAPA = models.ForeignKey(ETAPA, on_delete=models.CASCADE, related_name='tareas_financieras', verbose_name='Etapa')
    TF_FFECHA_INICIO = models.DateField(verbose_name='Fecha de inicio')
    TF_FFECHA_FIN_ESTIMADA = models.DateField(verbose_name='Fecha de fin estimada')
    TF_FFECHA_FIN_REAL = models.DateField(null=True, blank=True, verbose_name='Fecha de fin real')
    TF_CESTADO = models.CharField(max_length=50, verbose_name='Estado de la tarea financiera')
    TF_NMONTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Monto')
    TF_CTIPO_TRANSACCION = models.CharField(max_length=50, verbose_name='Tipo de transacción')
    TF_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    TF_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    TF_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    TF_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_financieras_creadas', verbose_name='Usuario creador')
    TF_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='tareas_financieras_modificadas', verbose_name='Usuario modificador')
    TF_BMILESTONE = models.BooleanField(default=False, verbose_name='Es un hito')
    TF_NPROGRESO = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Progreso (%)')
    TF_NDURACION_PLANIFICADA = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Duración planificada (horas)')
    TF_NDURACION_REAL = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Duración real (horas)')
    TG_BCRITICA = models.BooleanField(default=False, verbose_name='En la ruta crítica')
    TF_PROYECTO_CLIENTE = models.ForeignKey(PROYECTO_CLIENTE, on_delete=models.CASCADE, null=True, blank=True, related_name='tareas_financieras_proyecto', verbose_name='Proyecto de Cliente')
    def __str__(self):
        return f"Tarea Financiera {self.TF_CCODIGO} - {self.TF_CNOMBRE} ({self.TF_ETAPA.ET_CNOMBRE})"

    def get_progreso(self):
        return self.TF_NPROGRESO
    
    def get_horas(self):
        return self.TF_NDURACION_REAL

    class Meta:
        db_table = 'TAREA_FINANCIERA'
        verbose_name = 'Tarea Financiera'
        verbose_name_plural = 'Tareas Financieras'

class ADJUNTO_TAREA_GENERAL(models.Model):
    AT_TAREA = models.ForeignKey(TAREA_GENERAL, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Tarea General')
    AT_CARCHIVO = models.FileField(upload_to='adjuntos/tareas_generales/', verbose_name='Archivo adjunto')
    AT_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del archivo')
    AT_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción del archivo')
    AT_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    AT_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    AT_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_tareas_generales_creados', verbose_name='Usuario creador')

    def __str__(self):
        return f"Adjunto {self.AT_CNOMBRE} - Tarea General {self.AT_CTAREA.TG_CCODIGO}"

    class Meta:
        db_table = 'ADJUNTO_TAREA_GENERAL'
        verbose_name = 'Adjunto de Tarea General'
        verbose_name_plural = 'Adjuntos de Tareas Generales'

class ADJUNTO_TAREA_INGENIERIA(models.Model):
    ATI_TAREA = models.ForeignKey(TAREA_INGENIERIA, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Tarea de Ingeniería')
    ATI_CARCHIVO = models.FileField(upload_to='adjuntos/tareas_ingenieria/', verbose_name='Archivo adjunto')
    ATI_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del archivo')
    ATI_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción del archivo')
    ATI_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    ATI_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    ATI_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_tareas_ingenieria_creados', verbose_name='Usuario creador')

    def __str__(self):
        return f"Adjunto {self.ATI_CNOMBRE} - Tarea de Ingeniería {self.ATI_CTAREA.TI_CCODIGO}"

    class Meta:
        db_table = 'ADJUNTO_TAREA_INGENIERIA'
        verbose_name = 'Adjunto de Tarea de Ingeniería'
        verbose_name_plural = 'Adjuntos de Tareas de Ingeniería'

class ADJUNTO_TAREA_FINANCIERA(models.Model):
    ATF_TAREA = models.ForeignKey(TAREA_FINANCIERA, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Tarea Financiera')
    ATF_CARCHIVO = models.FileField(upload_to='adjuntos/tareas_financieras/', verbose_name='Archivo adjunto')
    ATF_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del archivo')
    ATF_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción del archivo')
    ATF_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    ATF_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    ATF_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_tareas_financieras_creados', verbose_name='Usuario creador')

    def __str__(self):
        return f"Adjunto {self.ATF_CNOMBRE} - Tarea Financiera {self.ATF_CTAREA.TF_CCODIGO}"

    class Meta:
        db_table = 'ADJUNTO_TAREA_FINANCIERA'
        verbose_name = 'Adjunto de Tarea Financiera'
        verbose_name_plural = 'Adjuntos de Tareas Financieras'

class ADJUNTO_ETAPA(models.Model):
    AE_ETAPA = models.ForeignKey(ETAPA, on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Etapa')
    AE_CARCHIVO = models.FileField(upload_to='adjuntos/etapas/', verbose_name='Archivo adjunto')
    AE_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del archivo')
    AE_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción del archivo')
    AE_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    AE_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    AE_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_etapas_creados', verbose_name='Usuario creador')

    def __str__(self):
        return f"Adjunto {self.AE_CNOMBRE} - Etapa {self.AE_CETAPA.ET_CCODIGO}"

    class Meta:
        db_table = 'ADJUNTO_ETAPA'
        verbose_name = 'Adjunto de Etapa'
        verbose_name_plural = 'Adjuntos de Etapas'

class ASIGNACION_EMPLEADO_TAREA_INGENIERIA(models.Model):
    AE_EMPLEADO = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE, related_name='asignaciones_ingenieria', verbose_name='Empleado')
    AE_TAREA = models.ForeignKey(TAREA_INGENIERIA, on_delete=models.CASCADE, related_name='asignaciones_empleados', verbose_name='Tarea de Ingeniería')
    AE_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AE_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AE_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AE_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_ingenieria_creadas', verbose_name='Usuario creador')
    AE_COSTO_REAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AE_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)
    AE_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)

    def __str__(self):
        return f"Asignación: {self.AE_EMPLEADO} - Tarea: {self.AE_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_TAREA_INGENIERIA'
        verbose_name = 'Asignación de Empleado a Tarea de Ingeniería'
        verbose_name_plural = 'Asignaciones de Empleados a Tareas de Ingeniería'

class ASIGNACION_EMPLEADO_TAREA_FINANCIERA(models.Model):
    AE_EMPLEADO = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE, related_name='asignaciones_financiera', verbose_name='Empleado')
    AE_TAREA = models.ForeignKey(TAREA_FINANCIERA, on_delete=models.CASCADE, related_name='asignaciones_empleados', verbose_name='Tarea Financiera')
    AE_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AE_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AE_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AE_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_financiera_creadas', verbose_name='Usuario creador')
    AE_COSTO_REAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AE_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)
    AE_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)

    def __str__(self):
        return f"Asignación: {self.AE_EMPLEADO} - Tarea: {self.AE_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_TAREA_FINANCIERA'
        verbose_name = 'Asignación de Empleado a Tarea Financiera'
        verbose_name_plural = 'Asignaciones de Empleados a Tareas Financieras'

class ASIGNACION_EMPLEADO_TAREA_GENERAL(models.Model):
    AE_EMPLEADO = models.ForeignKey(EMPLEADO, on_delete=models.CASCADE, related_name='asignaciones_general', verbose_name='Empleado')
    AE_TAREA = models.ForeignKey(TAREA_GENERAL, on_delete=models.CASCADE, related_name='asignaciones_empleados', verbose_name='Tarea General')
    AE_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AE_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AE_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AE_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_general_creadas', verbose_name='Usuario creador')
    AE_COSTO_REAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AE_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)
    AE_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)
    
    def __str__(self):
        return f"Asignación: {self.AE_EMPLEADO} - Tarea: {self.AE_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_TAREA_GENERAL'
        verbose_name = 'Asignación de Empleado a Tarea General'
        verbose_name_plural = 'Asignaciones de Empleados a Tareas Generales'

class ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA(models.Model):
    AEC_EMPLEADO = models.ForeignKey(EMPLEADO_CONTRATISTA, on_delete=models.CASCADE, related_name='asignaciones_ingenieria', verbose_name='Empleado Contratista')
    AEC_TAREA = models.ForeignKey(TAREA_INGENIERIA, on_delete=models.CASCADE, related_name='asignaciones_empleados_contratistas', verbose_name='Tarea de Ingeniería')
    AEC_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AEC_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AEC_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AEC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_contratista_ingenieria_creadas', verbose_name='Usuario creador')
    AEC_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AEC_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)
    AEC_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)

    def __str__(self):
        return f"Asignación: {self.AEC_EMPLEADO} - Tarea: {self.AEC_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_INGENIERIA'
        verbose_name = 'Asignación de Empleado Contratista a Tarea de Ingeniería'
        verbose_name_plural = 'Asignaciones de Empleados Contratistas a Tareas de Ingeniería'

class ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA(models.Model):
    AEC_EMPLEADO = models.ForeignKey(EMPLEADO_CONTRATISTA, on_delete=models.CASCADE, related_name='asignaciones_financiera', verbose_name='Empleado Contratista')
    AEC_TAREA = models.ForeignKey(TAREA_FINANCIERA, on_delete=models.CASCADE, related_name='asignaciones_empleados_contratistas', verbose_name='Tarea Financiera')
    AEC_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AEC_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AEC_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AEC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_contratista_financiera_creadas', verbose_name='Usuario creador')
    AEC_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AEC_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)    
    AEC_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)

    def __str__(self):
        return f"Asignación: {self.AEC_EMPLEADO} - Tarea: {self.AEC_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_FINANCIERA'
        verbose_name = 'Asignación de Empleado Contratista a Tarea Financiera'
        verbose_name_plural = 'Asignaciones de Empleados Contratistas a Tareas Financieras'

class ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL(models.Model):
    AEC_EMPLEADO = models.ForeignKey(EMPLEADO_CONTRATISTA, on_delete=models.CASCADE, related_name='asignaciones_general', verbose_name='Empleado Contratista')
    AEC_TAREA = models.ForeignKey(TAREA_GENERAL, on_delete=models.CASCADE, related_name='asignaciones_empleados_contratistas', verbose_name='Tarea General')
    AEC_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')
    AEC_FFECHA_FINALIZACION = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')
    AEC_CESTADO = models.CharField(max_length=20, choices=[
        ('ASIGNADO', 'Asignado'),
        ('EN_PROGRESO', 'En Progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado')
    ], default='ASIGNADO', verbose_name='Estado')
    AEC_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_contratista_general_creadas', verbose_name='Usuario creador')
    AEC_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    AEC_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)
    AEC_COSTO_TOTAL = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Costo Total', blank=True, null=True)

    def __str__(self):
        return f"Asignación: {self.AEC_EMPLEADO} - Tarea: {self.AEC_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_EMPLEADO_CONTRATISTA_TAREA_GENERAL'
        verbose_name = 'Asignación de Empleado Contratista a Tarea General'
        verbose_name_plural = 'Asignaciones de Empleados Contratistas a Tareas Generales'

class ASIGNACION_RECURSO_TAREA_GENERAL(models.Model):
    ART_TAREA = models.ForeignKey(TAREA_GENERAL, on_delete=models.CASCADE, related_name='recursos_asignados', verbose_name='Tarea General')
    ART_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='asignaciones_tarea_general', verbose_name='Producto')
    ART_CANTIDAD = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')
    ART_COSTO_UNITARIO = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Unitario')
    ART_COSTO_TOTAL = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo Total')
    ART_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Asignación')
    ART_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_recurso_general_creadas', verbose_name='Usuario Creador')
    ART_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    ART_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ART_COSTO_TOTAL = self.ART_CANTIDAD * self.ART_COSTO_UNITARIO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recurso: {self.ART_PRODUCTO} - Tarea: {self.ART_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_RECURSO_TAREA_GENERAL'
        verbose_name = 'Asignación de Recurso a Tarea General'
        verbose_name_plural = 'Asignaciones de Recursos a Tareas Generales'

class ASIGNACION_RECURSO_TAREA_INGENIERIA(models.Model):
    ART_TAREA = models.ForeignKey(TAREA_INGENIERIA, on_delete=models.CASCADE, related_name='recursos_asignados', verbose_name='Tarea de Ingeniería')
    ART_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='asignaciones_tarea_ingenieria', verbose_name='Producto')
    ART_CANTIDAD = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')
    ART_COSTO_UNITARIO = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Unitario')
    ART_COSTO_TOTAL = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo Total')
    ART_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Asignación')
    ART_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_recurso_ingenieria_creadas', verbose_name='Usuario Creador')
    ART_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    ART_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ART_COSTO_TOTAL = self.ART_CANTIDAD * self.ART_COSTO_UNITARIO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recurso: {self.ART_PRODUCTO} - Tarea: {self.ART_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_RECURSO_TAREA_INGENIERIA'
        verbose_name = 'Asignación de Recurso a Tarea de Ingeniería'
        verbose_name_plural = 'Asignaciones de Recursos a Tareas de Ingeniería'

class ASIGNACION_RECURSO_TAREA_FINANCIERA(models.Model):
    ART_TAREA = models.ForeignKey(TAREA_FINANCIERA, on_delete=models.CASCADE, related_name='recursos_asignados', verbose_name='Tarea Financiera')
    ART_PRODUCTO = models.ForeignKey(PRODUCTO, on_delete=models.CASCADE, related_name='asignaciones_tarea_financiera', verbose_name='Producto')
    ART_CANTIDAD = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')
    ART_COSTO_UNITARIO = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Unitario')
    ART_COSTO_TOTAL = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo Total')
    ART_FFECHA_ASIGNACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Asignación')
    ART_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='asignaciones_recurso_financiera_creadas', verbose_name='Usuario Creador')
    ART_COSTO_REAL = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Costo Real', blank=True, null=True)
    ART_HORAS_REALES = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horas Reales', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ART_COSTO_TOTAL = self.ART_CANTIDAD * self.ART_COSTO_UNITARIO
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recurso: {self.ART_PRODUCTO} - Tarea: {self.ART_TAREA}"

    class Meta:
        db_table = 'ASIGNACION_RECURSO_TAREA_FINANCIERA'
        verbose_name = 'Asignación de Recurso a Tarea Financiera'
        verbose_name_plural = 'Asignaciones de Recursos a Tareas Financieras'

class ACTA_REUNION(models.Model):
    AR_ETAPA = models.ForeignKey(ETAPA, on_delete=models.CASCADE, related_name='actas_reunion', verbose_name='Etapa del Proyecto')
    AR_CTITULO = models.CharField(max_length=255, verbose_name='Título del Acta')
    AR_CFECHA = models.DateTimeField(verbose_name='Fecha y Hora de la Reunión')
    AR_CLUGAR = models.CharField(max_length=255, verbose_name='Lugar de la Reunión')
    AR_CPARTICIPANTES = models.TextField(verbose_name='Participantes')
    AR_CAGENDA = models.TextField(verbose_name='Agenda')
    AR_CCONTENIDO = models.TextField(verbose_name='Contenido del Acta')
    AR_CACUERDOS = models.TextField(verbose_name='Acuerdos y Compromisos')
    AR_CARCHIVO = models.FileField(upload_to='actas_reunion/', null=True, blank=True, verbose_name='Archivo Adjunto')
    AR_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    AR_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    AR_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='actas_reunion_creadas', verbose_name='Usuario Creador')
    AR_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='actas_reunion_modificadas', verbose_name='Usuario Modificador')

    def __str__(self):
        return f"{self.AR_CTITULO} - {self.AR_CFECHA}"

    class Meta:
        db_table = 'ACTA_REUNION'
        verbose_name = 'Acta de Reunión'
        verbose_name_plural = 'Actas de Reunión'
        ordering = ['-AR_CFECHA']

class PROYECTO_ADJUNTO(models.Model):
    PA_PROYECTO = models.ForeignKey('PROYECTO_CLIENTE', on_delete=models.CASCADE, related_name='adjuntos', verbose_name='Proyecto')
    PA_CNOMBRE = models.CharField(max_length=255, verbose_name='Nombre del documento')
    PA_CDESCRIPCION = models.TextField(blank=True, null=True, verbose_name='Descripción')
    PA_CARCHIVO = models.FileField(
        upload_to='proyectos_adjuntos/',
        verbose_name='Archivo',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'xlsx', 'jpg', 'png'])
        ]
    )
    PA_CTIPO = models.CharField(max_length=50, verbose_name='Tipo de documento')
    PA_FFECHA_SUBIDA = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')
    PA_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')
    PA_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_proyecto_creados', verbose_name='Usuario creador')
    PA_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='adjuntos_proyecto_modificados', verbose_name='Usuario modificador')

    def __str__(self):
        return f"{self.PA_CNOMBRE} - {self.PA_PROYECTO}"

    class Meta:
        db_table = 'PROYECTO_ADJUNTO'
        verbose_name = 'Adjunto de Proyecto'
        verbose_name_plural = 'Adjuntos de Proyectos'
        ordering = ['-PA_FFECHA_SUBIDA']

class BOLETA_GARANTIA(models.Model):
    BG_PROYECTO = models.ForeignKey('PROYECTO_CLIENTE', on_delete=models.CASCADE, related_name='boletas_garantia', verbose_name='Proyecto')
    BG_CNUMERO = models.CharField(max_length=50, verbose_name='Número de Boleta')
    BG_CMONTO = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Monto')
    BG_CENTIDAD_EMISORA = models.CharField(max_length=255, verbose_name='Entidad Emisora')
    BG_FFECHA_EMISION = models.DateField(verbose_name='Fecha de Emisión')
    BG_FFECHA_VENCIMIENTO = models.DateField(verbose_name='Fecha de Vencimiento')
    BG_CESTADO = models.CharField(max_length=50, choices=[
        ('VIGENTE', 'Vigente'),
        ('VENCIDA', 'Vencida'),
        ('EJECUTADA', 'Ejecutada'),
        ('DEVUELTA', 'Devuelta')
    ], default='VIGENTE', verbose_name='Estado')
    BG_CARCHIVO = models.FileField(upload_to='boletas_garantia/', null=True, blank=True, verbose_name='Archivo Adjunto')
    BG_COBSERVACIONES = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    BG_FFECHA_CREACION = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    BG_FFECHA_MODIFICACION = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')
    BG_CUSUARIO_CREADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='boletas_garantia_creadas', verbose_name='Usuario Creador')
    BG_CUSUARIO_MODIFICADOR = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='boletas_garantia_modificadas', verbose_name='Usuario Modificador')

    def __str__(self):
        return f"Boleta {self.BG_CNUMERO} - {self.BG_PROYECTO}"

    class Meta:
        db_table = 'BOLETA_GARANTIA'
        verbose_name = 'Boleta de Garantía'
        verbose_name_plural = 'Boletas de Garantía'
        ordering = ['-BG_FFECHA_EMISION']

class TAREA_GENERAL_DEPENDENCIA(models.Model):
    TD_TAREA_PREDECESORA = models.ForeignKey('TAREA_GENERAL', on_delete=models.CASCADE, related_name='sucesoras')
    TD_TAREA_SUCESORA = models.ForeignKey('TAREA_GENERAL', on_delete=models.CASCADE, related_name='predecesoras')
    TD_TIPO_DEPENDENCIA = models.CharField(max_length=20, choices=[
        ('FS', 'Finish-to-Start'),
        ('SS', 'Start-to-Start'),
        ('FF', 'Finish-to-Finish'),
        ('SF', 'Start-to-Finish')
    ])

    def __str__(self):
        return f"Tarea {self.TD_TAREA_PREDECESORA} - {self.TD_TAREA_SUCESORA}"

    class Meta:
        db_table = 'TAREA_GENERAL_DEPENDENCIA'
        verbose_name = 'Dependencia de Tarea General'
        verbose_name_plural = 'Dependencias de Tareas Generales'

class TAREA_FINANCIERA_DEPENDENCIA(models.Model):
    TD_TAREA_PREDECESORA = models.ForeignKey('TAREA_FINANCIERA', on_delete=models.CASCADE, related_name='sucesoras')
    TD_TAREA_SUCESORA = models.ForeignKey('TAREA_FINANCIERA', on_delete=models.CASCADE, related_name='predecesoras')
    TD_TIPO_DEPENDENCIA = models.CharField(max_length=20, choices=[
        ('FS', 'Finish-to-Start'),
        ('SS', 'Start-to-Start'),
        ('FF', 'Finish-to-Finish'),
        ('SF', 'Start-to-Finish')
    ])

    def __str__(self):
        return f"Tarea {self.TD_TAREA_PREDECESORA} - {self.TD_TAREA_SUCESORA}"

    class Meta:
        db_table = 'TAREA_FINANCIERA_DEPENDENCIA'
        verbose_name = 'Dependencia de Tarea Financiera'
        verbose_name_plural = 'Dependencias de Tareas Financieras'

class TAREA_INGENIERIA_DEPENDENCIA(models.Model):
    TD_TAREA_PREDECESORA = models.ForeignKey('TAREA_INGENIERIA', on_delete=models.CASCADE, related_name='sucesoras')
    TD_TAREA_SUCESORA = models.ForeignKey('TAREA_INGENIERIA', on_delete=models.CASCADE, related_name='predecesoras')
    TD_TIPO_DEPENDENCIA = models.CharField(max_length=20, choices=[
        ('FS', 'Finish-to-Start'),
        ('SS', 'Start-to-Start'),
        ('FF', 'Finish-to-Finish'),
        ('SF', 'Start-to-Finish')
    ])

    def __str__(self):
        return f"Tarea {self.TD_TAREA_PREDECESORA} - {self.TD_TAREA_SUCESORA}"

    class Meta:
        db_table = 'TAREA_INGENIERIA_DEPENDENCIA'
        verbose_name = 'Dependencia de Tarea de Ingeniería'
        verbose_name_plural = 'Dependencias de Tareas de Ingeniería'


