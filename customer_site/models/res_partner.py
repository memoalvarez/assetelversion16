# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.modules.module import get_resource_path
import base64

class ResPartner(models.Model):
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('site', 'Sitio')])

    @api.model
    def create(self, vals):
        if vals.get('type') == 'site':
            if not vals.get('image_1920'):
                image_path = get_resource_path('customer_site', 'static/src/img', 'site.jpg')
                vals['image_1920'] = base64.b64encode(open(image_path, 'rb').read())
                
        return super(ResPartner, self).create(vals)
        
        
    def write(self, vals):
        for reg in self:
            if reg.type == 'site':
                if not reg.image_1920:
                    image_path = get_resource_path('customer_site', 'static/src/img', 'site.jpg')
                    reg.image_1920 = base64.b64encode(open(image_path, 'rb').read())
                return super(ResPartner, reg).write(vals)
            else:
                return super(ResPartner, reg).write(vals)
    