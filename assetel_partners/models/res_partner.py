# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class ResPartner(models.Model):
    _inherit = 'res.partner'

    number_afiliation = fields.Many2one('assetel.partners', string='Numero de Afiliación')
                