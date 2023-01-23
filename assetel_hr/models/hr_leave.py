# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    backup = fields.Many2many('hr.employee', 'backup_employees', 'employee_id', 'backup_id', string="Backup")

    def action_validate(self):
        result = super(HrLeave, self).action_validate()

        if self.state == 'validate':
            if self.holiday_status_id.email_notification:
                general = self.sudo().env['res.partner'].search([('email', '=', 'general@assetel.com')]).id
                capital = self.sudo().env['res.partner'].search([('email', '=', 'jgomez@assetel.com')]).id
                backups = "<p>Backups:</p><ul>"

                if self.backup:
                    for backup in self.backup:
                        backups = backups + "<li><p>" + backup.name + "</p></li>"

                self.message_post(body="<p>Hola</p><p>Informamos que la incidencia " + self.holiday_status_id.name + " ha sido aprobada para el colaborador " + self.employee_id.name +
                    " desde " + str(self.request_date_from) + " hasta " + str(self.request_date_to) + ". Si alguna parte de su operación depende del seguimiento de esta persona, le sugerimos contactarla para programar la revisión de temas durante su ausencia y conocer al backup asignado.</p>" + 
                    backups + "</ul><p>Saludos</p>", subject="NOTIFICACIÓN DE AUSENCIA", author_id=capital, partner_ids=[general])

        return result