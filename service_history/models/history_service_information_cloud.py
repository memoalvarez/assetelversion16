# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistoryServiceInformationCloud(models.Model):
    _name = 'history.service.information.cloud'
    _description = 'Historia de información de servicio cloud'

    service_information_cloud_id = fields.Many2one('history.service.information', string='Informacion de servicio')

    numero = fields.Char(string='Número')
    extension = fields.Char(string='Extensión')