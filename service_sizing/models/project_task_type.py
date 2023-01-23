# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    end_sizing = fields.Boolean(string='Etapa de dimensionamiento terminado', default=False)