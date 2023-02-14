# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    subscription_user_id = fields.Many2one(related='company_id.subscription_user_id', readonly=False, string='Encargado de suscripciones')
