# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    to_unbuild = fields.Boolean(string='Baja en proceso', default=False)
    