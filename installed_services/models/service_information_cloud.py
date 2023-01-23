# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ServiceInformationCloud(models.Model):
    _name = 'service.information.cloud'
    _description = 'Información de servicio cloud'

    service_information_cloud_id = fields.Many2one('service.information', string='Informacion de servicio')

    numero = fields.Char(string='Número')
    extension = fields.Char(string='Extensión')