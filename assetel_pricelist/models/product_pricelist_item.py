# -*- coding: utf-8 -*-
from odoo import models, api, fields

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    product_attribute_ids = fields.Many2many(related='product_id.product_template_attribute_value_ids', readonly=True)
    product_template_id = fields.Many2one(related='product_id.product_tmpl_id', string='Plantilla de producto', readonly=True, store=True)
    product_category = fields.Char(related='product_id.categ_id.name', string='Categorías', readonly=True, store=True)
