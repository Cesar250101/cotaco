# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleado(models.Model):
    _inherit = 'hr.contract'

    trabajo_pesado=fields.Boolean(string='Trabajo Pesado?')
    tipo_comision = fields.Selection(string="Tipo de Comisión",
                                     selection=[('antiguo', 'Metodo Antiguo'), ('nuevo', 'Metodo Nuevo'), ('equipos','Equipos')],
                                     required=False, )


