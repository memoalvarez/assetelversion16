# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import date, datetime


class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'


    def _compute_history_ids(self):
        #Se cuentan todos los registros de historia#
        for reg in self:
            hist_count = reg.env['history.sale.subscription'].search_count([['active_sale_subscription', '=', reg.id]])
            reg.update({
                'history_count': hist_count,
            })

    history_count = fields.Integer(string='Modification sale order', compute='_compute_history_ids')
    history_ids = fields.One2many('history.sale.subscription', 'active_sale_subscription', 'Registros de historial')


    def action_view_history(self):
        action = self.env.ref('subscription_history.get_history_sale_subscription_view').read()[0]

        history_regs = self.mapped('history_ids')

        if len(history_regs) > 1:
            action = self.env.ref('subscription_history.get_history_sale_subscription_view').read()[0]
            action['domain'] = [('id', 'in', history_regs.ids)]
            action['context'] = dict(create=False, edit=False)
            return action
        elif history_regs:
            return {
                    "type": "ir.actions.act_window",
                    "res_model": "history.sale.subscription",
                    "views": [[False, "form"]],
                    "res_id": history_regs.id,
                    "context": {"create": False, "edit": False},
                }



    def new_history(self):
        for reg in self:
            values = {
                'active_sale_subscription' : reg.id,
                'modification_date' : datetime.now(),
                'display_name' : reg.display_name,
                'empresarial_group' : reg.empresarial_group.name,
                'partner_id' : reg.partner_id.name,
                'pricelist_id' : reg.pricelist_id.name,
                'close_reason_id' : reg.close_reason_id.name,
                'date_start' : reg.date_start,
                'date' : reg.date,
                'template_id' : reg.template_id.name,
                'user_id' : reg.user_id.name,
                'team_id' : reg.team_id.name,
                'corporate_group_id' : reg.corporate_group_id.name,
                'company_id' : reg.company_id.name,
                'recurring_total' : reg.recurring_total,
                'currency_id' : reg.currency_id.id,
                'code' : reg.code,
            }
            principal = self.env['history.sale.subscription'].create(values)

            #Por cada linea en lotes#
            for line in reg.recurring_invoice_line_ids:
                values_lot = {
                    'history_sale_subscription_id' : principal.id,
                    'service_number' : line.service_number.name,
                    'name' : line.name,
                    'product_id' : line.product_id.name,
                    'site' : line.site.name,
                    'uom_id' : line.uom_id.name,
                    'quantity' : line.quantity,
                    'price_unit' : line.price_unit,
                    'discount' : line.discount,
                    'price_subtotal' : line.price_subtotal,
                }
                lines = self.env['history.sale.subscription.line'].create(values_lot)

        return True
        