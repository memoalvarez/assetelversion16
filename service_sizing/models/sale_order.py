# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields, exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):

        for so in self:
            for linea in so.order_line:
                if linea.product_uom_qty:
                    if linea.site:
                        pass
                    else:
                        if so.opportunity_id:
                            raise exceptions.ValidationError('Te falta el sitio en alguna línea de pedido')

        for so in self:
            if so.opportunity_id:
                if so.opportunity_id.sizing_task_ids:

                    so_ok = False

                    for dim in so.opportunity_id.sizing_task_ids:
                        if dim.stage_id.end_sizing == True:
                            so_ok = True

                    if so_ok:
                        res = super(SaleOrder, self).action_confirm()
                        return res
                    else:
                        raise exceptions.ValidationError('El dimensionamiento de tu oportunidad debe estar terminado')

                else:
                    raise exceptions.ValidationError('Debes tener un dimensionamiento desde la oportunidad para confirmar tu presupuesto')

            else:
                res = super(SaleOrder, self).action_confirm()
                return res

