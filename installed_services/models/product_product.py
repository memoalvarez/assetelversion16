# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    manufacturing_product = fields.Many2one('product.product', string='Producto para fabricación')
    sale_service = fields.Many2one('product.product', string='Servicio para venta')