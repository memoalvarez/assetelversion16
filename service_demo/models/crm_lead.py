# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions
from datetime import date, datetime

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    demo_stage = fields.Boolean(string='Etapa de demo', default=False, related='stage_id.demo_stage')

    def _compute_demo_ids(self):
        #Se cuentan todos los demos de la oportunidad actual#
        for reg in self:
            demo_count = reg.env['project.task'].search_count([('lead_id', '=', reg.id), ('demo_task', '=', True), '|', ('active', '=', True), ('active', '=', False)])
            reg.update({
                'demo_task_count': demo_count,
            })

    demo_task_count = fields.Integer(string='Demo count', compute='_compute_demo_ids')
    demo_task_ids = fields.One2many('project.task', 'lead_id', string='Demos')

    def new_demo(self):
        if self.partner_id:
            if self.sizing_task_count > 0:
                action = self.env.ref('service_demo.get_project_task_demo_view').read()[0]
                action['views'] = [(self.env.ref('service_demo.project_task_form_demo').id, 'form')]
                action['context'] = {'default_name': 'DEMO', 'default_project_id': self.company_id.demo_project_id.id,
                'default_user_id': self.company_id.demo_project_id.user_id.id, 'default_partner_id': self.partner_id.id,
                'default_lead_id': self.id, 'default_demo_task': True, 'default_demo_application_date': datetime.now(),
                'default_active': False}
                
                action['target'] = 'new'
                return action
            else:
                raise exceptions.ValidationError('Necesitas solicitar un dimensionamiento antes')

        else:
            raise exceptions.ValidationError('Necesitas registrar un cliente')


    def action_view_task_demo(self):
        action = self.env.ref('service_demo.get_project_task_demo_view').read()[0]

        demos = self.env['project.task'].search([('lead_id', '=', self.id), ('demo_task', '=', True), '|', ('active', '=', True), ('active', '=', False)])

        if len(demos) > 1:
            action['domain'] = [('id', 'in', demos.ids),'|', ('active', '=', True), ('active', '=', False)]
            action['views'] = [(self.env.ref('service_demo.project_task_tree_demo').id, 'tree'), (self.env.ref('service_demo.project_task_form_demo').id, 'form')]
        elif demos:
            action['views'] = [(self.env.ref('service_demo.project_task_form_demo').id, 'form')]
            action['res_id'] = demos.id
        return action
        