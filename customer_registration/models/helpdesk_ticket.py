# -*- coding: utf-8 -*-
from odoo import models, api, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    opportunity_id = fields.Many2one('crm.lead', string='Lead/Oportunidad')
    internal_support = fields.Boolean(string="Soporte interno", default=False, related='team_id.internal_support')


    #Redireccion a oportunidad relacionado a ticket
    def action_view_opportunity_id(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "crm.lead",
            "views": [[False, "form"]],
            "res_id": self.opportunity_id.id,
            "context": {"create": False},
        }


    #Enviar encuesta
    def new_survey_invite(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "res_model": "survey.survey",
            "views": [[False, "kanban"]],
            "context": {"ticket_id": self.id},
        }

    def _compute_survey_ids(self):
        #Se cuentan todas las encuestas del ticket actual#
        for reg in self:
            srv_count = reg.env['survey.user_input'].search_count([('ticket_id', '=', reg.id)])
            reg.update({
                'survey_count': srv_count,
            })

    survey_count = fields.Integer(string='Survey count', compute='_compute_survey_ids')
    survey_ids = fields.One2many('survey.user_input', 'ticket_id', string='Encuestas cliente')


    def action_view_surveys(self):
        self.ensure_one()
        surveys = self.mapped('survey_ids')

        if len(surveys) > 1:
            action = self.env.ref('survey.action_survey_user_input').read()[0]
            action['domain'] = [('id', 'in', surveys.ids)]
            action['context'] = dict(create=False)
            return action

        elif surveys:
            return {
                "type": "ir.actions.act_window",
                "res_model": "survey.user_input",
                "views": [[False, "form"]],
                "res_id": surveys.id,
                "context": {"create": False},
            }


