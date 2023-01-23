# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class AccountMove(models.Model):
    _inherit = 'account.move'

    pay_online = fields.Boolean(string='Pago en linea', default=False)

    @api.model
    def create(self, vals):
        result = super(AccountMove, self).create(vals)

        if result.partner_id.pay_online:
            result.pay_online = result.partner_id.pay_online

        return result
        