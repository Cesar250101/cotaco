# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta


class TransportesExternos(models.Model):
    _name = 'cotaco.transportes'
    _description = 'Transportes Externos'

    name = fields.Char(string='Transporte Externo')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Proveedor", required=False, domain=[('supplier','=','true')] )



class LineasPedidoVenta(models.Model):
    _inherit = 'sale.order.line'

    item_precios = fields.Char(string='Precios', compute='_Obtener_Precios')
    user_id = fields.Many2one(comodel_name="res.users", string="Vendedor", required=False, )
    team_id = fields.Many2one(comodel_name="crm.team", string="Canal", required=False, )



    @api.one
    @api.depends('product_id')
    #@api.onchange('product_id')
    def _Obtener_Precios(self):
        precios = self.product_id.pricelist_item_ids
        precios_1 = ""

        for p in precios:
            precios_1 += str(p.fixed_price)+ ' - '

        self.item_precios=precios_1


class ExcepcionesVenta(models.Model):
    _inherit = 'sale.order'
    despacho_guia = fields.Boolean(string="Despacho con Guia")
    despacho_representante = fields.Boolean(string="Despacha Vendedor")
    es_muestra = fields.Boolean(string="Es muestra?")
    retira_cliente = fields.Boolean(string="Retira Cliente")
    adjunta_doc_prod = fields.Boolean(string="Adjunto documentación del producto")
    despacho_cotaco = fields.Boolean(string="Despacha Cotaco?", )
    transporte = fields.Many2one(comodel_name="cotaco.transportes", string="Transporte", required=False, )
    valor_transporte = fields.Integer(string="Valor Despacho", required=False, )
    horario_cliente = fields.Char(string="Horario de Entrega", related='partner_id.hora_entrega')
    ficha_tecnica = fields.Boolean(string="Ficha Técnica", related='partner_id.ficha_tecnica')
    hoja_seguridad = fields.Boolean(string="Hoja de Seguridad", related='partner_id.hoja_seguridad')
    especificar_oc = fields.Boolean(string="Especificar OC", related='partner_id.especificar_oc')
    especificar_hes = fields.Boolean(string="Especificar HES", related='partner_id.especificar_hes')
    despacha_guia = fields.Boolean(string="Despachar con Guía", related='partner_id.despacha_guia')

    items_precios_3 = fields.Integer(string='Precios', compute='_Obtener_Precios')

    instrucciones_cliente = fields.Text(compute='_Instrucciones_Cliente')
    observaciones = fields.Char(string="Obs.Venta", related='partner_id.obs_venta')


    @api.onchange('partner_id')
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

    @api.multi
    def check_duplicate_order(self):
        self.ensure_one()
        # por compatibilidad con el modulo de sale_order_type_invoice_policy
        if self._context.get('by_pass_credit_limit', False):
            return True

        desdeFecha = date.today() - timedelta(days=30)
        desde = datetime(desdeFecha.year, desdeFecha.month, desdeFecha.day, 0, 0, 0, 0)
        desdeStr = desde.strftime("%Y-%m-%d %I:%M:%S")

        domain = [
            ('id', '!=', self.id),
            ('amount_total', '=', self.amount_total),
            ('partner_id', '=', self.partner_id.id),
            ('confirmation_date', '>=', desdeStr)
        ]
        order = self.env['sale.order'].search(domain)

        for r in order:
            print(r.name)

        if order:
            return False

        return True

    @api.multi
    def check_protested_checks(self):
        self.ensure_one()
        # por compatibilidad con el modulo de sale_order_type_invoice_policy
        if self._context.get('by_pass_credit_limit', False):
            return True
        cuentas_excepcion = self.env['account.account'].search([('valida_excepcion', '=', True), ])

        debitos, creditos = 0, 0

        cuentas = []
        for reg in cuentas_excepcion:
            cuentas.append(reg.id)

        domain = [
            ('partner_id', '=', self.partner_id.id),
            ('account_id', 'in', cuentas),
            ('move_id.state', '=', 'posted'),
        ]
        protested = self.env['account.move.line'].search(domain)
        for prot in protested:
            debitos = +prot.debit
            creditos = +prot.credit

        dif = debitos - creditos
        if dif != 0:
            return False
        return True