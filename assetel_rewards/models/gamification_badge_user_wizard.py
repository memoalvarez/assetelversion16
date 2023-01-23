# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import UserError, AccessError
import logging

_logger = logging.getLogger(__name__)

class GamificationBadgeUserWizard(models.TransientModel):
    _inherit = 'gamification.badge.user.wizard'
    
    puntos = fields.Integer(string="Puntos")
    
    def action_grant_badge(self):
        """Wizard action for sending a badge to a chosen employee"""
        if not self.user_id:
            raise UserError(_('You can send badges only to employees linked to a user.'))

        if self.env.uid == self.user_id.id:
            raise UserError(_('You can not send a badge to yourself.'))

        values = {
            'user_id': self.user_id.id,
            'sender_id': self.env.uid,
            'badge_id': self.badge_id.id,
            'employee_id': self.employee_id.id,
            'comment': self.comment,
            'puntos': self.puntos,
        }
        _logger.info('MODEL: 1')
        return self.env['gamification.badge.user'].create(values)._send_badge()
