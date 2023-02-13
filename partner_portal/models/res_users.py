# -*- coding: utf-8 -*-

from odoo import models, api, fields

class ResUsers(models.Model):
    _inherit = 'res.users'



    def _is_partner(self):
        self.ensure_one()

        if self.partner_id.grade_id.id:
            return True
        else:
            return False

    def _get_user_id(self):
        name = self.sudo().env['crm.team'].search([('sequence', '=', 0)])
        return name.user_id.partner_id.name

    def _get_phone(self):
        phone = self.sudo().env['crm.team'].search([('sequence', '=', 0)])
        return phone.user_id.partner_id.phone


    def _get_email(self):
        email = self.sudo().env['crm.team'].search([('sequence', '=', 0)])
        return email.user_id.partner_id.email

    def _get_image(self):
        image = self.sudo().env['crm.team'].search([('sequence', '=', 0)])
        return image.user_id.partner_id.image_1920

    def _is_silver(self):
        if self.sudo().partner_id.partner_weight >= 0 and  self.sudo().partner_id.partner_weight <= 33:
            return True
        else:
            return False

    def _is_golden(self):
        if self.sudo().partner_id.partner_weight >= 34 and  self.sudo().partner_id.partner_weight <= 66:
            return True
        else:
            return False

    def _is_platinum(self):
        if self.sudo().partner_id.partner_weight >= 67 and  self.sudo().partner_id.partner_weight <= 100:
            return True
        else:
            return False

    def _get_conteo_lead(self):
        leads_count = self.sudo().env['crm.lead'].search_count([('partner_assigned_id', '=', self.sudo().partner_id.id)])
        return leads_count

    
