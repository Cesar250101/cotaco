# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class Cheque(models.Model):
    _inherit = 'account.payment'

class CuentaExcepcionVenta (models.Model):

    _inherit = 'account.account'

    valida_excepcion = fields.Boolean(string='Valida Excepción Venta')
    es_fondo_rendir = fields.Boolean(string='Es para fondos x Rendir')

class PeriodoLibro(models.Model):
    _name = 'cotaco.periodo.libro'
    _rec_name = 'name'
    _description = 'Periodos en facturas para la emisión del los libros de compra y venta'

    name = fields.Char(string="Periodo Libro")
    active = fields.Boolean(string="Activo?",  )


class Facturas(models.Model):
    _inherit = 'account.invoice'

    periodo_libro = fields.Many2one(comodel_name="cotaco.periodo.libro", string="Periodo del Libro", required=False, )
    valor_flete = fields.Integer(string="Valor Flete")



    @api.onchange('date_invoice')
    def _obtener_periodo(self):
        # fecha=str(self.date_invoice)
        # objfecha = datetime.strptime(fecha,'%y-%m-%d')
        # año=objfecha.year
        # mes=objfecha.month
        # strmes="00" + str(mes)
        # strmes=strmes[-2:]
        # periodo=str(año)+str(mes)
        self.periodo="201906"



class ComprobantesContables(models.Model):
    _inherit = 'account.move'

    tipo_comprobante = fields.Selection(string="Tipo de Comprobante", selection=[('Egreso', 'Egreso'), ('Ingreso', 'Ingreso'),('Traspaso', 'Traspaso'), ], required=True,default='Traspaso' )

class ComprobantesContables(models.Model):
    _inherit = 'account.payment.order'

    tipo_comprobante = fields.Selection(string="Tipo de Comprobante", selection=[('Egreso', 'Egreso'), ('Ingreso', 'Ingreso'),('Traspaso', 'Traspaso'), ], required=True,default='Egreso' )

    @api.model
    def generate_move(self):
        res = super(ComprobantesContables, self).generate_move()
        asientos=self.env['account.move'].search([('id','=',self.move_ids.id)])
        for i in asientos:
            i.tipo_comprobante=self.tipo_comprobante

class RendicionGastos(models.Model):
    _inherit = 'hr.expense'

    fondo_pendiente=fields.Char(string='Fondo x Rendir',compute='_Obtener_Fondo')

    @api.one
    @api.depends('employee_id')
    def _Obtener_Fondo(self):
        domain = [
            ('es_fondo_rendir', '=', True),
        ]
        cuentas_fondos_pendientes=self.env['account.account'].search(domain)
        cuentas = []
        for reg in cuentas_fondos_pendientes:
            cuentas.append(reg.id)

        domain = [
            ('account_id', 'in', cuentas),
            ('partner_id', '=', self.employee_id.address_home_id.id),
            ('reconciled', '=', False),
            ('move_id.state', '=', 'posted'),
            ('debit', '>', 0),
        ]

        fondos_pendientes=self.env['account.move.line'].search(domain)
        str_fondos_rendir=''
        for r in fondos_pendientes:
            if str(r.debit):
                str_fondos_rendir+='Fecha :' + str(r.date)+': Monto :'+ str(r.debit)+ ' - '

        self.fondo_pendiente=str_fondos_rendir