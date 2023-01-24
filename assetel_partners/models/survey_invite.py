# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SurveyInvite(models.TransientModel):
    _inherit = 'survey.invite'

    afiliacion_id = fields.Many2one('assetel.partners', string='Afiliación')


    def _get_answers_values(self):
        res = super(SurveyInvite, self)._get_answers_values()
        res['afiliacion_id'] = self.afiliacion_id.id

        return res