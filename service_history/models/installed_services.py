# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import date, datetime


class InstalledServices(models.Model):
    _inherit = 'installed.services'


    def _compute_history_ids(self):
        #Se cuentan todos los registros de historia#
        for reg in self:
            hist_count = reg.env['history.installed.services'].search_count([['active_installed_service', '=', reg.id]])
            reg.update({
                'history_count': hist_count,
            })

    history_count = fields.Integer(string='Modification sale order', compute='_compute_history_ids')
    history_ids = fields.One2many('history.installed.services', 'active_installed_service', 'Registros de historial')


    def action_view_history(self):
        action = self.env.ref('service_history.get_history_installed_services_view').read()[0]

        history_regs = self.mapped('history_ids')

        if len(history_regs) > 1:
            action['domain'] = [('id', 'in', history_regs.ids)]
        elif history_regs:
            action['views'] = [(self.env.ref('service_history.history_installed_services_form').id, 'form')]
            action['res_id'] = history_regs.id
        return action


    def new_history(self):
        for reg in self:
            values = {
                'active_installed_service' : reg.id,
                'modification_date' : datetime.now(),
                'name' : reg.name,
                'service_type' : reg.service_type,
                'product_id' : reg.product_id.id,
                'description' : reg.description,
                'empresarial_group' : reg.empresarial_group.id,
                'partner_id' : reg.partner_id.id,
                'razon_social_id' : reg.razon_social_id.id,
                'encargado_comercial' : reg.encargado_comercial.id,
                'site' : reg.site.id,
                'sale_subscription' : reg.sale_subscription.display_name,
                'demo_installation_date' : reg.demo_installation_date,
                'demo_finish_date' : reg.demo_finish_date,
                'service_price_unit' : reg.service_price_unit,
                'service_vig' : reg.service_vig,
                'notes' : reg.notes,
            }
            principal = self.env['history.installed.services'].create(values)

            #Por cada linea en lotes#
            for line in reg.lot_ids:
                values_lot = {
                    'history_service_number' : principal.id,
                    'name' : line.name,
                    'product_id' : line.product_id.id,
                }
                lotes = self.env['history.service.lot'].create(values_lot)

            #Por cada linea en service information#
            for line in reg.service_information_ids:
                values_info = {
                    'installed_service_id' : principal.id,
                    'service_type' : line.service_type,
                    'notes_info' : line.notes_info,
                    'sae_type' : line.sae_type,
                    'sae_portal' : line.sae_portal,
                    'sae_usuario' : line.sae_usuario,
                    'sae_contrasena' : line.sae_contrasena,
                    'sae_equipo' : line.sae_equipo,
                    'sae_serie' : line.sae_serie,
                    'sae_licencia' : line.sae_licencia,
                    'sae_direccion_ip' : line.sae_direccion_ip,
                    'sae_mascara' : line.sae_mascara,
                    'conectividad_type' : line.conectividad_type,
                    'conectividad_portal' : line.conectividad_portal,
                    'conectividad_usuario' : line.conectividad_usuario,
                    'conectividad_contrasena' : line.conectividad_contrasena,
                    'conectividad_direccion_ip' : line.conectividad_direccion_ip,
                    'conectividad_mascara' : line.conectividad_mascara,
                    'conectividad_puerta_de_enlace' : line.conectividad_puerta_de_enlace,
                    'conectividad_dns_1' : line.conectividad_dns_1,
                    'conectividad_dns_2' : line.conectividad_dns_2,
                    'conectividad_pop' : line.conectividad_pop.id,
                    'conectividad_punto_a' : line.conectividad_punto_a,
                    'conectividad_punto_b' : line.conectividad_punto_b,
                    'conectividad_direccion_ip_a' : line.conectividad_direccion_ip_a,
                    'conectividad_direccion_ip_b' : line.conectividad_direccion_ip_b,
                    'conectividad_bw_down' : line.conectividad_bw_down,
                    'conectividad_bw_up' : line.conectividad_bw_up,
                    'conectividad_admin_router' : line.conectividad_admin_router,
                    'ingenieria_nombre_proyecto' : line.ingenieria_nombre_proyecto,
                    'ingenieria_inicio' : line.ingenieria_inicio,
                    'ingenieria_fin' : line.ingenieria_fin,
                    'cloud_type' : line.cloud_type,
                    'cloud_direccion_ip' : line.cloud_direccion_ip,
                    'cloud_direccion_ip_externa' : line.cloud_direccion_ip_externa,
                    'cloud_sistema_operativo' : line.cloud_sistema_operativo,
                    'cloud_hostname' : line.cloud_hostname,
                    'cloud_software' : line.cloud_software,
                    'cloud_vcore' : line.cloud_vcore,
                    'cloud_ram' : line.cloud_ram,
                    'cloud_hd' : line.cloud_hd,
                    'cloud_vpn_p2p' : line.cloud_vpn_p2p,
                    'cloud_usuario_vpn_ssl' : line.cloud_usuario_vpn_ssl,
                    'cloud_contrasena_vpn_ssl' : line.cloud_contrasena_vpn_ssl,
                    'cloud_usuario_so' : line.cloud_usuario_so,
                    'cloud_contrasena_so' : line.cloud_contrasena_so,
                    'cloud_ur' : line.cloud_ur,
                    'cloud_ubicacion_rack_dc' : line.cloud_ubicacion_rack_dc,
                    'cloud_ancho_de_banda' : line.cloud_ancho_de_banda,
                    'cloud_firewall' : line.cloud_firewall,
                    'cloud_cuentas' : line.cloud_cuentas,
                    'cloud_capacidad' : line.cloud_capacidad,
                    'cloud_dominio' : line.cloud_dominio,
                    'cloud_portal_filtrado' : line.cloud_portal_filtrado,
                    'cloud_portal_filtrado_usuario' : line.cloud_portal_filtrado_usuario,
                    'cloud_portal_filtrado_contrasena' : line.cloud_portal_filtrado_contrasena,
                    'cloud_vpn' : line.cloud_vpn,
                    'cloud_vpn_usuario' : line.cloud_vpn_usuario,
                    'cloud_vpn_contrasena' : line.cloud_vpn_contrasena,
                    'cloud_zimbra_cpanel' : line.cloud_zimbra_cpanel,
                    'cloud_almacenamiento' : line.cloud_almacenamiento,
                    'cloud_tecnologia' : line.cloud_tecnologia,
                    'cloud_cliente' : line.cloud_cliente,
                    'cloud_res' : line.cloud_res,
                    'cloud_admin' : line.cloud_admin,
                    'cloud_canales' : line.cloud_canales,
                    'cloud_paquetes_llamadas' : line.cloud_paquetes_llamadas,
                    'cloud_did' : line.cloud_did,
                    'cloud_cantidad' : line.cloud_cantidad,
                    'cloud_consumo' : line.cloud_consumo,
                    'cloud_estado' : line.cloud_estado,
                    'cloud_modelo' : line.cloud_modelo,
                    'cloud_mascara' : line.cloud_mascara,
                    'cloud_puerta_de_enlace' : line.cloud_puerta_de_enlace,
                    'cloud_e1' : line.cloud_e1,
                    'cloud_fxo_fxs' : line.cloud_fxo_fxs,
                    'cloud_sip' : line.cloud_sip,
                    'cloud_licencia' : line.cloud_licencia,
                    'cloud_tipo' : line.cloud_tipo,
                    'cloud_vigencia' : line.cloud_vigencia,
                    'poliza_type' : line.poliza_type,
                    'poliza_condiciones' : line.poliza_condiciones,
                    'poliza_soporte_dxh' : line.poliza_soporte_dxh,
                    'poliza_contratados' : line.poliza_contratados,
                    'poliza_utilizados' : line.poliza_utilizados,
                    'poliza_restantes' : line.poliza_restantes,
                    'poliza_sitio' : line.poliza_sitio.id,
                    'poliza_equipo' : line.poliza_equipo,
                    'poliza_serie' : line.poliza_serie,
                    'poliza_licencia' : line.poliza_licencia,
                }
                informacion = self.env['history.service.information'].create(values_info)

                for tel in line.cloud_numeros_extensiones:
                    values_tel = {
                        'service_information_cloud_id' : informacion.id,
                        'numero' : tel.numero,
                        'extension' : tel.extension,
                    }
                    numeros = self.env['history.service.information.cloud'].create(values_tel)
        return True

