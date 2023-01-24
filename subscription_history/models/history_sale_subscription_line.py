# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistorySaleSubscriptionLine(models.Model):
    _name = 'history.sale.subscription.line'
    _description = 'Historial de lineas de suscripción'

    history_sale_subscription_id = fields.Many2one('history.sale.subscription', string='Historia de suscripción')

    product_id = fields.Char(string="Producto")
    service_number = fields.Char(string="Producto")
    site = fields.Char(string="Sitio")
    uom_id = fields.Char(string="UdM")
    name = fields.Text(string='Descripcion')
    quantity = fields.Float(string="Catidad")
    price_unit = fields.Float(string='Precio')
    discount = fields.Float(string='Descuento')
    price_subtotal = fields.Float(string='Subtotal')
