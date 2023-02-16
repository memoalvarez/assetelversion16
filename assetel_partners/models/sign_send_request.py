# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, api, _, Command

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
        
                
        
    def create_request(self):
        template_id = self.template_id.id
        if self.signers_count:
            signers = [{'partner_id': signer.partner_id.id, 'role_id': signer.role_id.id, 'mail_sent_order': signer.mail_sent_order} for signer in self.signer_ids]
        else:
            signers = [{'partner_id': self.signer_id.id, 'role_id': self.env.ref('sign.sign_item_role_default').id, 'mail_sent_order': self.signer_ids.mail_sent_order}]
        cc_partner_ids = self.cc_partner_ids.ids
        reference = self.filename
        subject = self.subject
        message = self.message
        message_cc = self.message_cc
        attachment_ids = self.attachment_ids
        refusal_allowed = self.refusal_allowed
        
        if self.afiliacion_id:
            afiliacion_id = self.afiliacion_id.id
            sign_request = self.env['sign.request'].create({
                'template_id': template_id,
                'afiliacion_id': afiliacion_id,
                'request_item_ids': [Command.create({
                    'partner_id': signer['partner_id'],
                    'role_id': signer['role_id'],
                    'mail_sent_order': signer['mail_sent_order'],
                }) for signer in signers],
                'reference': reference,
                'subject': subject,
                'message': message,
                'message_cc': message_cc,
                'attachment_ids': [Command.set(attachment_ids.ids)],
                'refusal_allowed': refusal_allowed,
            })
            sign_request.message_subscribe(partner_ids=cc_partner_ids)
            return sign_request
        else:
            sign_request = self.env['sign.request'].create({
                'template_id': template_id,
                'request_item_ids': [Command.create({
                    'partner_id': signer['partner_id'],
                    'role_id': signer['role_id'],
                    'mail_sent_order': signer['mail_sent_order'],
                }) for signer in signers],
                'reference': reference,
                'subject': subject,
                'message': message,
                'message_cc': message_cc,
                'attachment_ids': [Command.set(attachment_ids.ids)],
                'refusal_allowed': refusal_allowed,
            })
            sign_request.message_subscribe(partner_ids=cc_partner_ids)
            return sign_request