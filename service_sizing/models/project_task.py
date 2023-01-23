# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    sizing_task = fields.Boolean(string='Tarea de dimensionamiento', default=False)
    
    lead_id = fields.Many2one('crm.lead', string='Oportunidad')
    attached_document = fields.Many2many('ir.attachment', string='Documento en extenso')   
    servicio_factible = fields.Boolean(string='Servicio factible', default=False)
    estudio_completado = fields.Boolean(string='Estudio completado', default=False)

    @api.model
    def create(self, vals):
        result = super(ProjectTask, self).create(vals)

        if result.sizing_task:
            result.name = '(#' + str(result.id) + ') - ' + result.name

            text = '''<div style="margin: 0px; padding: 0px;">
                <p style="margin: 0px; padding: 0px; font-size: 13px;">
                    Buen día,
                    <br/><br/>
                    Se ha creado una nueva tarea de dimensionamiento:
                    <br/><br/>
                    Proyecto: ''' + str(result.project_id.name) + '''
                    <br/>
                    Nombre: ''' + str(result.name) + '''
                    <br/>
                    Oportunidad: ''' + str(result.lead_id.name) + '''
                    <br/>
                    Cliente: ''' + str(result.partner_id.name) + '''
                    <br/>
                    Descripción: ''' + str(result.description) + '''
                    <br/><br/>
                    Saludos.
                </p>'''

            for line in result.project_id.users_to_notify:
                result.message_post(body=text, partner_ids=[line.partner_id.id])
        
        return result

    def action_view_lead(self):
        action = self.env.ref('crm.crm_lead_action_pipeline').read()[0]

        if self.lead_id:
            action['views'] = [(self.env.ref('crm.crm_lead_view_form').id, 'form')]
            action['res_id'] = self.lead_id.id
        return action

    def set_factible(self):
        
        self.servicio_factible = True
        self.estudio_completado = True


    def set_no_factible(self):
        self.servicio_factible = False
        self.estudio_completado = True