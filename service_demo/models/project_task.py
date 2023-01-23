# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions
from datetime import date, datetime

class ProjectTask(models.Model):
    _inherit = 'project.task'

    demo_task = fields.Boolean(string='Tarea de demo', default=False)
    demo_rejected = fields.Boolean(string='Demo Rechazado', default=False)

    demo_application_date = fields.Datetime('Fecha solicitud demo')
    demo_installation_date = fields.Datetime('Fecha instalacion demo')
    demo_finish_date = fields.Datetime('Fecha finalización demo')

    product_id = fields.Many2one('product.product', 'Servicio')
    demo_service_life = fields.Integer('Dias de vigencia de demo')

    active_demo_service = fields.Many2one('installed.services', 'Servicio demo activo')

    order_id_demo = fields.Many2one('sale.order', 'Presupuesto')
    sale_order_line_demo = fields.Many2one('sale.order.line', 'Servicio')
    sizing_task_id_demo = fields.Many2one('project.task', 'Dimensionamiento')

    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        #En la oportunidad se registra la tarea generada
        if result.demo_task:
            result.sale_line_id = result.sale_order_line_demo.id
            result.planned_hours = result.sale_line_id.product_uom_qty

            result.name = '(#' + str(result.id) + ') - ' + result.name
            result.lead_id.message_post(body="Nueva solicitud de demo (#" + str(result.id) + "), esperando aprobación")

            for line in result.project_id.users_to_notify:
                result.message_post(body="Buen día<br/><br/>Solicito la aprobación del Demo (#" + str(result.id) + ")<br/><br/>Descripción:<br/>" + str(result.description) +"<br/><br/>Saludos", partner_ids=[line.partner_id.id])

        if result.sale_order_id.opportunity_id.demo_task_ids:
            for demo in result.sale_order_id.opportunity_id.demo_task_ids:
                if demo.service_number:
                    if result.sale_line_id.product_id == demo.service_number.product_id:
                        result.active_demo_service = demo.service_number
        
        return result


    @api.onchange('sale_order_line_demo')
    def _on_change_sale_order_line_demo(self):
        if self.sale_order_line_demo.product_id:
            self.product_id = self.sale_order_line_demo.product_id


    def new_mrp(self):
        result = super(ProjectTask, self).new_mrp()

        for reg in self:
            if reg.product_id:
                result['context'] = {'default_product_id': reg.product_id.manufacturing_product.id,
                'default_project_task': reg.id}

        return result


    def new_demo_service(self):
        if self.mrp_production:
            note = '<p>Servicio creado desde:</p><p>Tarea.- ' + self.name + '</p>' + '<p>Orden de fabricacion.- ' + self.mrp_production.name + '</p>'    
        else:
            note = '<p>Servicio creado desde:</p><p>Tarea.- ' + self.name + '</p>'

        if self.partner_id.parent_id:
            cliente = self.partner_id.parent_id
        else:
            cliente = self.partner_id

        action = self.env.ref('installed_services.get_installed_services_view').read()[0]
        action['views'] = [(self.env.ref('installed_services.installed_services_form').id, 'form')]
        action['context'] = {'default_product_id': self.product_id.id,
        'default_description': self.product_id.name, 'default_stage': 'installed',
        'default_project_task': self.id , 'default_empresarial_group': cliente.empresarial_group_id.id,
        'default_partner_id': cliente.id, 'default_site': self.sale_order_line_demo.site.id, 'default_notes': note,
        'default_demo_service': True, 'default_demo_installation_date': datetime.now()}
        action['target'] = 'new'
        return action


    def formalize_demo(self):

        if self.mrp_production:
            note = self.active_demo_service.notes + '<br/><p>Servicio modificado desde:</p><p>Tarea.- ' + self.name + '</p><p>Orden de fabricacion.- ' + self.mrp_production.name + '</p>'
        else:
            note = self.active_demo_service.notes + '<br/><p>Servicio formalizado desde:</p><p>Tarea.- ' + self.name + '</p>'

        for reg in self:
            reg.service_number = reg.active_demo_service
            reg.active_demo_service = False
            reg.service_number.demo_service = False
            reg.service_number.project_task = reg.id
            reg.service_number.demo_installation_date = False
            reg.service_number.demo_finish_date = False
            reg.service_number.notes = note
            reg.sale_line_id.qty_delivered = reg.sale_line_id.product_uom_qty
            reg.sale_line_id.service_number = reg.service_number

        action = self.env.ref('installed_services.get_installed_services_view').read()[0]
        if self.service_number:
            action['views'] = [(self.env.ref('installed_services.installed_services_form').id, 'form')]
            action['res_id'] = self.service_number.id
            action['target'] = 'new'

        return action


    def authorize_demo(self):
        for reg in self:
            if reg.sizing_task_id_demo.stage_id.end_sizing == True:
                reg.active = True
                reg.message_post(body="Demo Aprobado")
                reg.lead_id.message_post(body="Buen dia<br/><br/>La solicitud de demo (#" + str(reg.id) + ") ha sido aprobada<br/><br/>Saludos", partner_ids=[reg.lead_id.user_id.partner_id.id])
            else:
                raise exceptions.ValidationError('El dimensionamiento (#' + str(reg.sizing_task_id_demo.id) + ') debe estar terminado')

    def reject_demo(self):
        for reg in self:
            reg.active = True
            reg.message_post(body="Demo Rechazado")
            reg.demo_rejected = True
            reg.lead_id.message_post(body="Buen dia<br/><br/>La solicitud de demo (#" + str(reg.id) + ") ha sido rechazada<br/><br/>Saludos", partner_ids=[reg.lead_id.user_id.partner_id.id])

    def action_view_sizing(self):
        action = self.env.ref('project.act_project_project_2_project_task_all').read()[0]

        if self.lead_id:
            action['views'] = [(self.env.ref('project.view_task_form2').id, 'form')]
            action['res_id'] = self.sizing_task_id_demo.id
        return action
            