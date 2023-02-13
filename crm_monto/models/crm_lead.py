from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    montoRetencion = fields.Monetary('Monto Retencion', currency_field='company_currency')
