# -*- coding: utf-8 -*-

from odoo import models, fields, api

class empleado(models.Model):
    _inherit = 'hr.contract'

    trabajo_pesado=fields.Boolean(string='Trabajo Pesado?')


