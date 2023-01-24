# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    entregado = fields.Boolean(string='Entregado', default=False)
    approval_request_category_id = fields.Many2many('approval.request.category', string='Categoría')

    def marcar_entregado(self):
        self.entregado = True
