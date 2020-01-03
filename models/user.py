# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Usuarios(models.Model):
    _inherit = 'res.users'
    #_rec_name = 'display_name'
    aprueba_muestras = fields.Boolean(string="Aprueba Muestras")
    #es_cobrador = fields.Boolean(string="Es Cobrador?")
