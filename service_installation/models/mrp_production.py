# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    project_task = fields.Many2one('project.task', string='Tarea de proyecto')


    @api.model
    def create(self, vals):
        result = super(MrpProduction, self).create(vals)

        #Se registra en la tarea desde donde e creo la orden de fabricacion el Id actual
        if result.project_task:
            result.project_task.mrp_production = result.id
            
        return result

    def action_view_project_task(self):
        self.ensure_one()
        #action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]
        action = {'type': 'ir.actions.act_window_close'}
        task_projects = self.tasks_ids.mapped('project_task')
        if len(task_projects) == 1:  # redirect to task of the project (with kanban stage, ...)
            action = self.with_context(active_id=task_projects.id).env['ir.actions.actions']._for_xml_id(
                'project.act_project_project_2_project_task_all')
            action['domain'] = [('id', 'in', self.tasks_ids.ids)]

        if self.project_task:
            action['views'] = [(self.env.ref('project.view_task_form2').id, 'form')]
            action['res_id'] = self.project_task.id
        return action
