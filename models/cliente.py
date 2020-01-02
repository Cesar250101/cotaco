# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cliente(models.Model):
    _inherit = 'res.partner'
    #_rec_name = 'display_name'

    hora_entrega=fields.Char(string="Horario de Entrega")
    ficha_tecnica = fields.Boolean(string="Adjuntar Ficha Técnica")
    hoja_seguridad = fields.Boolean(string="Adjuntar Hoja de Seguridad")
    #certificado_calidad = fields.Boolean(string="Certificado de Calidad")
    especificar_oc = fields.Boolean(string="Especificar Orden de Compra")
    especificar_hes = fields.Boolean(string="Especificar HES")
    despacha_guia = fields.Boolean(string="Despachar con Guía?")
    obs_venta = fields.Char(string="Observación venta")
    user_id_ti = fields.Many2one(comodel_name="res.users", string="Vendedor DI", required=False, )

