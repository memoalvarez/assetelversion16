# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    mrp_stage = fields.Boolean(string='Etapa de fabricación', default=False)
    service_registration_stage = fields.Boolean(string='Etapa de registro de servicio', default=False)
    