# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, api, _ 

class SignSendRequest(models.TransientModel):
    _inherit = 'sign.send.request'

    afiliacion_id = fields.Many2one('assetel.partners', string='Afiliacion')


    @api.model
    def default_get(self, fields):
        res = super(SignSendRequest, self).default_get(fields)

        if self.env.context.get('afiliacion_id'):
            template = self.env['sign.template'].browse(res['template_id'])
            roles = template.mapped('sign_item_ids.responsible_id')
            res['signer_ids'] = [(0, 0, {
                'role_id': role.id,
                'partner_id': self.env.context.get('contact_id'),
            }) for role in roles]

            res['afiliacion_id'] = self.env.context.get('afiliacion_id')
            
        return res


    def create_request(self, send=True, without_mail=False):
        template_id = self.template_id.id
        if self.signers_count:
            signers = [{'partner_id': signer.partner_id.id, 'role': signer.role_id.id} for signer in self.signer_ids]
        else:
            signers = [{'partner_id': self.signer_id.id, 'role': False}]
        followers = self.follower_ids.ids
        reference = self.filename
        subject = self.subject
        message = self.message

        if self.afiliacion_id:
            afiliacion_id = self.afiliacion_id.id
            return self.env['sign.request'].initialize_new_afilation(template_id, signers, followers, reference, afiliacion_id, subject, message, send, without_mail)
        else:
            return self.env['sign.request'].initialize_new(template_id, signers, followers, reference, subject, message, send, without_mail)