# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    subscription_user_id = fields.Many2one('res.users', string='Encargado de suscripciones')
