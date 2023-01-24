# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    help_desk_team_cec = fields.Many2one('helpdesk.team', string='Mesa de ayuda CEC')
