# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_helpdesk_form.controller.main import WebsiteForm

class WebsiteFormInherit(WebsiteForm):

    @http.route('''/helpdesk/<model("helpdesk.team", "[('use_website_helpdesk_form','=',True)]"):team>/submit''', type='http', auth="public", website=True)
    def website_helpdesk_form(self, team, **kwargs):
        response = super(WebsiteFormInherit, self).website_helpdesk_form(team)
        installed_service_id = self._get_installed_services()
        response.qcontext['installed_service_id'] = installed_service_id
        return response
        

    def _get_installed_services(self):
        installed_services = request.env['installed.services'].sudo()
        partner = request.env.user.partner_id
        empresarial_group = partner.parent_id.empresarial_group_id

        if empresarial_group:
            list_installed_services = list(installed_services.search([('empresarial_group', '=', empresarial_group.id)]))
        else:
            list_installed_services = list(installed_services.search([('partner_id', '=', partner.parent_id.id)]))

        return list_installed_services
        