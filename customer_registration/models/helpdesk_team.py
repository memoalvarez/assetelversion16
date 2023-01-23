# -*- coding: utf-8 -*-

from odoo import models, api, fields

class HelpdeskTeam(models.Model):

    _inherit = 'helpdesk.team'

    internal_support = fields.Boolean(string="Soporte interno")
    