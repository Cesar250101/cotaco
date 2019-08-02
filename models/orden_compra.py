# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class OrdenCompra(models.Model):
    _inherit = 'purchase.order'

    cuentas_analiticas = fields.Many2one(string='Cuentas Analiticas', related='order_line.account_analytic_id')
