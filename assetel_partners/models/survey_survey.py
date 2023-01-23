# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'


    def action_send_survey(self):
        res = super(SurveySurvey, self).action_send_survey()

        contexto = res.get('context')
        contexto['default_afiliacion_id'] = self.env.context.get('afiliacion_id')
        contexto['default_partner_ids'] = self.env.context.get('contact_id')
        res['context'] = contexto

        return res
