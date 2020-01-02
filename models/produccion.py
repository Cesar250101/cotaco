# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ListaMateriales(models.Model):
    _inherit = 'mrp.bom.line'

    densidad = fields.Float(string="Densidad", related="product_id.densidad" ,required=False, readonly=True )
    #qty_kilos = fields.Float(string="Cantidad Kilos",  required=False, )

    #@api.onchange('qty_kilos')
    #def _onchange_qty_kilos(self):
    #    self.product_qty=self.densidad*self.qty_kilos


class Produccion(models.Model):
    _inherit = 'mrp.workorder'

    @api.model
    def record_production(self):
        res = super(Produccion, self).record_production()
        nrolote=self.env['stock.production.lot'].search([])[-1].name
        nrolote+=1
        for i in nrolote:
            self.final_lot_id=nrolote

class NewModule(models.Model):
    _inherit = 'mrp.bom'

    nro_formula = fields.Char(string='Nro. Formula')
    version_formula = fields.Char(string='Versión Formula')

