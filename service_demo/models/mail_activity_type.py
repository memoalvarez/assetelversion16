# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    demo_ending_activity = fields.Boolean(string='Actividad finalización demo', default=False)
