# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    service_number = fields.Many2one('installed.services', string='N° de servicio')
    
    empresarial_group = fields.Many2one('empresarial.group', string='Grupo empresarial')


    @api.onchange('product_template_id', 'product_uom_qty')
    def _onchange_partner_id_service_installation(self):
        if self.order_id.empresarial_group:
            self.empresarial_group = self.order_id.empresarial_group
