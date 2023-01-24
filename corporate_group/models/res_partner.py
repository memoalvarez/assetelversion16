# -*- coding: utf-8 -*-

from odoo import models, api, fields

class ResPartner(models.Model):
	_inherit = 'res.partner'

	corporate_group_id = fields.Many2one('res.partner.category', string='Grupo corporativo')

	