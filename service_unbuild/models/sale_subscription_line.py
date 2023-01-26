# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    to_unbuild = fields.Boolean(string='Baja en proceso', default=False)
    