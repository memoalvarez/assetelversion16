# -*- coding: utf-8 -*-

from odoo import models, api, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    @api.model
    def create(self, vals):
        result = super(CrmLead, self).create(vals)

        if result.partner_assigned_id:
            if result.create_uid != result.partner_assigned_id:
                result.partner_assigned_id = result.create_uid.partner_id.id

            text = '''<div style="margin: 0px; padding: 0px;">
                <p style="margin: 0px; padding: 0px; font-size: 13px;">
                    Buen día,
                    <br/><br/>
                    Se ha registrado un nuevo lead:
                    <br/><br/>
                    Partner: ''' + str(result.partner_assigned_id.name) + '''
                    <br/>
                    Contacto: ''' + str(result.contact_name) + '''
                    <br/>
                    Título: ''' + str(result.name) + '''
                    <br/>
                    Descripción: ''' + str(result.description) + '''
                    <br/><br/>
                    Saludos.
                </p>'''
            
            for contact in result.team_id.member_ids:
                result.message_post(body=text, partner_ids=[contact.partner_id.id])

            result.message_post(body=text, partner_ids=[result.team_id.user_id.partner_id.id])

        return result

    #Metodo que hace envio automatico de correo elctronico en etapa configurada
    def _track_template(self, changes):
        res = super(CrmLead, self)._track_template(changes)
        test_service_request = self[0]
        if 'stage_id' in changes and test_service_request.stage_id.mail_template_id:
            res['stage_id'] = (test_service_request.stage_id.mail_template_id, {
                'auto_delete_message': False,
                'subtype_id': self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'),
                'email_layout_xmlid': 'mail.mail_notification_light'
            })
        return res


    def _get_comercial(self):
        return self.sudo().user_id.name
