# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    demo_project_id = fields.Many2one('project.project', string='Proyecto de demo')
