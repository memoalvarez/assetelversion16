from odoo import models, api, fields, exceptions, _

class AppraisalBehavior(models.Model):
    _name = 'appraisal.behavior'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Conductas'
                
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

    competencia_id = fields.Many2one('expected.behaviors', string="Selecciona")
    comentarios_empleado = fields.Html(string='Comentarios y evidencias')
    comentarios_supervisor = fields.Html(string='Comentarios y evidencias')
    promedio_supervisor = fields.Float(string='Promedio Supervisor')
    promedio_empleado = fields.Float(string='Promedio Empleado')

    #ASIGNAR SUPERVISOR A EMPLEADO
    @api.onchange('competencia_id')
    def _onchange_competencia_id(self):
        for reg in self:
            reg.conducta = reg.competencia_id.conducta
            reg.competencia = reg.competencia_id.competencia
            reg.descripcion = reg.competencia_id.descripcion
            
    conducta = fields.Text(string="Conducta")
    competencia = fields.Text(string="Competencia") 
    descripcion = fields.Html(string='Descripcion')

    conducta_type_empleado = fields.Selection([
    ('deficiente', 'Deficiente'),
    ('aceptable', 'Aceptable'),
    ('satisfactorio', 'Satisfactorio'),
    ('muy_satisfactorio', 'Muy Satisfactorio')
    ], string='Conducta de Actuación')
    
    frecuencia_type_empleado = fields.Selection([
    ('no_presenta', 'No presenta la conducta'),
    ('aveces_p', 'Solo a veces presenta la conducta'),
    ('presenta', 'Presenta la conducta'),
    ('siempre_p', 'Siempre presenta la conducta')
    ], string='Frecuencia')

    conducta_type_supervisor = fields.Selection([
    ('deficiente', 'Deficiente'),
    ('aceptable', 'Aceptable'),
    ('satisfactorio', 'Satisfactorio'),
    ('muy_satisfactorio', 'Muy Satisfactorio')
    ], string='Conducta de Actuación')
    
    frecuencia_type_supervisor = fields.Selection([
    ('no_presenta', 'No presenta la conducta'),
    ('aveces_p', 'Solo a veces presenta la conducta'),
    ('presenta', 'Presenta la conducta'),
    ('siempre_p', 'Siempre presenta la conducta')
    ], string='Frecuencia')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('appraisal.behavior') or _('New')

        result = super(AppraisalBehavior, self).create(vals)
        
        return result
            
