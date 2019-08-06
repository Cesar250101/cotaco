# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import logging
from odoo import exceptions
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class Clase(models.Model):
    _name = 'cotaco.clase'
    name = fields.Char(String='Clase')

class NU(models.Model):
    _name = 'cotaco.nu'
    name = fields.Char(String='NU')
    active = fields.Boolean("Activo?")


class ProductoClaseUN(models.Model):
    _inherit = 'product.template'
    nu = fields.Many2one('cotaco.nu',string='NU')
    clase = fields.Many2one('cotaco.clase', string = 'Clase')

    uso_texto = fields.Html('Uso')
    almacen_texto = fields.Html('Almacenamiento')
    precaucion_texto = fields.Html('Precaución')
    composicion_texto = fields.Html('Composición')
    primeros_auxilios_texto = fields.Html('Primeros Auxilios')
    registro_isp = fields.Char('Registro ISP')
    items_precios_1 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    items_precios_2 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    items_precios_3 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    densidad = fields.Float(string="Densidad",  required=False, )
    is_new_field = fields.Boolean(string="Puede Ver Precios",compute=""  )

    @api.one
    @api.depends('item_ids')
    def _Obtener_Precios(self):
        precios_lista=""
        precios=self.env['product.pricelist.item'].search([('product_tmpl_id','=',self.id)])
        r=1
        for i in precios:
            if r==1:
                self.items_precios_1=i.fixed_price
            elif r==2:
                self.items_precios_2 = i.fixed_price
            elif r==3:
                self.items_precios_3 = i.fixed_price
            r+=1



    @api.one
    @api.depends('item_ids')
    def _Obtener_Precios(self):
        precios_lista=""
        precios=self.env['product.pricelist.item'].search([('product_tmpl_id','=',self.id)])
        r=1
        for i in precios:
            if r==1:
                self.items_precios_1=i.fixed_price
            elif r==2:
                self.items_precios_2 = i.fixed_price
            elif r==3:
                self.items_precios_3 = i.fixed_price
            r+=1
