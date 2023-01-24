# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ApprovalRequestCategory(models.Model):
    _name = 'approval.request.category'
    _description = 'Categorias de solicitudes de aprobación'

    name = fields.Char("Nombre ")
    active = fields.Boolean(string="Activo", default=True)
    approval_category_id = fields.Many2one('approval.category', string="Tipo de aprobación")
    