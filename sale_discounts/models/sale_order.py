# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approved_order = fields.Boolean("Presupuesto aprobado", default=True)


    #FUNCIONA EN VERSION 16
    @api.onchange('order_line')
    def _on_change_order_line_sale_discount(self):
        approved = True
        for line in self.order_line:
            if line.discount > 0:
                approved = False

        self.approved_order = approved

    #FUNCIONA EN VERSION 16
    def checking_action(self):
        self.message_post(body="Solicitud de aprobación de presupuesto", partner_ids=[self.team_id.user_id.partner_id.id])

        return True

    #FUNCIONA EN VERSION 16
    def approved_action(self):
        self.approved_order = True
        self.message_post(body="Presupuesto Aprobado", partner_ids=[self.user_id.partner_id.id])

        return True

    #FUNCIONA EN VERSION 16
    def rejected_action(self):
        self.message_post(body="Presupuesto Rechazado", partner_ids=[self.user_id.partner_id.id])
        self.write({'state': 'draft'})
        return True


