# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class InstalledServices(models.Model):
    _inherit = 'installed.services'

    unbuild_task_id = fields.Many2one('project.task', 'Tarea de baja')

    
    def new_unbuild(self):
        action = self.env.ref('service_unbuild.get_project_task_uninstall_view').read()[0]
        action['views'] = [(self.env.ref('service_unbuild.project_task_form_from_installed_services_uninstall').id, 'form')]
        action['context'] = {'default_name': 'BAJA', 'default_project_id': self.company_id.unbuild_project_id.id,
        'default_mrp_production': self.project_task.mrp_production.id, 'default_user_id': self.company_id.unbuild_project_id.user_id.id,
        'default_partner_id': self.partner_id.id, 'default_service_number': self.id, 'default_unbuild_task': True, 'default_active': False,
        'default_requesting_user': self.env.uid}
        action['target'] = 'new'
        return action



    def action_view_task_unbuild(self):
        action = self.env.ref('service_unbuild.get_project_task_uninstall_view').read()[0]

        if self.unbuild_task_id:
            action['views'] = [(self.env.ref('service_unbuild.project_task_form_from_installed_services_uninstall').id, 'form')]
            action['res_id'] = self.unbuild_task_id.id
        return action


