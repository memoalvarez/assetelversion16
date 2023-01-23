# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ExpectedBehaviors(models.Model):
    _name = 'expected.behaviors'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Conductas y Competencias Assetel'

    appraisal_period_id = fields.Many2one('appraisal.period', string='Evaluaciones')

    behaviors_empleados = fields.Many2many('hr.employee', string='Empleados')

    name = fields.Char('Nombre')
    conducta = fields.Text(string="Conducta")
    competencia = fields.Text(string="Competencia")
    descripcion = fields.Html(string='Descripcion')
    active = fields.Boolean(string="Activo", default=True)

    def name_get(self):
            result = []
            for doc in self:
                if doc.competencia:
                    if doc.conducta:
                        doc.name = str(doc.competencia) + ' - ' + doc.conducta
                result.append((doc.id, doc.name))
            return result