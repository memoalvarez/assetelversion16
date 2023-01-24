# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contact_id = fields.Many2one('res.partner', string='Contacto')

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)

        for line in result.order_lines:
            line.analytic_account_id = result.id
            if line.service_number:
                line.service_number.sale_subscription_line = line.id
                line.service_number.sale_subscription = result.id
                if line.service_number.stage == 'installed':
                    line.service_number.stage = 'active'

        return result

    def write(self, values):

        for line in self.order_lines:
            if line.service_number:
                line.service_number.sale_subscription_line = False
                line.service_number.sale_subscription = False
                if line.service_number.stage == 'active':    
                    line.service_number.stage = 'installed'

        result = super(SaleOrder, self).write(values)

        for line in self.order_lines:
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