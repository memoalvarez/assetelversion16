# -*- coding: utf-8 -*-
from odoo import models, api, fields

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    invited_by = fields.Char(string='Invitado por')
    company = fields.Char(string='Empresa')
