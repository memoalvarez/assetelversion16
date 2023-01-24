# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    empresarial_group = fields.Many2one('empresarial.group', string='Grupo empresarial')


    @api.onchange('partner_id')
    def _onchange_partner_id_empresarial_group(self):
        if self.partner_id:
            if self.partner_id.parent_id:
                self.empresarial_group = self.partner_id.parent_id.empresarial_group_id
            else:
                self.empresarial_group = self.partner_id.empresarial_group_id

    def _prepare_subscription_data(self, template):
        result = super(SaleOrder, self)._prepare_subscription_data(template)

        if self.partner_invoice_id.parent_id:
            result['empresarial_group'] = self.partner_invoice_id.parent_id.empresarial_group_id.id
        else:
            result['empresarial_group'] = self.partner_invoice_id.empresarial_group_id.id

        return result