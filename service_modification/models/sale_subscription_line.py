# -*- coding: utf-8 -*-

from odoo import models, api, fields

import logging
import pprint

_logger = logging.getLogger(__name__)

class SaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    to_modify = fields.Boolean(string='Modificacion en proceso', default=False)


    @api.onchange('name')
    def _on_change_name_service_modification(self):
        self.service_number.sale_subscription_line.to_modify = False
    