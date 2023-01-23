# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    site = fields.Many2one('res.partner', string='Sitio')

    contact_id = fields.Many2one('res.partner', string='Contacto')


    @api.onchange('product_template_id', 'product_uom_qty')
    def _onchange_partner_id_customer_site(self):
        if self.order_id.partner_id.parent_id:
            self.contact_id = self.order_id.partner_id.parent_id
        else:
            self.contact_id = self.order_id.partner_id
