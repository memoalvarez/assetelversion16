# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class SaleSuscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    empresarial_group = fields.Many2one(string='Grupo empresarial', related='analytic_account_id.empresarial_group')
    business_name = fields.Many2one(string='Razón Social', related='analytic_account_id.partner_id')
    subscription_template = fields.Many2one(string='Plantilla de suscripción', related='analytic_account_id.template_id')
