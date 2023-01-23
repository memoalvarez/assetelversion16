# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HistoryServiceLot(models.Model):
    _name = 'history.service.lot'
    _description = 'Historial de lotes en número de servicio'

    name = fields.Char('Lote/N° de serie')
    product_id = fields.Many2one('product.product', string="Producto")

    history_service_number = fields.Many2one('history.installed.services', string='Historia de numero de servicio')
