# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleConsiderations(models.Model):
	_name = 'sale.considerations'
	_description = 'Consideraciones de venta'

	name = fields.Char(string='Nombre')
	note = fields.Text(string='Descripción')

	commercial_consideration = fields.Boolean(string='Consideración comercial', default=False)
	currency_id = fields.Many2one("res.currency", string="Moneda")