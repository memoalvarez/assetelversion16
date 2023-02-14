# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectProject(models.Model):
    _inherit = 'project.project'

    users_to_notify = fields.Many2many('res.users', string='Usuarios a notificar')
    