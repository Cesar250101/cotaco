# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrdenCompra(models.Model):
    _inherit = 'purchase.order'

    cuentas_analiticas = fields.Many2one(string='Cuentas Analiticas', related='order_line.account_analytic_id')
