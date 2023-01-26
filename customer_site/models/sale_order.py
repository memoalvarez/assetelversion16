# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice_line(self, **optional_values):
        result = super(SaleOrder, self)._prepare_invoice_line(**optional_values)
        result['service_number'] = line.service_number.id
        result['site'] = line.site.id

        return result