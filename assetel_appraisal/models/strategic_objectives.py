# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 

class StrategicObjectives(models.Model):
    _name = 'strategic.objectives'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Objetivos estrategicos'

    name = fields.Char('Nombre')
    active = fields.Boolean(string="Activo", default=True)
    unidad_de_negocio =  fields.Selection([
        ('Assetel ', 'Assetel'),
        ('LinkSIDE ', 'LinkSIDE'),
        ('BeSIDE', 'BeSIDE'),
        ('CloudSIDE', 'CloudSIDE'),
        ('UpSIDE', 'UpSIDE'),
        ('SmartSIDE', 'SmartSIDE'),
        ('CyberSIDE', 'CyberSIDE')])
    objetivo  = fields.Char(string='Objetivo')
    area  = fields.Char(string='Área')
    descripcion  = fields.Html(string='Descripción')
    
    def name_get(self):
            result = []
            for doc in self:
                if doc.unidad_de_negocio:
                    if doc.objetivo:
                        doc.name = str(doc.unidad_de_negocio) + ' - ' + doc.objetivo
                result.append((doc.id, doc.name))
            return result