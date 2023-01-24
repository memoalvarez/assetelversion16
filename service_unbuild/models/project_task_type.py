# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    deactivate_service_stage = fields.Boolean(string='Etapa de baja de servicio', default=False)
    