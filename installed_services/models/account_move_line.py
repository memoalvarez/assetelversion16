# -*- coding: utf-8 -*-
from odoo import models, api, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    service_number = fields.Many2one('installed.services', string='N° de servicio')

