# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Armado(models.Model):
    _inherit = 'account.payment.order'

    cobrador = fields.Many2one(comodel_name="res.users", string="Cobrador", required=False,)


