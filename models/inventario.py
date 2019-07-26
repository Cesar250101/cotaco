# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT



class SeguimientoDespacho(models.Model):
    _inherit = 'stock.picking'

    status_despacho_id = fields.Many2one(comodel_name="cotaco.status.despacho", string="Status de Despacho", required=False, )
    observacion = fields.Char(string="Observación", required=False, )


class StatusDespacho(models.Model):
    _name = 'cotaco.status.despacho'

    name = fields.Char(string="Status de Despacho", required=False, )
