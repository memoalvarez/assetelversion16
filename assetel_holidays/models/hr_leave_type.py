# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    automatic_allocation = fields.Boolean(string='Asignacion automatica')
    accumulative = fields.Boolean(string='Acumulables')
    holidays_table = fields.One2many('hr.leave.table', 'hr_leave_type_id', string='Tabla de vacaciones')
    employee_ids = fields.Many2many('hr.employee', string='Empleados')


    @api.model
    def _cron_recurring_holidays_calculation(self):
        hr_leave_types = self.env['hr.leave.type'].sudo().search([('active', '=', True), ('automatic_allocation', '=', True)])

        for leave_type in hr_leave_types:
            for employee in leave_type.employee_ids:
                if employee.contract_id.date_start:
                    #Se toma la fecha de inicio del empleado
                    date_start = employee.contract_id.date_start
                    #Se toma la fecha actual (de servidor)
                    current_date = datetime.today().date()
                    
                    #Calculo de años de antiguedad
                    diff_date = current_date - date_start
                    years = diff_date.days / 365.0
                    antiguedad_anos = int(years)

                    #Se asigna a "anniversary" fecha de aniversario
                    anniversary = date_start + relativedelta(years=antiguedad_anos)

                    #Se crea variable que guardara dias restantes
                    remaining = 0
                    note=''

                    #Si el tipo de ausencia tiene "accumulative" en false hace lo siguiente
                    if not leave_type.accumulative:
                        #Buscamos en el reporte de ausencias del empleado los dias restantes
                        leave_report = self.env['hr.leave.report'].sudo().search([('holiday_status_id', '=', leave_type.id), ('employee_id', '=', employee.id)])
                        
                        for line in leave_report:
                            remaining += line.number_of_days

                        note += '\nDias no acumulables restantes: ' + str(remaining)
                    
                     #Si la fecha actual y la fecha de aniversario es la misma, hacer lo siguiente
                    if current_date == anniversary:
                        #Se crea variable para guardar dias de vacaciones
                        number_of_days = 0
                        #Busqueda de dias
                        for line in leave_type.holidays_table:
                            if line.years <= antiguedad_anos:
                                number_of_days = line.holidays
                            else:
                                break

                        values = {
                            'holiday_type': 'employee',
                            'employee_id': employee.id,
                            'holiday_status_id': leave_type.id,
                            'allocation_type': 'regular',
                            'number_of_days': number_of_days - remaining,
                            'name': 'Asignación automática',
                            'notes': 'Asignacion anual de vacaciones' + note
                        }
                        new_allocation = self.env['hr.leave.allocation'].create(values)
                        new_allocation.action_approve()
                        if new_allocation.state != 'validate':
                            new_allocation.action_validate()

                            