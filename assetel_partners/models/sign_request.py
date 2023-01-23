# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, api, _ 

class SignRequest(models.Model):
    _inherit = 'sign.request'

    afiliacion_id = fields.Many2one('assetel.partners', string='Afiliacion')


    @api.model
    def initialize_new_afilation(self, id, signers, followers, reference, afiliacion_id, subject, message, send=True, without_mail=False):
        sign_users = self.env['res.users'].search([('partner_id', 'in', [signer['partner_id'] for signer in signers])]).filtered(lambda u: u.has_group('sign.group_sign_user'))
        sign_request = self.create({'template_id': id, 'reference': reference, 'afiliacion_id': afiliacion_id, 'favorited_ids': [(4, item) for item in (sign_users | self.env.user).ids]})
        sign_request.message_subscribe(partner_ids=followers)
        sign_request.activity_update(sign_users)
        sign_request.set_signers(signers)
        if send:
            sign_request.action_sent(subject, message)
        if without_mail:
            sign_request.action_sent_without_mail()
        return {
            'id': sign_request.id,
            'token': sign_request.access_token,
            'sign_token': sign_request.request_item_ids.filtered(lambda r: r.partner_id == self.env.user.partner_id)[:1].access_token,
        }


    def action_view_afilacion(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "assetel.partners",
            "views": [[False, "form"]],
            "res_id": self.afiliacion_id.id,
            "context": {"create": False},
        }