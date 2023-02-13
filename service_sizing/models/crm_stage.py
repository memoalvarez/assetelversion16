# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    sizing_stage = fields.Boolean(string='Etapa de dimensionamiento', default=False)
