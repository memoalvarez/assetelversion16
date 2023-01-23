# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EmpresarialGroup(models.Model):
	_name = 'empresarial.group'
	_description = 'Grupos empresariales'

	name = fields.Char(string='Nombre')
	company_ids = fields.One2many('res.partner', 'empresarial_group_id', string='Compañias')

	sales_of__millions = fields.Selection([
        ('a', '0 a 10 millones'),
        ('b', '11 a 30 millones'),
        ('c', '30 a 50 millones'),
        ('d', '50 a 100 millones'),
        ('f', '100 a 500 millones'),
        ('g', 'Mayor a 500 millones'),
        ], string='Ventas en milones',)

	users_of_group_empresarial = fields.Selection([
        ('a', '0 a 10 usuarios'),
        ('b', '11 a 30 usuarios'),
        ('c', '31 a 50 usuarios'),
        ('d', '51 a 100 usuarios'),
        ('e', 'Mayor a 100 usuarios'),
        ], string='Usuarios',)

	locates_of_grouo_emprearial = fields.Selection([
        ('a', '1 a 5 localidades'),
        ('b', '6 a 10 localidades'),
        ('c', '11 a 20 localidades'),
        ('d', 'Mayor a 20 localidades'),
        ], string='Localidades',)