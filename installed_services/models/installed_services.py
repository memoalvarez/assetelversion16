# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class InstalledServices(models.Model):
    _name = 'installed.services'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Número de servicio'

    service_information_ids = fields.One2many('service.information', 'installed_service_id', 'Informacion del servicio')

    name = fields.Char('Numero de servicio', copy=False, index=True, default=lambda self: _('New'))
    stage = fields.Selection([
        ('installed', 'Instalado'),
        ('active', 'Activo'),
        ('discontinued', 'Suspendido'),
        ('disabled', 'Inactivo')
        ], string='Estado', default='installed')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get())
    product_id = fields.Many2one('product.product', string="Servicio", domain=[('sale_ok', '=', True)])
    description = fields.Text(string='Descripcion')
    service_type = fields.Selection([
        ('sae', 'SAE'),
        ('sae_client', 'SAE de cliente'),
        ('connectivity', 'Conectividad'),
        ('cloud', 'Cloud'),
        ('engineering', 'Ingenieria'),
        ('poliza', 'Póliza')
        ], string='Tipo de servicio')
    empresarial_group = fields.Many2one('empresarial.group', string="Grupo empresarial")
    partner_id = fields.Many2one('res.partner', string="Cliente/Empresa")
    razon_social_id = fields.Many2one('res.partner', string="Razón social")
    site = fields.Many2one('res.partner', string="Sitio")

    notes = fields.Html(string='Notas')

    lot_ids = fields.One2many('stock.production.lot', 'service_number', string='Equipos instalados')

    service_price_unit = fields.Float(string='Precio')
    service_vig = fields.Date(string='Vigencia de servicio')
    contrato_vig = fields.Char(string='Contrato Vigente')

    encargado_comercial = fields.Many2one('res.users', string="Encargado comercial")
    ingeniero_asignado = fields.Many2one('res.users', string="Ingeniero asignado")

    installation_type = fields.Selection([
        ('formal', 'Formal'),
        ('cortesia', 'Cortesía'),
        ('temporal', 'Temporal'),
        ('infraestructura', 'Infraestructura')
        ], string='Tipo de instalación')


    def _compute_ticket_ids(self):
        #Se cuentan todos los tickets del servicio actual#
        for reg in self:
            tickets_count = reg.env['helpdesk.ticket'].search_count([['installed_service_id', '=', reg.id]])
            reg.update({
                'ticket_count': tickets_count,
            })

    ticket_count = fields.Integer(string='Tickets count', compute='_compute_ticket_ids')
    ticket_ids = fields.One2many('helpdesk.ticket', 'installed_service_id', string='Historial de tickets')

    def name_get(self):
        result = []
        for doc in self:
            name = doc.name or ''
            if doc.product_id:
                name += ' - ' + doc.product_id.name
            result.append((doc.id, name))
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('installed.services') or _('New')

        result = super(InstalledServices, self).create(vals)

        #Campos para crear registro de configuracion del servicio#
        values = {
            'installed_service_id' : result.id,
            'service_type' : result.service_type
        }

        new = self.env['service.information'].create(values)

        #Campos para crear cuenta analitica
        analytic_account  = {
            'name' : result.name,
            'partner_id' : result.partner_id.id
        }

        new = self.env['account.analytic.account'].create(analytic_account)

        return result


        
    def write(self, values):
        result = super(InstalledServices, self).write(values)

        configuration = self.env['service.information'].search([['installed_service_id', '=', self.id]])

        #SI ENCUENTRA UN REGISTRO DE INFORMACION#
        if configuration:
            #COMPRUEBO DIFERENCIAS Y CAMBIO#
            for record in configuration:
                if record.service_type != self.service_type:
                    record.update({
                        'service_type': self.service_type,
                    })

        else:
            #CREO UN REGISTRO#
            values = {
                'installed_service_id' : self.id,
                'service_type' : self.service_type
            }
            new = self.env['service.information'].create(values)

        return result


    def open_service_configuration(self):
        action = self.env.ref('installed_services.get_service_information_view').read()[0]

        information = self.mapped('service_information_ids')

        if len(information) > 1:
            action['domain'] = [('id', 'in', information.ids)]
        elif information:
            action['views'] = [(self.env.ref('installed_services.service_information_form').id, 'form')]
            action['res_id'] = information.id
            action['target'] = 'new'
        return action


    def action_view_tickets(self):
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]

        tickets = self.mapped('ticket_ids')

        if len(tickets) > 1:
            action['domain'] = [('id', 'in', tickets.ids)]
        elif tickets:
            action['views'] = [(self.env.ref('helpdesk.helpdesk_ticket_view_form').id, 'form')]
            action['res_id'] = tickets.id
        return action


    def new_ticket(self):
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        action['views'] = [(self.env.ref('helpdesk.helpdesk_ticket_view_form').id, 'form')]
        action['context'] = {'default_installed_service_id': self.id, 'default_empresarial_group': self.empresarial_group.id}
        action['target'] = 'current'
        return action


    def suspend_service(self):
        for reg in self:
            reg.stage = 'discontinued'


    def activate_service(self):
        for reg in self:
            reg.stage = 'active'
