# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    def new_ticket_customer(self):
        user_id = self.env.user.partner_id.id

        name = 'Solicitud de registro de cliente'
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['views'] = [(self.env.ref('helpdesk.helpdesk_ticket_view_form').id, 'form')]
        action['context'] = {'default_name': name, 'default_team_id': self.company_id.help_desk_team_cec.id,
        'default_partner_id': user_id, 'default_opportunity_id' : self.id}
        action['target'] = 'current'
        return action


    def _compute_tickets_ids(self):
        #Se cuentan todos los dimensionamientos de la oportunidad actual#
        for reg in self:
            tickets_count = reg.env['helpdesk.ticket'].search_count([('opportunity_id', '=', reg.id)])
            reg.update({
                'ticket_count': tickets_count,
            })

    ticket_count = fields.Integer(string='Ticket count', compute='_compute_tickets_ids')
    ticket_customer_ids = fields.One2many('helpdesk.ticket', 'opportunity_id', string='Tickets registro cliente')


    def action_view_ticket_customer(self):
        self.ensure_one()
        tickets = self.mapped('ticket_customer_ids')

        if len(tickets) > 1:
            action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
            action['domain'] = [('id', 'in', tickets.ids)]
            action['context'] = dict(create=False)
            return action

        elif tickets:
            return {
                "type": "ir.actions.act_window",
                "res_model": "helpdesk.ticket",
                "views": [[False, "form"]],
                "res_id": tickets.id,
                "context": {"create": False},
            }
