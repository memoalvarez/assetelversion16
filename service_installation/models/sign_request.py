# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SignRequest(models.Model):
    _inherit = 'sign.request'

    project_task = fields.Many2one('project.task', string='Tarea de proyecto')

    @api.model
    def create(self, vals):
        result = super(SignRequest, self).create(vals)

        if result.template_id.project_task:
            result.project_task = result.template_id.project_task.id
            result.project_task.sign_request = result.id
        return result


    def action_view_task_service_installation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "views": [[False, "form"]],
            "res_id": self.project_task.id,
            "context": {"create": False},
        }

