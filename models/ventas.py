# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT



class Cliente(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'display_name'

    hora_entrega=fields.Char(string="Horario de Entrega")
    ficha_tecnica = fields.Boolean(string="Adjuntar Ficha Técnica")
    hoja_seguridad = fields.Boolean(string="Adjuntar Hoja de Seguridad")
    especificar_oc = fields.Boolean(string="Especificar Orden de Compra")
    especificar_hes = fields.Boolean(string="Especificar HES")
    despacha_guia = fields.Boolean(string="Despachar con Guía?")
    obs_venta = fields.Char(string="Observación venta")



class TransportesExternos(models.Model):
    _name = 'cotaco.transportes'
    _description = 'Transportes Externos'

    name = fields.Char(string='Transporte Externo')
    partner_id = fields.Many2one(comodel_name="res.partner", string="Proveedor", required=False, domain=[('supplier','=','true')] )


class LineasPedidoVenta(models.Model):
    _inherit = 'sale.order.line'

    cliente_id = fields.Integer(string="Cliente", related="order_id.partner_id.id", required=False, )
    state_order=fields.Selection(string="Status",related="order_id.state")
    ultima_venta=fields.Date(string="Última Ventas")
    ultimo_precio = fields.Integer(string="Último Precio", required=False, )
    item_precios = fields.Char(string='Precios', compute='_Obtener_Precios')



    # @api.one
    # @api.constrains('price_unit')
    # def check_costo_precio(self):
    #     self.ensure_one()
    #     # por compatibilidad con el modulo de sale_order_type_invoice_policy
    #     #if self._context.get('by_pass_credit_limit', False):
    #     #    return True
    #     product_id=self.product_id.product_tmpl_id.id
    #     domain = [
    #         ('product_tmpl_id', '=', product_id),
    #         ('pricelist_id', '=', 1)
    #     ]
    #     precio_uno = self.env['product.pricelist_item'].search(domain,limit=1).fixed_price
    #     precio_uno=precio_uno*0,8
    #
    #     if self.price_unit < precio_uno:
    #         raise ValidationError("Precio no puede ser menor al precio de venta mas bajo de la lista 1 (precio-20%)")

    def action_show_details(self):
        self.ensure_one()
        view = self.env.ref('cotaco.view_historial_venta_cliente')



        domain = [
            ('product_id', '=', self.product_id.id),
            ('state_order', 'in', ('sale', 'done')),
            ('cliente_id', '=', self.cliente_id)
        ]

        ultima_venta=self.env['sale.order.line'].search(domain,order='create_date desc',limit=1).create_date
        ultimo_precio=self.env['sale.order.line'].search(domain,order='create_date desc',limit=1).price_unit
        self.ultima_venta=ultima_venta
        self.ultimo_precio=ultimo_precio

        #picking_type_id = self.picking_type_id or self.picking_id.picking_type_id
        return {
            'name': ('Historial de Ventas Clientes'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order.line',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            'ultima_venta': ultima_venta,
        }

    # @api.one
    # @api.constrains('user_id')
    # def _check_vendedor(self):
    #     vendedor=""
    #     if self.order_id.partner_shipping_id and self.product_id:
    #         if self.user_id=="":
    #             raise ValidationError("Debe seleccionar un vendedor en cada línea de producto!")
    #         division=self.env['product.category'].search([('id','=',self.product_id.categ_id.id)])
    #         for d in division:
    #             if 'Agua' in d.complete_name:
    #                 vendedor=self.env['res.partner'].search([('id','=',self.order_id.partner_shipping_id.id)],limit=1).user_id
    #             if 'Indust' in d.complete_name:
    #                 vendedor=self.env['res.partner'].search([('id','=',self.order_id.partner_shipping_id.id)],limit=1).user_id_ti

    @api.onchange('product_id')
    def _onchange(self):
        if self.order_id.partner_shipping_id and self.product_id:
            division=self.env['product.category'].search([('id','=',self.product_id.categ_id.id)])
            for d in division:
                if 'Agua' in d.complete_name:
                    vendedor=self.env['res.partner'].search([('id','=',self.order_id.partner_shipping_id.id)])
                    for v in vendedor:
                        self.user_id=v.user_id
                if 'Indust' in d.complete_name:
                    vendedor=self.env['res.partner'].search([('id','=',self.order_id.partner_shipping_id.id)])
                    for v in vendedor:
                        self.user_id=v.user_id_ti

    # @api.onchange('user_id')
    # def _onchange(self):
    #     if self.user_id:
    #         equipo_id=self.env['team.favorite.user.rel'].search([('user_id','=',self.user_id)])
    #         for e in equipo_id:
    #             self.team_id=e.team_id




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
    despacho_cotaco = fields.Boolean(string="Transporte Externo", )
    paga_cliente = fields.Boolean(string="Flete por Pagar", )
    transporte = fields.Many2one(comodel_name="cotaco.transportes", string="Transporte", required=False, )
    valor_transporte = fields.Integer(string="Valor Despacho", required=False, )
    horario_cliente = fields.Char(string="Horario de Entrega", related='partner_id.hora_entrega')
    ficha_tecnica = fields.Boolean(string="Ficha Técnica", related='partner_id.ficha_tecnica')
    hoja_seguridad = fields.Boolean(string="Hoja de Seguridad", related='partner_id.hoja_seguridad')
    #certificado_calidad = fields.Boolean(string="Certificado de Calidad", related='partner_id.certificado_calidad')
    especificar_oc = fields.Boolean(string="Especificar OC", related='partner_id.especificar_oc')
    especificar_hes = fields.Boolean(string="Especificar HES", related='partner_id.especificar_hes')
    despacha_guia = fields.Boolean(string="Despachar con Guía", related='partner_id.despacha_guia')

    items_precios_3 = fields.Integer(string='Precios', compute='_Obtener_Precios')

    instrucciones_cliente = fields.Text(compute='_Instrucciones_Cliente')
    observaciones = fields.Char(string="Obs.Venta", related='partner_id.obs_venta')
    recibe_cliente = fields.Char(string="Quien Recibe?")
    order_repair_ids = fields.One2many(comodel_name="mrp.repair", inverse_name="orden_venta", string="Ordenes de Reparación", required=False, )
    rendicion_gastos_ids = fields.One2many(comodel_name="hr.expense", inverse_name="sale_order_id", string="Redición de Gastos", required=False, )
    tota_armado = fields.Integer(string="Costo Armado Equipo", required=False,compute="_compute_amount_costo_armado")
    total_rendiciones = fields.Integer(string="Costo Armado Equipo", required=False,compute="_compute_amount_costo_armado")
    costo_armado_rendicion = fields.Integer(string="Costo Armado Equipo", required=False,compute="_compute_amount_costo_armado" )

    @api.one
    @api.depends('order_repair_ids','rendicion_gastos_ids')
    def _compute_amount_costo_armado(self):
        total_armado=0
        total_gastos=0
        armado=self.env["mrp.repair"].search([('orden_venta','=',self.id)])
        for i in armado:
            total_armado+=i.amount_total
            self.tota_armado=total_armado
        gastos=self.env["hr.expense"].search([('sale_order_id','=',self.id)])
        for i in gastos:
            total_gastos+=i.total_amount
            self.total_rendiciones=total_gastos
        self.costo_armado_rendicion=total_armado+total_gastos

    @api.one
    @api.constrains('es_muestra')
    def check_muestra(self):
        context = self._context
        current_uid = context.get('uid')
        permisos=self.env['res.users'].search([('id','=',current_uid)],limit=1).aprueba_muestras
        if self.es_muestra:
            if permisos!=True:
                raise ValidationError('No puede confirmar un presupuesta que esta marcado como muestra')


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

class ComisionTramo(models.Model):
    _name = "comision.tramo"

    desde = fields.Float('UF > desde', required=True)
    hasta = fields.Float('UF <= hasta', required=True)
    comision = fields.Float('% comision', requiere=True)
    descripcion = fields.Html(string="Descripción")


class ComisionFactorizacion(models.Model):
    _name = "comision.factorizacion"

    descuento = fields.Float('Descuento', required=True)
    factor = fields.Float('Factor', required=True)

class ListaPrecios(models.Model):
    _inherit = 'product.pricelist.item'

    comision = fields.Integer(string='% Comisión', default=0)