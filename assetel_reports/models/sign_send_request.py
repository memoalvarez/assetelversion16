# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields
_logger = logging.getLogger(__name__)

class SignSendRequest(models.TransientModel):
    _inherit = 'sign.send.request'

    @api.model
    def default_get(self, fields):
        res = super(SignSendRequest, self).default_get(fields)
        if self.env.context.get('user_id'):
            template = self.env['sign.template'].browse(res['template_id'])
            roles = template.mapped('sign_item_ids.responsible_id')

            res['signer_ids'] = [
                (0, 0, {
                'role_id': roles[0].id,
                'partner_id': self.env.context.get('user_id'),})
            ]


        return res

