# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sizing_stage = fields.Boolean(string='Etapa de dimensionamiento', default=False, related='stage_id.sizing_stage')

    def _compute_sizing_ids(self):
        #Se cuentan todos los dimensionamientos de la oportunidad actual#
        for reg in self:
            sizing_count = reg.env['project.task'].search_count([('lead_id', '=', reg.id), ('sizing_task', '=', True)])
            reg.update({
                'sizing_task_count': sizing_count,
            })

    sizing_task_count = fields.Integer(string='Sizing count', compute='_compute_sizing_ids')
    sizing_task_ids = fields.One2many('project.task', 'lead_id', string='Dimensionamientos')


    def new_sizing(self):
        if self.partner_id:

            action = self.env.ref('service_sizing.get_project_task_sizing_view').read()[0]
            action['views'] = [(self.env.ref('service_sizing.project_task_form_from_crm').id, 'form')]
            action['context'] = {'default_name': 'DIMENSIONAMIENTO', 'default_project_id': self.company_id.sizing_project_id.id,
            'default_user_id': self.company_id.sizing_project_id.user_id.id, 'default_partner_id': self.partner_id.id,
            'default_lead_id': self.id, 'default_sizing_task': True}
            action['target'] = 'new'
            return action

        else:
            raise exceptions.ValidationError('Necesitas registrar un cliente')


    def action_view_task_sizing(self):
        action = self.env.ref('service_sizing.get_project_task_sizing_view').read()[0]

        dimensionamientos = self.mapped('sizing_task_ids')

        if len(dimensionamientos) > 1:
            action['domain'] = [('id', 'in', dimensionamientos.ids), ('sizing_task', '=', True)]
            action['views'] = [(self.env.ref('service_sizing.project_task_tree_from_crm').id, 'tree'), (self.env.ref('service_sizing.project_task_form_from_crm').id, 'form')]
        elif dimensionamientos:
            action['views'] = [(self.env.ref('service_sizing.project_task_form_from_crm').id, 'form')]
            action['res_id'] = dimensionamientos.id
        return action
