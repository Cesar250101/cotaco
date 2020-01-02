# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64

class ListaPrecios(models.Model):
    _inherit = 'product.pricelist.item'

    comision = fields.Integer(string='% Comisión', default=0)

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

    nro_rombo_salud=fields.Char(string='N° Salud')
    nro_rombo_inflamable = fields.Char(string='N° Inflamable')
    nro_rombo_reactividad = fields.Char(string='N° Reactividad')
    nro_rombo_caract_especial = fields.Char(string='N° Caracteríadtica Especial')
    uso_texto = fields.Html(string='Uso')
    almacen_texto = fields.Html(string='Almacenamiento')
    precaucion_texto = fields.Html(string='Precaución')
    composicion_texto = fields.Html(string='Composición')
    primeros_auxilios_texto = fields.Html(string='Primeros Auxilios')
    registro_isp = fields.Char(string='Registro ISP')
    items_precios_1 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    items_precios_2 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    items_precios_3 = fields.Integer(sring='Precios', compute='_Obtener_Precios')
    densidad = fields.Float(string="Densidad",  required=False, )
    is_new_field = fields.Boolean(string="Puede Ver Precios",compute=""  )
    product_doc_id=fields.Many2one('cotaco.doc', string = 'Ficha Técnica')
    product_doc_seguridad = fields.Many2one('cotaco.doc', string='Hoja de Seguridad')
    product_doc_calidad = fields.Many2one('cotaco.doc', string='Ficha Técnica')

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

class DocumentacionProductos(models.Model):
    _name = 'cotaco.doc'
    _rec_name='txt_filename'
    _description = 'Documentación de Productos'

    txt_filename = fields.Char(string='Nombre del Archivo')
    txt_binary = fields.Binary(string='Archivo')
    product_id = fields.Many2many(comodel_name="product.template", string="Productos", )

    @api.one
    def generate_file(self):
        """
        function called from button
        """

        content = ''
    # make something to generate content
        return self.write({
            #'txt_filename': 'file.txt',
            'txt_binary': base64.encodestring(content)
        })


class UnidadesMedida(models.Model):

    _inherit = 'product.uom'

    name_mostrado = fields.Char(string='Nombre a Mostrar')

