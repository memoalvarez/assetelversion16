# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SignTemplate(models.Model):
    _inherit = 'sign.template'

    project_task = fields.Many2one('project.task', string='Tarea de proyecto')
    hide_template = fields.Boolean(string='Ocultar plantilla', default=False)

    def action_view_project_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "views": [[False, "form"]],
            "res_id": self.project_task.id,
            "context": {"create": False},
        }


   
