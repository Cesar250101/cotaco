# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Armado(models.Model):
    _inherit = 'mrp.repair'

    orden_venta = fields.Many2one(comodel_name="sale.order", string="Nota de Venta", required=False, )


