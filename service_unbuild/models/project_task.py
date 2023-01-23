# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    unbuild_task = fields.Boolean(string='Tarea de Baja', default=False)
    unbuild_finished = fields.Boolean(string='Desinstalacion terminada', default=False)
    deactivate_service_stage = fields.Boolean(string='Etapa de desactivar servicio', default=False, related='stage_id.deactivate_service_stage')
    requesting_user = fields.Many2one('res.users', string='usuario que solicita')

    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.unbuild_task:
            result.service_number.unbuild_task_id = result.id

            for line in result.project_id.users_to_notify:
                result.message_post(body="Solicitud de baja", partner_ids=[line.partner_id.id])

            result.name = '(#' + str(result.id) + ') - ' + result.name
        
        return result

    #Cambiar de estado el numero de servicio
    def new_service_unbuild(self):
        for task in self:
            if task.unbuild_task:
                task.service_number.stage = 'disabled'
                note = task.service_number.notes + '<br/><p>Servicio dado de baja desde:</p><p>Tarea.- ' + self.name + '</p>'
                task.service_number.notes = note
                task.service_number.message_post(body="Servicio desactivado", partner_ids=[task.company_id.subscription_user_id.partner_id.id])
                task.unbuild_finished = True


    def authorize_unbuild(self):
        for reg in self:
            reg.active = True
            reg.message_post(body="Baja Aprobada")
            reg.service_number.message_post(body="La solicitud de baja (#" + str(reg.id) + ") fue aprobada", partner_ids=[reg.requesting_user.partner_id.id])
            if reg.service_number.sale_subscription:
                reg.service_number.sale_subscription.message_post(body="El servicio (" + reg.service_number.name + ") esta en proceso de baja" , partner_ids=[reg.company_id.subscription_user_id.partner_id.id])
                reg.service_number.sale_subscription_line.to_unbuild = True


    def reject_unbuild(self):
        for reg in self:
            reg.active = True
            reg.message_post(body="Baja Rechazada")
            reg.service_number.unbuild_task_id = False
            reg.service_number.message_post(body="La solicitud de baja (#" + str(reg.id) + ") fue rechazada", partner_ids=[reg.requesting_user.partner_id.id])
