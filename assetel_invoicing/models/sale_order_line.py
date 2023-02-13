# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    def _prepare_invoice_line(self, **optional_values):
        result = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)

        result['service_number'] = self.service_number.id
        result['site'] = self.site.id

        return result