# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    @api.depends('recurring_invoice_line_ids')
    def _check_modification(self):
        for subs in self:
            active_modification = False
            for line in subs.recurring_invoice_line_ids:
                if line.to_modify:
                    active_modification = True

            subs.update({
                'to_modify' : active_modification
            })

    to_modify = fields.Boolean(string='Suscripcion con modificacion', default=False, compute='_check_modification')

