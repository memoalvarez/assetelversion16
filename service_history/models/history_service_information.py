# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistoryServiceInformation(models.Model):
    _name = 'history.service.information'
    _description = 'Historial de información de servicio'

    installed_service_id = fields.Many2one('history.installed.services', string='Servicio')

    #CAMPOS TODAS LAS VISTAS#

    service_type = fields.Selection([
        ('sae', 'SAE'),
        ('sae_client', 'SAE de cliente'),
        ('connectivity', 'Conectividad'),
        ('cloud', 'Cloud'),
        ('engineering', 'Ingenieria'),
        ('poliza', 'Póliza')
        ], string='Tipo de servicio')

    notes_info = fields.Html(string='Notas')

    #CAMPOS SAE#

    sae_type = fields.Selection([
        ('firewall', 'SAE FIREWALL'),
        ('switch', 'SAE SWITCH'),
        ('ap', 'SAE AP'),
        ('licencia', 'SAE Licencia'),
        ], string='Tipo')

    sae_portal = fields.Char(string='Portal')
    sae_usuario = fields.Char(string='Usuario')
    sae_contrasena = fields.Char(string='Contraseña')
    sae_equipo = fields.Char(string='Equipo')
    sae_serie = fields.Char(string='Serie')
    sae_licencia = fields.Char(string='Licencia')
    sae_numero_licencias = fields.Char(string='Numero de licencias')
    sae_direccion_ip = fields.Char(string='Direccion IP')
    sae_mascara = fields.Char(string='Mascara')
    sae_host = fields.Char(string='Num. de hosts sensors')


    #CAMPOS CONECTIVIDAD#

    conectividad_type = fields.Selection([
        ('dedicado', 'DEDICADO'),
        ('pro', 'PRO'),
        ('plus', 'PLUS'),
        ('startup', 'STARTUP'),
        ('metropolitano', 'METROPOLITANO'),
        ('cnv', 'CNV'),
        ('paq1', 'PAQ. IPV4'),
        ('paq2', 'CNV PAQ. IPV4'),
        ], string='Tipo')

    conectividad_portal = fields.Char(string='Portal')
    conectividad_usuario = fields.Char(string='Usuario')
    conectividad_contrasena = fields.Char(string='Contraseña')
    conectividad_direccion_ip = fields.Char(string='Direccion IP')
    conectividad_mascara = fields.Char(string='Mascara')
    conectividad_puerta_de_enlace = fields.Char(string='Puerta de enlace')
    conectividad_dns_1 = fields.Char(string='DNS 1')
    conectividad_dns_2 = fields.Char(string='DNS 2')
    conectividad_pop = fields.Many2one('res.partner', string='POP')
    conectividad_punto_a = fields.Char(string='Punto A')
    conectividad_punto_b = fields.Char(string='Punto B')
    conectividad_direccion_ip_a = fields.Char(string='Direccion IP A')
    conectividad_direccion_ip_b = fields.Char(string='Direccion IP B')
    conectividad_bw_down = fields.Char(string='BW down')
    conectividad_bw_up = fields.Char(string='BW up')
    conectividad_admin_router = fields.Selection([
        ('cliente', 'CLIENTE'),
        ('assetel', 'ASSETEL'),
        ], string='Administración router')


    #CAMPOS INGENIERIA#

    ingenieria_nombre_proyecto = fields.Char(string='Nombre de proyecto')
    ingenieria_inicio = fields.Datetime("Fecha de inicio")
    ingenieria_fin = fields.Datetime("Fecha de fin")


    #CAMPOS CLOUD#

    cloud_type = fields.Selection([
        ('maquina_virtual', 'MAQUINA VIRTUAL'),
        ('coubicacion', 'COUBICACIÓN'),
        ('correo_electronico', 'CORREO ELECTRÓNICO'),
        ('backup', 'BACKUP'),
        ('hosting', 'HOSTING'),
        ('telefonia', 'TELEFONIA'),
        ('sae', 'SAE'),
        ('licencias', 'LICENCIAS'),
        ('dominio', 'DOMINIO'),
        ], string='Tipo')

    cloud_direccion_ip = fields.Char(string='Direccion IP')
    cloud_direccion_ip_externa = fields.Char(string='Direccion IP externa')
    cloud_sistema_operativo = fields.Char(string='Sistema Operativo')
    cloud_hostname = fields.Char(string='Hostname')
    cloud_software = fields.Char(string='Software')
    cloud_vcore = fields.Char(string='vCORE')
    cloud_ram = fields.Char(string='RAM')
    cloud_hd = fields.Char(string='HD')
    cloud_vpn_p2p = fields.Char(string='VPN p2p')
    cloud_usuario_vpn_ssl = fields.Char(string='Usuario VPN/SSL')
    cloud_contrasena_vpn_ssl = fields.Char(string='Contraseña VPN/SSL')
    cloud_usuario_so = fields.Char(string='Usuario SO')
    cloud_contrasena_so = fields.Char(string='Contraseña SO')
    cloud_ur = fields.Char(string='UR')
    cloud_ubicacion_rack_dc = fields.Char(string='Ubicación Rack DC')
    cloud_ancho_de_banda = fields.Char(string='Ancho de Banda')
    cloud_firewall = fields.Char(string='Firewall')
    cloud_cuentas = fields.Char(string='Cuentas')
    cloud_capacidad = fields.Char(string='Capacidad')
    cloud_dominio = fields.Char(string='Dominio')
    cloud_portal_filtrado = fields.Char(string='Portal filtrado')
    cloud_portal_filtrado_usuario = fields.Char(string='Usuario')
    cloud_portal_filtrado_contrasena = fields.Char(string='Contraseña')
    cloud_vpn = fields.Char(string='VPN')
    cloud_vpn_usuario = fields.Char(string='Usuario')
    cloud_vpn_contrasena = fields.Char(string='Contraseña')
    cloud_zimbra_cpanel = fields.Char(string='Zimbra/cPanel')
    cloud_almacenamiento = fields.Char(string='Almacenamiento')
    cloud_tecnologia = fields.Selection([
        ('syn', 'Syn'),
        ('connectivity', 'Veeam'),
        ], string='Tecnologia')
    cloud_cliente = fields.Selection([
        ('mv', 'MV'),
        ('sv', 'SV'),
        ], string='Cliente')
    cloud_res = fields.Char(string='Res')
    cloud_admin = fields.Char(string='Admin')
    cloud_numeros_extensiones = fields.One2many('history.service.information.cloud', 'service_information_cloud_id', string='Numeros')
    cloud_canales = fields.Char(string='Canales')
    cloud_paquetes_llamadas = fields.Char(string='Paquete de llamadas')
    cloud_did = fields.Char(string='DID')
    cloud_cantidad = fields.Char(string='Cantidad')
    cloud_consumo = fields.Char(string='Consumo')
    cloud_estado = fields.Selection([
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ], string='Estado')
    cloud_modelo = fields.Char(string='Modelo')
    cloud_mascara = fields.Char(string='Mascara')
    cloud_puerta_de_enlace = fields.Char(string='Puerta de enlace')
    cloud_e1 = fields.Char(string='E1')
    cloud_fxo_fxs = fields.Char(string='FXO/FXS')
    cloud_sip = fields.Char(string='SIP')
    cloud_licencia = fields.Char(string='Licencia')
    cloud_tipo = fields.Char(string='Tipo')
    cloud_vigencia = fields.Datetime("Vigencia")



    #CAMPOS POLIZA#

    poliza_type = fields.Selection([
        ('conectividad', 'CONECTIVIDAD'),
        ('sae', 'SAE'),
        ('cloud', 'CLOUD'),
        ], string='Tipo')

    poliza_condiciones = fields.Char(string='Condiciones')
    poliza_soporte_dxh = fields.Char(string='Soporte DxH')
    poliza_contratados = fields.Char(string='Contratado')
    poliza_utilizados = fields.Char(string='Utilizado')
    poliza_restantes = fields.Char(string='Restante')
    poliza_sitio = fields.Many2one('res.partner', string='Sitio')
    poliza_equipo = fields.Char(string='Equipo')
    poliza_serie = fields.Char(string='Serie')
    poliza_licencia = fields.Char(string='Licencia')

