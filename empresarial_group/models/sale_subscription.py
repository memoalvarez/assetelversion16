# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    empresarial_group = fields.Many2one('empresarial.group', string='Grupo empresarial')

