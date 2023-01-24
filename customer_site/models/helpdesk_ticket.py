# -*- coding: utf-8 -*-
from odoo import models, api, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    site = fields.Many2one('res.partner', string='Sitio')

    contact_id = fields.Many2one('res.partner', string='Contacto')

    @api.onchange('partner_id')
    def _onchange_partner_id_customer_site(self):
        if self.partner_id:
            if self.partner_id.parent_id:
                self.contact_id = self.partner_id.parent_id
                self.empresarial_group = self.partner_id.parent_id.empresarial_group_id

            else:
                self.contact_id = self.partner_id
                self.empresarial_group = self.partner_id.empresarial_group_id

    @api.onchange('site')
    def _onchange_site_customer_site(self):
        if self.site:
            self.empresarial_group = self.site.parent_id.empresarial_group_id