# -*- coding: utf-8 -*-
from odoo import models, api, fields

class GamificationBadgeUser(models.Model):
    _inherit = 'gamification.badge.user'

    puntos = fields.Integer(string="Puntos")
    