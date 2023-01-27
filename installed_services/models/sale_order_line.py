# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    service_number = fields.Many2one('installed.services', string='N° de servicio')
    contact_id = fields.Many2one('res.partner', string='Contacto')
    analytic_account_id = fields.Many2one('sale.order', string="Suscripción")

    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_id_installed_services(self):
        self.contact_id = self.analytic_account_id.contact_id



    @api.onchange('service_number')
    def _onchange_service_number(self):
        for reg in self:
            if reg.service_number:
                reg.product_template_id = reg.service_number.product_template_id.id
                reg.site = reg.service_number.site.id
                reg.product_uom_qty = reg.service_number.project_task.sale_line_id.product_uom_qty
                reg.discount = reg.service_number.project_task.sale_line_id.discount


    @api.onchange('product_template_id', 'product_uom_qty')
    def onchange_product_quantity(self):
        res = super(SaleOrderLine, self).onchange_product_quantity()

        self.name = self.service_number.description
        self.price_unit = self.service_number.project_task.sale_line_id.price_unit

        return res
