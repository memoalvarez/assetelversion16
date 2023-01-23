# -*- coding: utf-8 -*-

from odoo import models, api, fields
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'
    mail_text = fields.Html(string='Texto Correo electronico')

    #ENVIAR CORREO
    def action_report_send(self):
        self.ensure_one()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('assetel_followup.email_followup_res_partner', raise_if_not_found=False)
        lang = self.env.context.get('lang') 
        template = self.env['mail.template'].browse(template_id)

        if template.lang:
            lang = template._render_template(template.lang, 'res.partner', self.ids[0])
        ctx = {
            'default_model': 'res.partner',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "assetel_followup.template_followup",
            'force_email': True,
            'model_description': "Cobranza",
        }
        #Buscamos facturas
        facturas = self.env['account.move'].search([['partner_id', '=', self.id], ['state', '=', 'posted']])
        #Comenzamos con la creación de la tabla
        text = '<table style ="font-family: arial, sans-serif;border-collapse: collapse;width: 100%;font-size: 13px;"><tr><th style="border: 1px solid #dddddd;">Folio</th><th style="border: 1px solid #dddddd;">Fecha de Factura</th><th style="border: 1px solid #dddddd;">Fecha de vencimiento</th><th style="border: 1px solid #dddddd;">Total Factura<th style="border: 1px solid #dddddd;">Importe adeudado<th style="border: 1px solid #dddddd;">Estado</th><th style="border: 1px solid #dddddd;">Fecha de pago</th></th></tr>'
        #Obtenemos la fecha de hoy
        today = datetime.now()
        adeudado = 0
        pagar = 0
        #Recorremos todas las facturas
        for factura in facturas:
            #Solo recorremos facturas de cliente
            if factura.type == 'out_invoice':
                #Formato a numeros
                total_factura_format = f'{factura.amount_total_signed:,}'
                importe_adeudado_format = f'{factura.amount_residual_signed:,}'
                #Llenamos el contenido de la tabla
                text = text + '<tr><td style="border: 1px solid #dddddd;">'+  str(factura.name) +'</td><td style="border: 1px solid #dddddd;">'+  str(factura.invoice_date) +'</td><td style="border: 1px solid #dddddd;">'+  str(factura.invoice_date_due) +'</td><td style="border: 1px solid #dddddd;">' + str(factura.currency_id.name) + str(total_factura_format) +'</td><td style="border: 1px solid #dddddd;">' + str(factura.currency_id.name) + str(importe_adeudado_format) +'</td>'
                #Asignamos valor a Estado
                if factura.amount_residual == 0:
                    text = text + '<td style="border: 1px solid #dddddd;">Pagado</td>'
                elif factura.invoice_date_due.strftime('%Y-%m-%d') < str(today):
                    pagar = pagar + factura.amount_residual
                    text = text + '<td style="border: 1px solid #dddddd;">Vencido</td>'
                else:
                    text = text + '<td style="border: 1px solid #dddddd;">Vigente</td>'
                #Asignamos valor de la fecha de pago
                if factura.invoice_payments_widget:
                    #Obtenemos la posición de date
                    date_position = factura.invoice_payments_widget.find('date')
                    if date_position >= 0:
                        fecha = factura.invoice_payments_widget[date_position + 8: date_position + 18]
                        text = text + '<td style="border: 1px solid #dddddd;">'+  str(fecha) +'</td>'
                    else:
                        text = text + '<td style="border: 1px solid #dddddd;">No pagada</td>'
                        #if factura.invoice_date_due.strftime('%Y-%m-%d') < str(today):
                            #pagar = pagar + factura.amount_residual

                text = text + '</tr>'
                adeudado = adeudado + factura.amount_residual
                adeudado_2dec =  round(adeudado, 2)
                pagar_2dec =  round(pagar, 2)
                adeudado_format = f'{adeudado_2dec:,}'
                pagar_format = f'{pagar_2dec:,}'
        text = text + '</table></br>'
        text = text + '<p></br><strong>TOTAL ADEUDADO: </strong>' + str(factura.currency_id.name) + str(adeudado_format) + '  </p></br>'
        text = text + '<p><strong>TOTAL A PAGAR: </strong>' + str(factura.currency_id.name) + str(pagar_format) + '</p></br>'

        self.mail_text = text

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        