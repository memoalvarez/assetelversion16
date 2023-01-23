# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    help_desk_team_cec = fields.Many2one(
        related='company_id.help_desk_team_cec', readonly=False,
        string='Mesa de ayuda CEC')
