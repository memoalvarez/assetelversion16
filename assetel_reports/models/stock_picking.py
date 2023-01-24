# -*- coding: utf-8 -*-
import logging
import base64

from odoo import models, api, fields
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sign_template = fields.Many2one('sign.template', string='Firma')
    sign_request = fields.Many2one('sign.request', string='Solicitud de firma')
    


    def _compute_employee_id(self):
        for reg in self:
            employee_id_search = reg.sudo().env['hr.employee'].search([('name', '=', reg.partner_id.name)]).id
            reg.update({'employee_id': employee_id_search})

                
    employee_id = fields.Many2one('hr.employee', string='Empleado', compute='_compute_employee_id')

    def _compute_employee_operation_type(self):
        for reg in self:
            if reg.picking_type_id.sequence_code == 'OUT/EMPLEADO':
                reg.employee_operation_type = True
            else:
                reg.employee_operation_type = False

                
    employee_operation_type = fields.Boolean(string='Tipo de operación empleado', default=False, compute='_compute_employee_operation_type')


    def action_view_sign_templates(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sign.template",
            "views": [[False, "form"]],
            "res_id": self.sign_template.id,
            "context": {"user_id": self.user_id.partner_id.id},
        }
    
    def action_view_sign_request(self):
        action = self.env.ref('sign.sign_request_action').read()[0]

        if self.sign_template:
            action['views'] = [(self.env.ref('sign.sign_request_view_form').id, 'form')]
            action['res_id'] = self.sign_request.id
        return action


    def pdf_generator(self):
        pdf = self.env.ref('assetel_reports.responsive_template').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # save pdf as attachment
        name = "Responsiva" + str(self.id)
        return self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })
    
    def createandopen_signature_request_responsive(self):
        if self.sign_template:
            self.sign_template.responsive = False
            self.sign_template.active = False
            self.sign_template = False
            
        if self.sign_request:
            self.sign_request.responsive = False
            self.sign_request.active = False
            self.sign_request = False
            

        for reg in self:
            values = {
                    'name' : 'Responsiva ' + str(reg.id),
                    'attachment_id': reg.pdf_generator().id,
                    'responsive': reg.id,
                    'hide_template': True
                }

            new_template = self.env['sign.template'].create(values)  
            reg.sign_template = new_template.id
            #Sign
            sign = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_signature').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.042,
                    'posY': 0.685,
                    'width': 0.287,
                    'height': 0.099,
                }
            obs_1 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.296,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_2 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.311,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_3 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.327,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_4 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.343,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_5 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.359,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_6 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.375,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_7 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.392,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_8 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.408,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_9 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.424,
                    'width': 0.382,
                    'height': 0.014,
                }
            obs_10 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.576,
                    'posY': 0.440,
                    'width': 0.382,
                    'height': 0.014,
                }
            
            new_sign = self.env['sign.item'].create(sign) 
            new_obs_1 = self.env['sign.item'].create(obs_1)
            new_obs_2 = self.env['sign.item'].create(obs_2)
            new_obs_3 = self.env['sign.item'].create(obs_3)
            new_obs_4 = self.env['sign.item'].create(obs_4)
            new_obs_5 = self.env['sign.item'].create(obs_5)
            new_obs_6 = self.env['sign.item'].create(obs_6)
            new_obs_7 = self.env['sign.item'].create(obs_7)
            new_obs_8 = self.env['sign.item'].create(obs_8)
            new_obs_9 = self.env['sign.item'].create(obs_9)
            new_obs_10 = self.env['sign.item'].create(obs_10)
               

            return reg.action_view_sign_templates()

