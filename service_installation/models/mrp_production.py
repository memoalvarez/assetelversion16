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
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]

        if self.project_task:
            action['views'] = [(self.env.ref('project.view_task_form2').id, 'form')]
            action['res_id'] = self.project_task.id
        return action
