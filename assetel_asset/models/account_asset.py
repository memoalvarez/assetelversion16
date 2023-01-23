# -*- coding: utf-8 -*-
from odoo import models, api, fields

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    mrp_production = fields.Many2one('mrp.production', string='Orden de fabricación')
    description = fields.Char(string='Descripción')
    