# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions

class HrLeaveCalculation(models.Model):
    _name = 'hr.leave.table'

    hr_leave_type_id = fields.Many2one('hr.leave.type', string='Tipo de ausencia')
    years = fields.Float('Antigüedad / Años')
    holidays = fields.Float('Vacaciones / Días')
    