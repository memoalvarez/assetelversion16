# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pay_online = fields.Boolean(string='Permitir pago en linea', default=False)
    