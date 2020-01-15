# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Armado(models.Model):
    _inherit = 'qc.test'

    nombre_completo = fields.Char(string='Categoria',related="category.complete_name")
    dias_duracion_producto = fields.Integer(string="Días de duración", required=False, )
    nu = fields.Char(string='Nu')
    clase = fields.Char(string='Clase')
    salud = fields.Integer(string='Salud')
    inflamable = fields.Integer(string='Inflamable')
    reactividad = fields.Integer(string='Reactividad')
    especial = fields.Integer(string='Especial')