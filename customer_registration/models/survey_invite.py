# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SurveyInvite(models.TransientModel):
    _inherit = 'survey.invite'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Ticket')


    def _get_answers_values(self):
        res = super(SurveyInvite, self)._get_answers_values()
        res['ticket_id'] = self.ticket_id.id

        return res