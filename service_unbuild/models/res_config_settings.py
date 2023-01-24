# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    unbuild_project_id = fields.Many2one(related='company_id.unbuild_project_id', readonly=False, string='Proyecto de baja')
