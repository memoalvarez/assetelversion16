# -*- coding: utf-8 -*-

from odoo import models, api, fields, exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_assigned_id = fields.Many2one('res.partner', string='Contacto asignado')

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)

        if result.opportunity_id.partner_assigned_id:
            result.partner_assigned_id = result.opportunity_id.partner_assigned_id.id

        return result