# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class InstalledServices(models.Model):
    _inherit = 'installed.services'

    project_task = fields.Many2one('project.task', string='Tarea de proyecto')
    sale_subscription = fields.Many2one('sale.subscription', string='Suscripción')
    sale_subscription_line = fields.Many2one('sale.subscription.line', string='Linea de suscripción')

    quantity = fields.Float(string="Catidad")

    @api.model
    def create(self, vals):
        result = super(InstalledServices, self).create(vals)

        #Se registra el numero de servicio en la tarea desde el que se creo
        #y se registra entrega en SO
        if result.project_task:
            result.project_task.service_number = result.id
            result.message_post(body="Servicio instalado", partner_ids=[result.company_id.subscription_user_id.partner_id.id])
            result.project_task.register_equipment()
            if result.project_task.demo_task == False:
                result.project_task.sale_line_id.qty_delivered = result.project_task.sale_line_id.product_uom_qty
                result.project_task.sale_line_id.service_number = result.id

        #Se registra el numero de servicio en la linea de suscripcion correspondiente
        if result.sale_subscription_line:
            result.sale_subscription_line.service_number = result.id
            
        return result


    def action_view_project_task(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]

        if self.project_task:
            action['views'] = [(self.env.ref('project.view_task_form2').id, 'form')]
            action['res_id'] = self.project_task.id
        return action
        
          