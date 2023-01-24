# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class ProjectTask(models.Model):
    _inherit = 'project.task'

    modification_service_number = fields.Many2one('installed.services', 'Numero de servicio a modificar')


    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.sale_line_id.service_number:
            result.modification_service_number = result.sale_line_id.service_number
        
        return result


    def modify_service(self):
        if self.mrp_production:
            note = self.modification_service_number.notes + '<br/><p>Servicio modificado desde:</p><p>Tarea.- (#' + str(self.id) + ') ' + self.name + '</p><p>Orden de fabricacion.- ' + self.mrp_production.name + '</p>'
        else:
            note = self.modification_service_number.notes + '<br/><p>Servicio modificado desde:</p><p>Tarea.- (#' + str(self.id) + ') ' + self.name + '</p>'
            
        if self.sale_line_id:
            self.modification_service_number.update({
                'product_id': self.sale_line_id.product_id.id,
                'description': self.sale_line_id.name,
                'project_task': self.id,
                'service_price_unit': self.sale_line_id.price_unit,
                'notes': note,
            })
        else:
           self.modification_service_number.update({
                'project_task': self.id,
                'notes': note,
            }) 

        self.service_number = self.modification_service_number.id
        self.sale_line_id.qty_delivered = self.sale_line_id.product_uom_qty

        if self.mrp_production:
            self.register_equipment()

        action = self.env.ref('installed_services.get_installed_services_view').read()[0]
        if self.service_number:
            action['views'] = [(self.env.ref('installed_services.installed_services_form').id, 'form')]
            action['res_id'] = self.service_number.id
            action['target'] = 'new'

        return action