# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    site = fields.Many2one('res.partner', string='Sitio')