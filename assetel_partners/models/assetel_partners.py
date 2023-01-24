# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, api, _ 

class AssetelPartners(models.Model):
    _name = 'assetel.partners'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Partners Assetel'
    
    name = fields.Char('Partner', copy=False, index=True, default=lambda self: _('New'))
    stage_id = fields.Many2one('assetel.partners.stage', string='Etapa', ondelete='restrict', tracking=True, copy=False, index=True, group_expand='_read_group_stage_ids',)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get())

    kanban_state = fields.Selection([
        ('normal', 'Gris'),
        ('done', 'Verde'),
        ('blocked', 'Rojo')], string='Kanban State',
        copy=False, default='normal', required=True)
    color = fields.Integer(string='Color Index')

    stage_sign_in = fields.Selection([
    ('new', 'Nuevo'),
    ('encuesta1', 'Encuesta 1'),
    ('carta_preliminar', 'Carta Preliminar'),
    ('acceso_portal', 'Acceso al portal')
    ], string='Etapa', related='stage_id.stage_sign_in')

    company_name = fields.Char('Empresa')
    partner_id = fields.Many2one('res.partner', string="Cliente")
    partner_name = fields.Char('Nombre')
    email = fields.Char('Correo electrónico')
    phone = fields.Char('Télefono')
    expediente_azul = fields.Char('Expediente azul')
    

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('assetel.partners') or _('New')

        if vals.get('stage_id.stage_sign_in') != 'new':
            vals['stage_id'] = self.env['assetel.partners.stage'].sudo().search([('stage_sign_in', '=', 'new')]).id

        result = super(AssetelPartners, self).create(vals)

        #Busca contacto y si no existe lo crea
        contact = self.env['res.partner'].sudo().search([('email', '=', result.email), ('type', '=', 'contact'), ('is_company', '=', False)])
        
        if contact:
            result.partner_id = contact[0].id
            result.partner_id.number_afiliation = result.id
            result.partner_id.parent_id = False

        else:
            values = {
                'name': result.partner_name,
                'phone': result.phone,
                'email': result.email,
            }
            new_contact = self.env['res.partner'].create(values)

            result.partner_id = new_contact.id
            result.partner_id.number_afiliation = result.id
        
        return result


    def action_view_partner(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "res.partner",
            "views": [[self.env.ref('assetel_partners.partner_view_form').id, "form"]],
            "res_id": self.partner_id.id,
            "context": {"create": False},
        }

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('active', '=', True)]

        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)
    
    
    def _track_template(self, changes):
        res = super(AssetelPartners, self)._track_template(changes)
        test_assetel_partners = self[0]
        if 'stage_id' in changes and test_assetel_partners.stage_id.mail_template_id:
            res['stage_id'] = (test_assetel_partners.stage_id.mail_template_id, {
                'auto_delete_message': False,
                'subtype_id': self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note'),
                'email_layout_xmlid': 'mail.mail_notification_light'
            })
        return res

    #Enviar encuesta
    def new_survey_invite(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "survey.survey",
            "views": [[False, "kanban"]],
            "context": {"afiliacion_id": self.id, "contact_id": self.partner_id.ids},
        }

    def _compute_survey_ids(self):
        #Se cuentan todas las encuestas del ticket actual#
        for reg in self:
            srv_count = reg.env['survey.user_input'].search_count([('afiliacion_id', '=', reg.id)])
            reg.update({
                'survey_count': srv_count,
            })

    survey_count = fields.Integer(string='Survey count', compute='_compute_survey_ids')
    survey_ids = fields.One2many('survey.user_input', 'afiliacion_id', string='Encuestas cliente')


    def action_view_surveys(self):
        self.ensure_one()
        surveys = self.mapped('survey_ids')

        if len(surveys) > 1:
            action = self.env.ref('survey.action_survey_user_input').read()[0]
            action['domain'] = [('id', 'in', surveys.ids)]
            action['context'] = dict(create=False)
            return action

        elif surveys:
            return {
                "type": "ir.actions.act_window",
                "res_model": "survey.user_input",
                "views": [[False, "form"]],
                "res_id": surveys.id,
                "context": {"create": False},
            }
        
    def new_carta_preliminar(self):        
        return {
            "type": "ir.actions.act_window",
            "res_model": "sign.template",
            "views": [[False, "kanban"]],
            "context": {"afiliacion_id": self.id, "contact_id": self.partner_id.id},
        }   
    
    #CONTEO DE CARTA PRELIMINAR Y REDIRECCION A ELLAS
    def _compute_sign_request_ids(self):
        #Se cuentan todas las solicitudes de firma#
        for reg in self:
            sign_count = reg.env['sign.request'].search_count([['afiliacion_id', '=', reg.id]])
            reg.update({
                'sign_request_count': sign_count,
            })
    sign_request_count = fields.Integer(string='Sign request count', compute='_compute_sign_request_ids')
    sign_request_ids = fields.One2many('sign.request', 'afiliacion_id', string='Solicitudes de firma')
    
    def action_view_sign_request(self):
        self.ensure_one()
        sign = self.mapped('sign_request_ids')

        if len(sign) > 1:
            action = self.env.ref('sign.sign_request_action').read()[0]
            action['domain'] = [('id', 'in', sign.ids)]
            return action

        elif sign:
            return {
                "type": "ir.actions.act_window",
                "res_model": "sign.request",
                "views": [[False, "form"]],
                "res_id": sign.id,
            }