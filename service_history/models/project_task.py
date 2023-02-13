# -*- coding: utf-8 -*-

from odoo import models, api, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'


    def formalize_demo(self):
        self.active_demo_service.sudo().new_history()
        return super(ProjectTask, self).formalize_demo()


    def modify_service(self):
        self.modification_service_number.sudo().new_history()
        return super(ProjectTask, self).modify_service()

    def new_service_unbuild(self):
        self.service_number.sudo().new_history()
        return super(ProjectTask, self).new_service_unbuild()


    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.unbuild_task:
            result.service_number.sudo().new_history()

        return result