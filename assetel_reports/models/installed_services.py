# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.modules.module import get_resource_path
import base64

class InstalledServices(models.Model):
    _inherit = 'installed.services'
    

    def action_report_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('assetel_reports.email_template_installed_services', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)

        pdf_path = get_resource_path('assetel_reports', 'static/src', 'Metodos de Soporte y Escalacion SAE-Conectividad-Cloud 2020.pdf')
        base64.b64encode(open(pdf_path, 'rb').read())

        attachment = self.env['ir.attachment'].create({
            'name': 'Metodos de Soporte y Escalacion SAE-Conectividad-Cloud 2020',
            'type': 'binary',
            'datas': base64.b64encode(open(pdf_path, 'rb').read())})

        template.attachment_ids = attachment


        if template.lang:
            lang = template._render_template(template.lang, 'installed.services', self.ids[0])
        ctx = {
            'default_model': 'installed.services',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "assetel_reports.template_installed_services",
            'force_email': True,
            'model_description': "Numero de servicio",
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }