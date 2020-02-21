# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Lotes(models.Model):
    _inherit = 'stock.production.lot'

    barcode = fields.Char(string="Código de Barra", required=False, compute="_compute_barcode")

    @api.one
    @api.depends('name')
    def _compute_barcode(self):
        codigobarra=self.product_id.product_tmpl_id.default_code+self.name
        self.barcode=codigobarra


