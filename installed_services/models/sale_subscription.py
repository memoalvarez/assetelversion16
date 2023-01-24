# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    contact_id = fields.Many2one('res.partner', string='Contacto')

    @api.model
    def create(self, vals):
        result = super(SaleSubscription, self).create(vals)

        for line in result.recurring_invoice_line_ids:
            if line.service_number:
                line.service_number.sale_subscription_line = line.id
                line.service_number.sale_subscription = result.id
                if line.service_number.stage == 'installed':
                    line.service_number.stage = 'active'

        return result

    def write(self, values):

        for line in self.recurring_invoice_line_ids:
            if line.service_number:
                line.service_number.sale_subscription_line = False
                line.service_number.sale_subscription = False
                if line.service_number.stage == 'active':    
                    line.service_number.stage = 'installed'

        result = super(SaleSubscription, self).write(values)

        for line in self.recurring_invoice_line_ids:
            if line.service_number:
                line.service_number.sale_subscription_line = line.id
                line.service_number.sale_subscription = self.id
                if line.service_number.stage == 'installed':
                    line.service_number.stage = 'active'

        return result

    @api.onchange('partner_id')
    def _onchange_partner_id_installed_services(self):
        if self.partner_id.parent_id:
            self.contact_id = self.partner_id.parent_id
        else:
            self.contact_id = self.partner_id


    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        self.empresarial_group = self.contact_id.empresarial_group_id.id