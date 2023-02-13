# -*- coding: utf-8 -*-
from odoo import models, api, fields, exceptions, _
from odoo.exceptions import ValidationError

class AppraisalSmart(models.Model):
    _name = 'appraisal.smart'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Objetivos smart'
                
    appraisal_period_id = fields.Many2one('appraisal.period', string='Evaluaciones')

    name = fields.Char('Nombre', copy=False, index=True, default=lambda self: _('New'))
    stage = fields.Selection([
        ('new', 'Nuevo'),
        ('aprobacion', 'Aprobación'),
        ('proceso', 'Proceso'),
        ('evaluacion', 'Evaluación'),
        ('cerrado', 'Cerrado')
        ], string='Estado', related='appraisal_period_id.stage')

    employee_status = fields.Selection([
        ('empleado', 'Empleado'),
        ('supervisor', 'Supervisor'), 
        ('visitante', 'Visitante')], related='appraisal_period_id.employee_status')

    objetivo_estrategico = fields.Many2one('strategic.objectives', string="Objetivo Estrategico")
    objetivo = fields.Text(string="Objetivo")
    ponderacion = fields.Integer(string="Ponderación")
    date_start = fields.Date(string='Fecha inicio')
    date_end = fields.Date(string='Fecha Fin')

    resultado_esperado = fields.Float(string="Resultado Esperado")
    resultado_sugerido = fields.Float(string='Resultado Sugerido')
    resultado_obtenido = fields.Float(string="Resultado Obtenido")

    comentarios_empleado = fields.Html(string='Comentarios y evidencias')
    comentarios_supervisor = fields.Html(string='Comentarios y evidencias')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('appraisal.smart') or _('New')
            
            result = super(AppraisalSmart, self).create(vals)
            
        return result

    #ONCHANGE SOBRE CAMPOS DE FECHA INICIAL
    @api.onchange('date_start', 'date_end')
    def onchange_date_start(self):
        #CAMBIOS EN FECHA INICIAL
        if self.date_start and self.appraisal_period_id.date_start and self.appraisal_period_id.date_end:
            start_date = self.date_start.strftime('%Y-%m-%d')
            period_date_start = self.appraisal_period_id.date_start.strftime('%Y-%m-%d')
            period_date_end = self.appraisal_period_id.date_end.strftime('%Y-%m-%d')
            if start_date < period_date_start:
                raise ValidationError(_('La fecha inicial esta fuera del rango'))
            if start_date > period_date_end:
                raise ValidationError(_('La fecha inicial esta fuera del rango'))
            if self.date_end:
                end_date = self.date_end.strftime('%Y-%m-%d')
                if start_date >= end_date:
                    raise ValidationError(_('La fecha inicial no puede ser mayor o igual a la final'))
        #CAMBIOS EN FECHA FINAL
        if self.date_end and self.appraisal_period_id.date_start and self.appraisal_period_id.date_end:
            end_date = self.date_end.strftime('%Y-%m-%d')
            period_date_start = self.appraisal_period_id.date_start.strftime('%Y-%m-%d')
            period_date_end = self.appraisal_period_id.date_end.strftime('%Y-%m-%d')
            if end_date < period_date_start:
                raise ValidationError(_('La fecha final esta fuera del rango'))
            if end_date > period_date_end:
                raise ValidationError(_('La fecha final esta fuera del rango'))
            if self.date_start:
                start_date = self.date_start.strftime('%Y-%m-%d')
                if end_date <= start_date:
                    raise ValidationError(_('La fecha final no puede ser menor o igual a la inicial'))
            
    