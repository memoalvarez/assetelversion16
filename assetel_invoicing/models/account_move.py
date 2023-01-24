# -*- coding: utf-8 -*-
from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'



    @api.model
    def create(self, vals):
        result = super(AccountMove, self).create(vals)

        if result.partner_id.l10n_mx_edi_payment_method_id:
            result.l10n_mx_edi_payment_method_id = result.partner_id.l10n_mx_edi_payment_method_id.id

        if result.partner_id.l10n_mx_edi_usage:
            result.l10n_mx_edi_usage = result.partner_id.l10n_mx_edi_usage

        if result.partner_shipping_id:
            result.partner_shipping_id = False

        return result


    def action_post(self):
        result = super(AccountMove, self).action_post()
        self.invoice_payment_ref = self.partner_id.ref

        return result
