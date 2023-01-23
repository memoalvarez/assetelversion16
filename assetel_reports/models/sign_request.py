# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SignRequest(models.Model):
    _inherit = 'sign.request'

    responsive = fields.Many2one('stock.picking', string='Responsiva')

    @api.model
    def create(self, vals):
        result = super(SignRequest, self).create(vals)

        if result.template_id.responsive:
            result.responsive = result.template_id.responsive.id
            result.responsive.sign_request = result.id
        return result


    def action_view_task(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "views": [[False, "form"]],
            "res_id": self.responsive.id,
            "context": {"create": False},
        }

