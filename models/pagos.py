# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Armado(models.Model):
    _inherit = 'account.payment.order'

    cobrador = fields.Many2one(comodel_name="cotaco.cobradores", string="Cobrador", required=False,)

class Cobradores(models.Model):
    _name = 'cotaco.cobradores'
    _rec_name = 'name'
    _description = 'Tabla de cobradores'

    name = fields.Char(string="Nombre")
    user_id = fields.Many2one(comodel_name="res.users", string="Usuario Relacionado", required=False, )




