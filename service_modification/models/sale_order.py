# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for so in self:
            for line in so.order_line:
                if line.service_number.sale_subscription:
                    line.service_number.sale_subscription.sudo().message_post(body="El servicio (" + line.service_number.name + ") esta en proceso de modificación" , partner_ids=[so.company_id.subscription_user_id.partner_id.id])

                if line.service_number.sale_subscription_line:
                    line.sudo().service_number.sale_subscription_line.to_modify = True
        return res
