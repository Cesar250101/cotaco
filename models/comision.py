# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta


class TablaComisionEquipos(models.Model):
    _name = "comision.equipos"

    factor = fields.Float(string="Factor",  required=False, )
    porc_vendedor= fields.Float(string="% Comisión Vendedor",  required=False, )
    porc_margen= fields.Float(string="% Margen",  required=False, )


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



class ComisionesAntiguos(models.Model):
    _inherit = 'hr.payslip'

    @api.one
    def calcular_comision(self):

        hoy = self.date_from
        # fechaStr = hoy.strftime("%Y-%m") + '-' + '01'
        fechaStr = hoy
        hastaStr = datetime.strptime(fechaStr, '%Y-%m-%d')
        hastaStr = hastaStr - timedelta(days=1)
        hastaStr = hastaStr.strftime("%Y-%m-%d")

        desdeStr = hastaStr[:-2] + '01'

        domain = [
            ('state', 'in', ['open', 'paid']),
            ('type', '=', 'out_invoice'),
            ('user_id', '=', self.employee_id.user_id.id),
            ('date_invoice', '>=', desdeStr),
            ('date_invoice', '<=', hastaStr)
        ]

        invoice = self.env['account.invoice'].search(domain)
        total = 0
        ids_invoice = []

        for i in invoice:
            total += i.amount_untaxed
            ids_invoice.append(i.id)

        domain = [
            ('name', '=', 'UF'),
            ('date', '=', self.date_to),
        ]

        conversion_uf = self.env['res.currency'].search(domain)
        for i in conversion_uf:
            valor_uf = i.rate

        total_uf = total * valor_uf

        domain = [
            ('code', '=', 'COMI'),
        ]
        rec = self.env['hr.payslip.input'].search(domain)
        rec.write({'amount': total_uf})

        domain = [
            ('desde', '<', total_uf),
            ('hasta', '>=', total_uf),
        ]

        tramo = self.env['comision.tramo'].search(domain)
        for i in tramo:
            porc_comision = i.comision / 100

        domain = [
            ('invoice_id', 'in', ids_invoice),
        ]
        invoice_line = self.env['account.invoice.line'].search(domain)
        valor_comision = 0
        for i in invoice_line:
            paso = 1
            precio = (i.price_subtotal / i.quantity)
            factura = self.env['account.invoice'].search([('id', '=', i.invoice_id.id)])

            for f in factura:
                subtotal = f.amount_untaxed
                descuento = f.amount_untaxed_global_discount
                subtotal_original = subtotal + descuento
                factor_dscto = descuento / subtotal_original
                factor_dscto = 1 - factor_dscto
                precio = precio * factor_dscto

            factor_comision = 0
            product_id = i.product_id.product_tmpl_id.id
            preciolista = self.env['product.pricelist.item'].search([('product_tmpl_id', '=', product_id), ])
            if preciolista:
                matriz_precio = []
                for r in preciolista:
                    matriz_precio.append(r.fixed_price)
                if precio < matriz_precio[0]:
                    porc_descuento_precio = round((100 - ((i.price_unit * 100) / matriz_precio[0])), 1)

                    domain = [
                        ('descuento', '=', porc_descuento_precio),
                    ]
                    factor = self.env['comision.factorizacion'].search(domain)
                    for n in factor:
                        factor_comision = n.factor
                    porc_comision_factorizada = porc_comision * factor_comision

                    valor_comision += i.price_subtotal * (porc_comision_factorizada / 100)

                elif precio >= matriz_precio[0] and precio < matriz_precio[1]:
                    if r.comision != 0:
                        valor_comision += i.price_subtotal * (r.comision / 100)
                    else:
                        valor_comision = +i.price_subtotal * (porc_comision / 100)
                elif precio >= matriz_precio[1] and precio < matriz_precio[2]:
                    if r.comision != 0:
                        valor_comision += i.price_subtotal * (r.comision / 100)
                    else:
                        valor_comision += i.price_subtotal * (porc_comision / 100)
                elif precio >= matriz_precio[2]:
                    if r.comision != 0:
                        valor_comision += i.price_subtotal * (r.comision / 100)
                    else:
                        valor_comision += i.price_subtotal * (porc_comision / 100)
        payslip = self.env['hr.payslip.input'].search([('code', '=', 'COMI')])
        payslip.write({'amount': valor_comision})
        return True

    @api.one
    def Factorizar(self, precio_lista, precio_factura, tramo_comision):
        porc_descuento_precio = 100 - ((precio_factura * 100) / precio_lista)
        domain = [
            ('descuento', '=', porc_descuento_precio),
        ]
        factor = self.env['comision.factorizacion'].search(domain)
        comision = tramo_comision * factor.factor
        return comision