# -*- coding: utf-8 -*-

from odoo import models, api, fields

class SaleSubscription(models.Model):
	_inherit = 'sale.subscription'

	corporate_group_id = fields.Many2one('res.partner.category', string='Grupo corporativo', store=True, related='contact_id.corporate_group_id')

	