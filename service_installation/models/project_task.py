# -*- coding: utf-8 -*-
import logging
import base64

from odoo import models, api, fields
_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    mrp_production = fields.Many2one('mrp.production', string='Orden de fabricación')
    service_number = fields.Many2one('installed.services', string='Numero de servicio')
    sign_template = fields.Many2one('sign.template', string='Firma')
    sign_request = fields.Many2one('sign.request', string='Solicitud de firma')

    #CAMPOS RELACIONADOS CON EL TIPO DE ETAPA PARA PODER OCULTAR BOTONES
    mrp_stage = fields.Boolean(string='Etapa de fabricación', default=False, related='stage_id.mrp_stage')
    service_registration_stage = fields.Boolean(string='Etapa de registro de servicio', default=False, related='stage_id.service_registration_stage')

    site = fields.Many2one('res.partner', string='Sitio', related='sale_line_id.site')

    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.sale_line_id:
            text = '''<div style="margin: 0px; padding: 0px;">
                <p style="margin: 0px; padding: 0px; font-size: 13px;">
                    Buen día,
                    <br/><br/>
                    Se ha creado una nueva tarea:
                    <br/><br/>
                    Proyecto: ''' + str(result.project_id.name) + '''
                    <br/>
                    Nombre: ''' + str(result.name) + '''
                    <br/>
                    Pedido de venta: ''' + str(result.sale_order_id.name) + '''
                    <br/>
                    Cliente: ''' + str(result.partner_id.name) + '''
                    <br/>
                    Sitio: ''' + str(result.site.name) + '''
                    <br/><br/>
                    Saludos.
                </p>'''

            for line in result.project_id.users_to_notify:
                result.message_post(body=text, partner_ids=[line.partner_id.id])
        
        return result

    
    def new_mrp(self):
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
        action['context'] = {'default_product_id': self.sale_line_id.product_id.manufacturing_product.id,
        'default_project_task': self.id, 'default_product_uom_qty': self.sale_line_id.product_uom_qty}
        action['target'] = 'new'
        return action



    def new_installed_service(self):
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
        action['context'] = {'default_product_id': self.sale_line_id.product_id.id,
        'default_description': self.sale_line_id.name, 'default_stage': 'installed',
        'default_project_task': self.id , 'default_empresarial_group': cliente.empresarial_group_id.id,
        'default_partner_id': cliente.id, 'default_razon_social_id': self.sale_line_id.order_id.partner_invoice_id.id,
        'default_encargado_comercial': self.sale_line_id.order_id.user_id.id, 'default_site': self.sale_line_id.site.id, 
        'default_service_price_unit': self.sale_line_id.price_subtotal, 'default_quantity': self.sale_line_id.product_uom_qty, 'default_notes': note}
        action['target'] = 'new'
        return action



    def action_view_mrp(self):
        action = self.env.ref('mrp.mrp_production_action').read()[0]

        if self.mrp_production:
            action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
            action['res_id'] = self.mrp_production.id
        return action



    def action_view_installed_service(self):
        action = self.env.ref('installed_services.get_installed_services_view').read()[0]

        if self.service_number:
            action['views'] = [(self.env.ref('installed_services.installed_services_form').id, 'form')]
            action['res_id'] = self.service_number.id
        return action


    def action_view_sign_templates(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sign.template",
            "views": [[False, "form"]],
            "res_id": self.sign_template.id,
            "context": {"user_id": self.user_id.partner_id.id, "customer_id": self.partner_id.id},
        }

    def action_view_sign_request(self):
        action = self.env.ref('sign.sign_request_action').read()[0]

        if self.sign_template:
            action['views'] = [(self.env.ref('sign.sign_request_view_form').id, 'form')]
            action['res_id'] = self.sign_request.id
        return action

    def register_equipment(self):
        #A CADA SERIE USADA EN LA ORDEN DE PRODUCCION LE ASIGNA UN NUMERO DE SERVICIO PARA
        #QUE AUTOMATICAMENTE APAREZCAN LOS EQUIPOS USADOS EN EL REGISTRO DEL SERVICIO
        for line in self.mrp_production.move_raw_ids:
                for line2 in line.move_line_ids:
                    line2.lot_id.service_number = self.service_number



    def pdf_generator(self):
        pdf = self.env.ref('service_installation.report_project_task').render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # save pdf as attachment
        name = "Reporte de servicio" + str(self.id)
        return self.env['ir.attachment'].create({
            'name': name,
            'type': 'binary',
            'datas': b64_pdf,
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

    def createandopen_signature_request(self):
        if self.sign_template:
            self.sign_template.project_task = False
            self.sign_template.active = False
            self.sign_template = False
            
        if self.sign_request:
            self.sign_request.project_task = False
            self.sign_request.active = False
            self.sign_request = False
            

        for reg in self:
            values = {
                    'name' : 'Reporte de servicio ' + str(reg.id),
                    'attachment_id': reg.pdf_generator().id,
                    'project_task': reg.id,
                    'hide_template': True
                }

            new_template = self.env['sign.template'].create(values)  
            reg.sign_template = new_template.id
            #Sign
            values1 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_signature').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_customer').id,
                    'page': 1,
                    'posX': 0.182,
                    'posY': 0.816,
                    'width': 0.200,
                    'height': 0.050,
                }
            #Contacto
            values2 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.137,
                    'posY': 0.166,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Telefono
            values3 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.726,
                    'posY': 0.166,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Puesto
            values4 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.420,
                    'posY': 0.166,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Casillas de verificación
            values5 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.044,
                    'posY': 0.294,
                    'width': 0.028,
                    'height': 0.025,
                }
            values6 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.655,
                    'posY': 0.296,
                    'width': 0.028,
                    'height': 0.025,
                }
            values7 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.349,
                    'posY': 0.299,
                    'width': 0.028,
                    'height': 0.025,
                }
            values8 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.044,
                    'posY': 0.318,
                    'width': 0.028,
                    'height': 0.025,
                }
            values9 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.655,
                    'posY': 0.319,
                    'width': 0.028,
                    'height': 0.025,
                }
            values10 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.350,
                    'posY': 0.321,
                    'width': 0.028,
                    'height': 0.025,
                }
            values11 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.655,
                    'posY': 0.340,
                    'width': 0.028,
                    'height': 0.025,
                }
            values12 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.044,
                    'posY': 0.341,
                    'width': 0.028,
                    'height': 0.025,
                }
            values13 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.350,
                    'posY': 0.342,
                    'width': 0.028,
                    'height': 0.025,
                }
            values14 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.656,
                    'posY': 0.362,
                    'width': 0.028,
                    'height': 0.025,
                }
            values15 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.044,
                    'posY': 0.365,
                    'width': 0.028,
                    'height': 0.025,
                }
            values16 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_checkbox').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.350,
                    'posY': 0.365,
                    'width': 0.028,
                    'height': 0.025,
                }
            #Observaciones
            values17 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_multiline_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.132,
                    'posY': 0.599,
                    'width': 0.735,
                    'height': 0.062,
                }
            #Hora inicio
            values18 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.600,
                    'posY': 0.722,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Hora fin
            values19 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.233,
                    'posY': 0.723,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Fecha
            values20 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': True,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.651,
                    'posY': 0.852,
                    'width': 0.150,
                    'height': 0.015,
                }
            #Otros
            values21 = {
                    'template_id':new_template.id,
                    'type_id': reg.env.ref('sign.sign_item_type_text').id,
                    'required': False,
                    'responsible_id': reg.env.ref('sign.sign_item_role_employee').id,
                    'page': 1,
                    'posX': 0.730,
                    'posY': 0.372,
                    'width': 0.150,
                    'height': 0.015,
                }
            new_text1 = self.env['sign.item'].create(values1)    
            new_text2 = self.env['sign.item'].create(values2)
            new_text3 = self.env['sign.item'].create(values3)
            new_text4 = self.env['sign.item'].create(values4)  
            new_text5 = self.env['sign.item'].create(values5)    
            new_text6 = self.env['sign.item'].create(values6)
            new_text7 = self.env['sign.item'].create(values7)
            new_text8 = self.env['sign.item'].create(values8)
            new_text9 = self.env['sign.item'].create(values9)    
            new_text10 = self.env['sign.item'].create(values10)
            new_text11 = self.env['sign.item'].create(values11)
            new_text12 = self.env['sign.item'].create(values12)
            new_text13 = self.env['sign.item'].create(values13)    
            new_text14 = self.env['sign.item'].create(values14)
            new_text15 = self.env['sign.item'].create(values15)
            new_text16 = self.env['sign.item'].create(values16)
            new_text17 = self.env['sign.item'].create(values17)
            new_text18 = self.env['sign.item'].create(values18)
            new_text19 = self.env['sign.item'].create(values19)
            new_text20 = self.env['sign.item'].create(values20)
            new_text21 = self.env['sign.item'].create(values21)

            return reg.action_view_sign_templates()
