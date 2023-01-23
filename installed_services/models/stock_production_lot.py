# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    service_number = fields.Many2one('installed.services', string='Numero de servicio')
