# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistorySaleSubscription(models.Model):
    _name = 'history.sale.subscription'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Historial de suscripciones'

    active_sale_subscription = fields.Many2one('sale.subscription', string='Suscripciones')

    modification_date = fields.Datetime("Fecha de guardado")

    display_name = fields.Char('Numero de Suscripcion')
    
    empresarial_group = fields.Char(string="Grupo empresarial")
    partner_id = fields.Char(string="Razón social")
    pricelist_id = fields.Char( string="Tarifa")
    close_reason_id = fields.Char(string="Cerrar Razón")
    date_start = fields.Date(string='Fecha inicial')
    date = fields.Date(string='Fecha final')
    currency_id = fields.Many2one('res.currency', string="Moneda")

    template_id = fields.Char(string="Plantilla de la suscripción")
    user_id = fields.Char(string="Comercial")
    team_id = fields.Char(string="Equipo de ventas")
    corporate_group_id = fields.Char(string="Grupo corporativo")
    company_id = fields.Char(string="Compañía")
    recurring_total = fields.Float(string="Precio recurrente")

    recurring_invoice_line_ids = fields.One2many('history.sale.subscription.line', 'history_sale_subscription_id', string='Apuntes de asientos periodicos')

    code = fields.Char('Referencia')

    def open_subscription(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.subscription",
            "views": [[False, "form"]],
            "res_id": self.active_sale_subscription.id,
            "context": {"create": False},
        }
