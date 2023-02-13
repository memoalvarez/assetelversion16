# -*- coding: utf-8 -*-
from odoo import models, api, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    installed_service_id = fields.Many2one('installed.services', string='Servicio')


    @api.onchange('installed_service_id')
    def _onchange_installed_service_id(self):
        if self.installed_service_id:
            self.site = self.installed_service_id.site

