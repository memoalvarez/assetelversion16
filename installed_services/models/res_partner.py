# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _compute_installed_services_ids(self):
        #Se cuentan todas los servicios instalados del cliente actual#
        for reg in self:
            services_model = reg.env['installed.services'].search_count([['partner_id', '=', reg.id]])
            reg.update({
                'services_count': services_model,
            })

    services_count = fields.Integer(string='Installed services', compute='_compute_installed_services_ids')
    services_ids = fields.One2many('installed.services', 'partner_id', 'Servicios instalados')


    def action_view_services(self):
        action = self.env.ref('installed_services.get_installed_services_view').read()[0]

        services = self.mapped('services_ids')

        if len(services) > 1:
            action['domain'] = [('id', 'in', services.ids)]
        elif services:
            action['views'] = [(self.env.ref('installed_services.installed_services_form').id, 'form')]
            action['res_id'] = services.id
        return action

    @api.model
    def create(self, vals):
        result = super(ResPartner, self).create(vals)

        if result.type == 'site':
            if result.parent_id.name == "Assetel S.A. de C.V.":
                result.ref = "POP"

        return result
        