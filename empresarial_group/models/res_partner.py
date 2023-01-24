# -*- coding: utf-8 -*-

from odoo import models, api, fields

class ResPartner(models.Model):
	_inherit = 'res.partner'

	empresarial_group_id = fields.Many2one('empresarial.group', string='Grupo empresarial')

	