# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AssetelPartnersStage(models.Model):
    _name = 'assetel.partners.stage'
    _description = 'Etapas de modelo assetel.partners'
    _order = 'sequence, id'

    name = fields.Char('Nombre de la etapa', required=True, translate=True)
    description = fields.Text(translate=True)

    sequence = fields.Integer('Secuencia', default=10)
    active = fields.Boolean('Activo', default=True)
    fold = fields.Boolean(
        'Doblado en Kanban', help='This stage is folded in the kanban view when there are no records in that stage to display.')

    mail_template_id = fields.Many2one(
        'mail.template', 'Plantilla de correo electrónico', domain="[('model', '=', 'assetel.partners')]",
        help="Automated email sent to the ticket's customer when the ticket reaches this stage.")
        
    legend_blocked = fields.Char(
        'Red Kanban Label', default=lambda s: _('Bloqueada'), translate=True, required=True,
        help='Override the default value displayed for the blocked state for kanban selection, when the task or issue is in that stage.')
    legend_done = fields.Char(
        'Green Kanban Label', default=lambda s: _('Listo para la siguiente etapa'), translate=True, required=True,
        help='Override the default value displayed for the done state for kanban selection, when the task or issue is in that stage.')
    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('En progreso'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    
    stage_sign_in = fields.Selection([
    ('new', 'Nuevo'),
    ('encuesta1', 'Encuesta 1'),
    ('carta_preliminar', 'Carta Preliminar'),
    ('acceso_portal', 'Acceso al portal')
    ], string='Función de etapa')
    