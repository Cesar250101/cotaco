# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Usuarios(models.Model):
    _inherit = 'res.users'

    aprueba_muestras = fields.Boolean(string="Aprueba Muestras")

