# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    def _prepare_invoice_line(self, line, fiscal_position, date_start=False, date_stop=False):
        tax_ids = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.analytic_account_id.company_id)
        if fiscal_position:
            tax_ids = self.env['account.fiscal.position'].browse(fiscal_position).map_tax(tax_ids)
        return {
            'name': line.name,
            'service_number': line.service_number.id,
            'site': line.site.id,
            'subscription_id': line.analytic_account_id.id,
            'price_unit': line.price_unit or 0.0,
            'discount': line.discount,
            'quantity': line.quantity,
            'product_uom_id': line.uom_id.id,
            'product_id': line.product_id.id,
            'tax_ids': [(6, 0, tax_ids.ids)],
            'analytic_account_id': line.analytic_account_id.analytic_account_id.id,
            'subscription_start_date': date_start,
            'subscription_end_date': date_stop,
        }