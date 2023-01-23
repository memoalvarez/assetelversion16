# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class PartnerPortal(http.Controller):
    @http.route(['/my/partner'], type='http', auth="public", website=True)
    def partner_portal(self, **post):
        return request.render("partner_portal.partner_portal_website", {})

        