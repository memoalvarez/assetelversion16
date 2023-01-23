# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AppraisalPeriod(models.Model):
    _name = 'appraisal.period'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Evaluaciones Assetel'
    
    name = fields.Char('Nombre', copy=False, index=True, default=lambda self: _('New'))
    stage = fields.Selection([
        ('new', 'Nuevo'),
        ('aprobacion', 'Aprobación'),
        ('proceso', 'Proceso'),
        ('evaluacion', 'Evaluación'),
        ('cerrado', 'Cerrado')
        ], string='Estado', default='new')
    color = fields.Integer(string='Color Index')

    empleado = fields.Many2one('hr.employee', string="Empleado")
    date_start = fields.Date(string='Fecha inicio')
    date_end = fields.Date(string='Fecha Fin')

    comentario_empleado = fields.Html(string='Comentario empleado')
    firma_empleado = fields.Binary("Firma empleado")

    comentario_general = fields.Html(string='Comentario supervisor')
    firma_supervisor = fields.Binary("Firma supervisor")

    appraisal_smart_lines = fields.One2many('appraisal.smart', 'appraisal_period_id', string='Objetivos smart')
    
    calificacion_smart = fields.Float(string='Calificación de objetivos smart')
    calificacion_behavior = fields.Float(string='Calificacion de conductas')

    

    approver_ids = fields.One2many('appraisal.approver', 'request_id', string="Approvers", check_company=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get())
    apprisal_activity_id = fields.Many2one('mail.activity', string='Actividad de Evaluación')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].sudo().next_by_code('appraisal.period') or _('New')

        result = super(AppraisalPeriod, self).create(vals)

        #AGREGAR SUPERVISOR Y EMPLEADO DE SEGUIDORES
        subtype_id = self.sudo().env['mail.message.subtype'].search([('id','=', 1)])

        if self.empleado.address_home_id:
            follower = {
                'res_id': result.id,
                'res_model': 'appraisal.period',
                'partner_id': self.empleado.address_home_id.id,
                'subtype_ids': subtype_id,
            }
            follower_creation = self.sudo().env['mail.followers'].create(follower)

        if self.supervisor.address_home_id:
            follower = {
                'res_id': result.id,
                'res_model': 'appraisal.period',
                'partner_id': self.supervisor.address_home_id.id,
                'subtype_ids': subtype_id,
            }
            follower_creation = self.sudo().env['mail.followers'].create(follower)

        return result


    @api.depends('approver_ids.status')
    def _compute_user_status(self):
        for approval in self:
            approval.user_status = approval.approver_ids.filtered(lambda approver: approver.user_id == self.env.user).status

    user_status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancel')], compute="_compute_user_status")

    #ASIGNAR SUPERVISOR A EMPLEADO
    @api.onchange('empleado')
    def _onchange_empleado(self):
        for reg in self:
            reg.supervisor = reg.empleado.parent_id.id
            
    supervisor = fields.Many2one('hr.employee', string="Supervisor")
            
    #SOLICITAR APROBACIÓN
    def action_approval_request(self):        
        #COMPRUEBA QUE LA PONDERACION DE 100 PUNTOS
        sumPonderacion = 0
        for line in self.appraisal_smart_lines:
            sumPonderacion += line.ponderacion
        if sumPonderacion < 100:
            raise ValidationError(_('La ponderacion debe ser 100'))
        else:
        #CAMBIA DE ETAPA A APROBACIÓN
            approvers = self.mapped('approver_ids').filtered(lambda approver: approver.status == 'new')
            approvers._create_activity()
            approvers.write({'status': 'pending'})
            self.stage = 'aprobacion'
        

    #TOMA TIPO DE ACTIVIDAD DE APROBACION PARA EVALUACIONES
    def _get_user_approval_activities(self, user):
        domain = [
            ('res_model', '=', 'appraisal.period'),
            ('res_id', 'in', self.ids),
            ('activity_type_id', '=', self.env.ref('assetel_appraisal.mail_activity_data_appraisal_approval').id),
            ('user_id', '=', user.id)
        ]
        activities = self.env['mail.activity'].search(domain)
        return activities


    #APROBAR
    def action_approve(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'approved'})
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()
        self.message_post(body="<span class='fa fa-thumbs-o-up fa-fw'></span> Solicitud aprobada")
        self.stage = 'proceso'

    #RECHAZAR
    def action_refuse(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'new'})
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()
        self.message_post(body="<span class='fa fa-thumbs-o-down fa-fw'></span> Solicitud rechazada")
        self.stage = 'new'


    #SOBREESCRIBE CAMPO approver_ids PARA PONER AL APROBADOR
    @api.onchange('supervisor')
    def _onchange_supervisor(self):
        if self.supervisor:
            for record in self.approver_ids:
                    self.write({'approver_ids': [(2,record.id)]}) 
            values = {
                'user_id':self.supervisor.user_id.id,
                'status': 'new',
                'request_id': self.id,
            }
            new_line = self.env['appraisal.approver'].create(values)

    @api.depends('appraisal_smart_lines.resultado_obtenido', 'appraisal_behavior_lines.conducta_type_supervisor', 'appraisal_behavior_lines.frecuencia_type_supervisor')
    def _compute_calificacion(self):
        for period in self:
            #Calificacion Objetivos
            sumPromedio = 0
            count = 0
            for line in period.appraisal_smart_lines:
                sumPromedio += line.resultado_obtenido
                count += 1

            if count > 0:
                period.update({
                    'calificacion_smart': sumPromedio/count
                })

            #Calificacion competencias
            sum = 0
            count = 0
            frecuencia = 0
            frecuenciaEmp = 0
            conducta = 0
            conductaEmp = 0
            #PROMEDIO SUPERVISOR
            for line in period.appraisal_behavior_lines:
                if line.conducta_type_supervisor == 'deficiente':
                    conducta = 25
                if line.conducta_type_supervisor == 'aceptable':
                    conducta = 50
                if line.conducta_type_supervisor == 'satisfactorio':
                    conducta = 75
                if line.conducta_type_supervisor == 'muy_satisfactorio':
                    conducta = 100
                if line.frecuencia_type_supervisor == 'no_presenta':
                    frecuencia = 25
                if line.frecuencia_type_supervisor == 'aveces_p':
                    frecuencia = 50
                if line.frecuencia_type_supervisor == 'presenta':
                    frecuencia = 75
                if line.frecuencia_type_supervisor == 'siempre_p':
                    frecuencia = 100
                sum += (conducta + frecuencia)/2
                #PROMEDIO EMPLEADO
                if line.conducta_type_empleado == 'deficiente':
                    conductaEmp = 25
                if line.conducta_type_empleado == 'aceptable':
                    conductaEmp = 50
                if line.conducta_type_empleado == 'satisfactorio':
                    conductaEmp = 75
                if line.conducta_type_empleado == 'muy_satisfactorio':
                    conductaEmp = 100
                if line.frecuencia_type_empleado == 'no_presenta':
                    frecuenciaEmp = 25
                if line.frecuencia_type_empleado == 'aveces_p':
                    frecuenciaEmp = 50
                if line.frecuencia_type_empleado == 'presenta':
                    frecuenciaEmp = 75
                if line.frecuencia_type_empleado == 'siempre_p':
                    frecuenciaEmp = 100
                line.promedio_supervisor = (conducta + frecuencia)/2
                line.promedio_empleado = (conductaEmp + frecuenciaEmp)/2
                count += 1

            if count > 0:
                period.update({
                    'calificacion_behavior': sum/count,
                })

                

            period.update({
                'calificacion_general': (period.calificacion_smart + period.calificacion_behavior) /2
            })


    calificacion_general = fields.Float(string='Calificación general', compute='_compute_calificacion')



    #BOTON QUE ENVIA A EVALUACIÓN
    def action_enviar_evaluacion(self):
        self.stage = 'evaluacion'

        #CREACION DE ACTIVIDAD "POR HACER"
        model_id = self.env['ir.model']._get(self._name).id
        activity_id = self.env['mail.activity.type'].search([['name', '=', 'Por hacer']])

        vals = {
            'res_model' : "appraisal.period",
            'res_model_id' : model_id,
            'res_id' : self.id,
            'summary' : "Evaluar Objetivos",
            'activity_type_id' : activity_id.id,
            'user_id' : self.supervisor.user_id.id,
        }
        new_activity = self.env['mail.activity'].create(vals)
        self.apprisal_activity_id = new_activity.id


    #REGRESAR A NUEVO
    def action_return_new(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'new'})
        self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()
        self.message_post(body="<span class='fa fa-arrows-h fa-fw'></span> Se regreso evaluación a estado Nuevo")
        self.stage = 'new'

    #REGRESAR A PROCESO
    def action_return_proceso(self, approver=None):
        self.apprisal_activity_id.action_feedback(feedback="Se regreso evaluación a estado Proceso")
        self.stage = 'proceso'

    #REGRESAR A EVALUACION
    def action_return_evaluacion(self, approver=None):
        self.message_post(body="<span class='fa fa-arrows-h fa-fw'></span> Se regreso evaluación a estado Evaluación")
        self.stage = 'evaluacion'


    #BOTON QUE CIERRA LA EVALUACIÓN
    def action_cerrar_evaluacion(self):
        self.stage = 'cerrado'
        self.apprisal_activity_id.action_feedback(feedback="Objetivos Evaluados")

    #ONCHANGE PARA AGREGAR Y ELIMINAR LINEAS EN COMPETENCIAS
    @api.depends('empleado')
    def _compute_appraisal_behavior_lines(self):
        for line in self.appraisal_behavior_lines:
            self.write({'appraisal_behavior_lines': [(2,line.id)]})
        conductas = self.env['expected.behaviors'].search([['active', '=', True]])
        for comp in conductas:
            for emp in comp.behaviors_empleados:
                if emp == self.empleado:
                    values = {
                        'appraisal_period_id': self.id,
                        'competencia_id': comp.id,
                        'competencia': comp.competencia,
                        'conducta': comp.conducta,
                        'descripcion': comp.descripcion,
                    }
                    conducta_creation = self.sudo().env['appraisal.behavior'].create(values)

    appraisal_behavior_lines = fields.One2many('appraisal.behavior', 'appraisal_period_id', string='Competencias', store=True, compute="_compute_appraisal_behavior_lines")
    
        
    #ENVIAR CORREO
    def action_report_send(self):
        self.ensure_one()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('assetel_appraisal.email_template_installed_services', raise_if_not_found=False)
        lang = self.env.context.get('lang') 
        template = self.env['mail.template'].browse(template_id)

        if template.lang:
            lang = template._render_template(template.lang, 'appraisal.period', self.ids[0])
        ctx = {
            'default_model': 'appraisal.period',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'custom_layout': "assetel_appraisal.template_appraisal_period",
            'force_email': True,
            'model_description': "Evaluacion",
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    #OBTENER USUARIO LOGGEADO

    @api.depends('empleado')
    def _compute_get_employee(self):
        for reg in self:
            employee = reg.env['hr.employee'].search([('user_id','=', reg.env.user.id)])
            self.update({
                    'current_employee': employee.id
                })
                
    current_employee = fields.Many2one('hr.employee','Current Employee', compute='_compute_get_employee')



    @api.depends('current_employee')
    def _compute_employee_status(self):
        for reg in self:
            if reg.empleado.id == reg.current_employee.id:
                reg.employee_status = 'empleado'
            elif reg.supervisor.id == reg.current_employee.id: 
                reg.employee_status = 'supervisor'
            else:
                reg.employee_status = 'visitante'


    employee_status = fields.Selection([
        ('empleado', 'Empleado'),
        ('supervisor', 'Supervisor'), 
        ('visitante', 'Visitante')], compute="_compute_employee_status")

