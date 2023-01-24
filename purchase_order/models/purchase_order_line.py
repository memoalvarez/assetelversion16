# -*- coding: utf-8 -*-
from odoo import models, api, fields

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float(string='Desc.%')

    def _prepare_compute_all_values(self):
        # Hook method to returns the different argument values for the
        # compute_all method, due to the fact that discounts mechanism
        # is not implemented yet on the purchase orders.
        # This method should disappear as soon as this feature is
        # also introduced like in the sales module.
        self.ensure_one()
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        return {
            'price_unit': price,
            'currency_id': self.order_id.currency_id,
            'product_qty': self.product_qty,
            'product': self.product_id,
            'partner': self.order_id.partner_id,
        }


