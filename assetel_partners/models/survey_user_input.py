# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    afiliacion_id = fields.Many2one('assetel.partners', string='Afiliacion')
    