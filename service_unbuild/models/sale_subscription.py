# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'


    @api.depends('recurring_invoice_line_ids')
    def _check_unbuild(self):
        for subs in self:
            active_unbuild = False
            for line in subs.recurring_invoice_line_ids:
                if line.to_unbuild:
                    active_unbuild = True

            subs.update({
                'to_unbuild' : active_unbuild
            })


    to_unbuild = fields.Boolean(string='Suscripcion con baja', default=False, compute='_check_unbuild')
    