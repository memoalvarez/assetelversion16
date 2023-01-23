# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'


    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.project_id.alias_name:
            #Se guarda estado actual para poder borrarlo y asgnarlo de nuevo (Para el envio de correo)
            actual_stage = result.stage_id
            result.stage_id = False
            result.stage_id = actual_stage.id
                
        return result
   