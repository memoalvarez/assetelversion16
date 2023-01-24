# -*- coding: utf-8 -*-

from odoo import models, api, fields

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    mail_template_id = fields.Many2one(
        'mail.template', 'Plantilla de correo electrónico', domain="[('model', '=', 'crm.lead')]",
        help="Automated email sent to the ticket's customer when the ticket reaches this stage.")

