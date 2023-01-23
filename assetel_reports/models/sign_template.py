# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SignTemplate(models.Model):
    _inherit = 'sign.template'

    responsive = fields.Many2one('stock.picking', string='Responsiva')
    hide_template = fields.Boolean(string='Ocultar plantilla', default=False)

    def action_view_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "views": [[False, "form"]],
            "res_id": self.responsive.id,
            "context": {"create": False},
        }


   
