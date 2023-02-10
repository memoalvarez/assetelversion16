# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields
from datetime import date, datetime

_logger = logging.getLogger(__name__)

class InstalledServices(models.Model):
    _inherit = 'installed.services'

    demo_service = fields.Boolean(string='Servicio demo', default=False)
    demo_installation_date = fields.Datetime("Fecha instalacion demo")
    demo_finish_date = fields.Datetime("Fecha finalización demo")

    #Guarda la actividad creada por si se requiere modificar o borrar
    demo_activity_id = fields.Many2one('mail.activity', string='Actividad de demo')

    @api.model
    def create(self, vals):
        result = super(InstalledServices, self).create(vals)

        if result.project_task:
            #Se registra la fecha de activacion de servicio en la tarea de demo
            if result.project_task.demo_task:
                result.project_task.demo_installation_date = result.demo_installation_date

            #Si se registro fecha de termino de demo se registra tambien el la tarea del proyecto
            if result.demo_finish_date:
                result.project_task.demo_finish_date = result.demo_finish_date
                self.create_activity_demo(result)
            
        return result

    def write(self, values):
        result = super(InstalledServices, self).write(values)

        if values.get('demo_finish_date'):
            for reg in self:
                if reg.project_task:
                    #Si se cambio fecha de termino de demo se actualiza tambien el la tarea del proyecto
                    reg.project_task.demo_finish_date = reg.demo_finish_date
                    self.create_activity_demo(reg)

        return result


    def create_activity_demo(self, result):
        if result.demo_activity_id:
            result.demo_activity_id.unlink()

        model_id = self.env['ir.model']._get(self._name).id
        activity_id = self.env['mail.activity.type'].search([['demo_ending_activity', '=', True]])

        vals = {
            'res_model' : "installed.services",
            'res_model_id' : model_id,
            'res_id' : result.id,
            'summary' : "Finalizar demo",
            'activity_type_id' : activity_id.id,
            'date_deadline' : result.demo_finish_date,
            'user_id' : result.project_task.project_id.user_id.id,
        }
        new_activity = self.env['mail.activity'].create(vals)
        result.demo_activity_id = new_activity.id
