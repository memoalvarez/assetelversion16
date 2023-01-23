# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    email_notification = fields.Boolean(string='Notificación general')
    