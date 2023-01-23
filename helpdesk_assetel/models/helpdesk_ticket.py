# -*- coding: utf-8 -*-

from odoo import models, api, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model
    def create(self, vals):
        result = super(HelpdeskTicket, self).create(vals)

        if not result.empresarial_group:
            result.empresarial_group =  result.installed_service_id.empresarial_group.id

        if not result.site:
            result.site =  result.installed_service_id.site.id
        
        return result