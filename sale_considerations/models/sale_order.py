# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_considerations = fields.Many2many('sale.considerations', string='Consideraciones')

    @api.onchange('pricelist_id')
    def _on_change_pricelist_id_sale_considerations(self):
        for reg in self:
            reg.sale_considerations = self.env['sale.considerations'].search([['currency_id', '=', reg.pricelist_id.currency_id.id]])


    @api.onchange('sale_considerations')
    def _on_change_sale_considerations(self):
        for reg in self:
            notas = '\n'
            for consideration in reg.sale_considerations:
                notas = notas + consideration.name + '\n' + consideration.note + '\n\n\n'

            reg.note = notas


