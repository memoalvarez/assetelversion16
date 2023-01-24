# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class StockLot(models.Model):
    _inherit = 'stock.lot'

    service_number = fields.Many2one('installed.services', string='Numero de servicio')
