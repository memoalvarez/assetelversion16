# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistoryInstalledServices(models.Model):
    _name = 'history.installed.services'
    _description = 'Historial de número de servicio'

    active_installed_service = fields.Many2one('installed.services', string='Servicio Activo')

    service_information_ids = fields.One2many('history.service.information', 'installed_service_id', 'Informacion del servicio')
    modification_date = fields.Datetime("Fecha de guardado")

    name = fields.Char('Numero de servicio')
    service_type = fields.Selection([
        ('sae', 'SAE'),
        ('sae_client', 'SAE de cliente'),
        ('connectivity', 'Conectividad'),
        ('cloud', 'Cloud'),
        ('engineering', 'Ingenieria'),
        ('poliza', 'Póliza')
        ], string='Tipo de servicio')
    product_id = fields.Many2one('product.product', string="Servicio", domain=[('sale_ok', '=', True)])
    description = fields.Text(string='Descripcion')

    empresarial_group = fields.Many2one('empresarial.group', string="Grupo empresarial")
    partner_id = fields.Many2one('res.partner', string="Cliente/Empresa")
    razon_social_id = fields.Many2one('res.partner', string="Razón social")
    site = fields.Many2one('res.partner', string="Sitio")
    sale_subscription = fields.Char('Suscripción')

    demo_installation_date = fields.Datetime("Fecha instalacion demo")
    demo_finish_date = fields.Datetime("Fecha finalización demo")

    quantity = fields.Float(string="Catidad")

    notes = fields.Html(string='Notas')

    lot_ids = fields.One2many('history.service.lot', 'history_service_number', string='Equipos instalados')

    service_price_unit = fields.Float(string='Precio')
    service_vig = fields.Date(string='Vigencia de servicio')

    encargado_comercial = fields.Many2one('res.users', string="Encargado comercial")


    def open_service_configuration(self):
        action = self.env.ref('service_history.get_history_service_information_view').read()[0]

        information = self.mapped('service_information_ids')

        if len(information) > 1:
            action['domain'] = [('id', 'in', information.ids)]
        elif information:
            action['views'] = [(self.env.ref('service_history.history_service_information_form').id, 'form')]
            action['res_id'] = information.id
            action['target'] = 'new'
        return action

