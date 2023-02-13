# -*- coding: utf-8 -*-
from odoo import models, api, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    empresarial_group = fields.Many2one('empresarial.group', string='Grupo empresarial')
    