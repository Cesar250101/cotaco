# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class NewModule(models.Model):
    _inherit = 'stock.picking.type'

    is_project = fields.Boolean(string="Es para Proyecto",  )


class NewModule(models.Model):
    _inherit = 'stock.move'

    codigo_mp = fields.Text(string="Materia Prima", related='product_id.product_tmpl_id.description')
    analytic_account_id = fields.Many2one(string='Analytic Account',comodel_name='account.analytic.account',
                                          related="picking_id.analytic_account_id")


class Lote(models.Model):
    _inherit = 'stock.move.line'

    lote_leido = fields.Char(string="Lote Scaneado", required=False, )

    @api.one
    @api.constrains('lote_leido')
    def _check_lote(self):
        if self.lot_id.name!=self.lote_leido:
            raise ValidationError("Número de lote no corresponde al que indica el sistema, N° Lote %s" % self.lot_id.name)



class SeguimientoDespacho(models.Model):
    _inherit = 'stock.picking'

    status_despacho_id = fields.Many2one(comodel_name="cotaco.status.despacho", string="Status de Despacho", required=False, )
    observacion = fields.Char(string="Observación", required=False, )
    horario_cliente = fields.Char(string="Horario de Entrega", compute='_ObtieneDatosSO')
    ficha_tecnica = fields.Boolean(string="Ficha Técnica", compute='_ObtieneDatosSO')
    hoja_seguridad = fields.Boolean(string="Hoja de Seguridad", compute='_ObtieneDatosSO')
    #certificado_calidad = fields.Boolean(string="Certificado de Calidad", related='partner_id.certificado_calidad')
    especificar_oc = fields.Boolean(string="Especificar OC", compute='_ObtieneDatosSO')
    especificar_hes = fields.Boolean(string="Especificar HES", compute='_ObtieneDatosSO')
    despacha_guia = fields.Boolean(string="Despachar con Guía", compute='_ObtieneDatosSO')
    instrucciones_cliente = fields.Text(compute='_Instrucciones_Cliente')
    observaciones = fields.Char(string="Obs.Venta", related='partner_id.obs_venta')
    analytic_account_id = fields.Many2one(string='Proyecto',comodel_name='account.analytic.account',)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        for i in self.move_lines:
            i.analityc_account_id=self.project_id
        return True


    @api.depends('partner_id')
    def _Instrucciones_Cliente(self):
        self.instrucciones_cliente = " "

        if(self.observaciones):
            self.instrucciones_cliente += "Obs." + self.observaciones + "\n\n"

        if (self.horario_cliente):
            self.instrucciones_cliente += "-> Horario : " + self.horario_cliente

        if (self.ficha_tecnica):
            self.instrucciones_cliente += "-> Ficha técnica "

        if(self.hoja_seguridad):
            self.instrucciones_cliente += "-> Hoja de seguridad "

        if(self.especificar_oc):
            self.instrucciones_cliente += "-> Especificar OC "

        if(self.especificar_hes):
            self.instrucciones_cliente += "-> Especificar HES "

        if(self.despacha_guia):
            self.instrucciones_cliente += "-> Despacho con guía "


    @api.one
    @api.depends('origin')
    def _ObtieneDatosSO(self):
        domain = [
            ('name', '=', self.origin)
        ]
        so=self.env['sale.order'].search(domain)
        for i in so:
            self.horario_cliente=i.horario_cliente
            self.ficha_tecnica=i.ficha_tecnica
            self.hoja_seguridad=i.ficha_tecnica
            self.especificar_oc=i.especificar_oc
            self.especificar_hes=i.especificar_hes
            self.despacha_guia=i.despacha_guia



class StatusDespacho(models.Model):
    _name = 'cotaco.status.despacho'

    name = fields.Char(string="Status de Despacho", required=False, )
