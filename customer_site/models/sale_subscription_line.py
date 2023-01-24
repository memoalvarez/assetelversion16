# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    site = fields.Many2one('res.partner', string='Sitio')